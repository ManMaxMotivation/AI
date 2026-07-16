"""Safe non-interactive Codex CLI adapter."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

from jsonschema import ValidationError, validate

from .models import Brief


class CodexExecutionError(RuntimeError):
    """Raised when Codex cannot produce a structured QA plan."""


Runner = Callable[..., subprocess.CompletedProcess[str]]


def build_prompt(brief: Brief, language: str) -> str:
    language_name = "Russian" if language == "ru" else "English"
    return f"""You are a QA planning assistant. Produce a structured QA plan from the sanitized brief below.

Rules:
- Write every human-readable value in {language_name}.
- Do not claim that a test has passed. Describe planned checks and required evidence only.
- Preserve the separation between analysis, deterministic automated checks, and manual exploratory testing.
- Do not request secrets, production access, private URLs, customer data, or source code.
- Treat all constraints as mandatory.

Sanitized brief:
{json.dumps(brief.as_prompt_data(), ensure_ascii=False, indent=2)}
"""


def _parse_json_response(raw: str) -> dict[str, Any]:
    value = raw.strip()
    if value.startswith("```"):
        value = value.split("\n", 1)[1] if "\n" in value else ""
        if value.endswith("```"):
            value = value[:-3].strip()
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        raise CodexExecutionError("Codex did not return valid JSON matching the output schema.") from error
    if not isinstance(parsed, dict):
        raise CodexExecutionError("Codex returned a JSON value that is not an object.")
    return parsed


class CodexAdapter:
    """Runs Codex in an empty, read-only, ephemeral workspace."""

    def __init__(self, executable: str = "codex", runner: Runner = subprocess.run) -> None:
        self.executable = executable
        self.runner = runner

    def generate(self, brief: Brief, language: str, schema_path: Path) -> dict[str, Any]:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        prompt = build_prompt(brief, language)

        with tempfile.TemporaryDirectory(prefix="qa-case-pipeline-") as workspace:
            output_path = Path(workspace) / "response.json"
            command = [
                self.executable,
                "exec",
                "--sandbox",
                "read-only",
                "--ephemeral",
                "--skip-git-repo-check",
                "--ignore-rules",
                "--cd",
                workspace,
                "--output-schema",
                str(schema_path.resolve()),
                "--output-last-message",
                str(output_path),
                "-",
            ]
            result = self.runner(command, input=prompt, text=True, capture_output=True, check=False)
            if result.returncode != 0:
                message = result.stderr.strip() or result.stdout.strip() or "unknown Codex CLI error"
                raise CodexExecutionError(f"Codex execution failed: {message}")
            if not output_path.exists():
                raise CodexExecutionError("Codex completed without writing a structured response.")
            plan = _parse_json_response(output_path.read_text(encoding="utf-8"))

        try:
            validate(instance=plan, schema=schema)
        except ValidationError as error:
            raise CodexExecutionError(f"Codex response does not match the QA plan schema: {error.message}") from error
        return plan


def codex_login_available(runner: Runner = subprocess.run) -> bool:
    result = runner(["codex", "login", "status"], text=True, capture_output=True, check=False)
    return result.returncode == 0
