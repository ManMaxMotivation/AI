"""Validate local JSON evidence with a declarative QA manifest.

The verifier deliberately does not run shell commands, browser code, or network
requests. A team collects evidence using its own approved tooling, exports the
relevant response or UI state as JSON, and this module makes the acceptance
logic reproducible and reviewable.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class CaseValidationError(ValueError):
    """Raised when a portable QA case is incomplete or malformed."""


@dataclass(frozen=True)
class AssertionResult:
    pointer: str
    operator: str
    expected: Any
    actual: Any
    passed: bool
    detail: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "pointer": self.pointer,
            "operator": self.operator,
            "expected": self.expected,
            "actual": self.actual,
            "passed": self.passed,
            "detail": self.detail,
        }


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CaseValidationError(f"Cannot read '{path}': {error}") from error
    except yaml.YAMLError as error:
        raise CaseValidationError(f"Cannot parse YAML '{path}': {error}") from error
    if not isinstance(value, dict):
        raise CaseValidationError(f"'{path}' must contain a YAML mapping.")
    return value


def load_case(case_dir: Path) -> dict[str, Any]:
    manifest = _load_yaml(case_dir / "verification.yaml")
    required = ("requirements", "evidence", "automated_checks", "manual_checks")
    missing = [key for key in required if key not in manifest]
    if missing:
        raise CaseValidationError(f"verification.yaml is missing: {', '.join(missing)}.")
    if not all(isinstance(manifest[key], list) for key in ("requirements", "automated_checks", "manual_checks")):
        raise CaseValidationError("requirements, automated_checks, and manual_checks must be lists.")
    if not isinstance(manifest["evidence"], dict):
        raise CaseValidationError("evidence must be a mapping of names to local JSON files.")
    return manifest


def _inside_case(case_dir: Path, relative_path: str) -> Path:
    candidate = (case_dir / relative_path).resolve()
    try:
        candidate.relative_to(case_dir.resolve())
    except ValueError as error:
        raise CaseValidationError(f"Evidence path escapes the case directory: {relative_path}") from error
    return candidate


def load_evidence(case_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    evidence: dict[str, Any] = {}
    for name, relative_path in manifest["evidence"].items():
        if not isinstance(name, str) or not isinstance(relative_path, str):
            raise CaseValidationError("Evidence names and paths must be strings.")
        path = _inside_case(case_dir, relative_path)
        try:
            evidence[name] = json.loads(path.read_text(encoding="utf-8"))
        except OSError as error:
            raise CaseValidationError(f"Cannot read evidence '{name}' at '{relative_path}': {error}") from error
        except json.JSONDecodeError as error:
            raise CaseValidationError(f"Evidence '{name}' is not valid JSON: {error}") from error
    return evidence


def resolve_pointer(document: Any, pointer: str) -> tuple[bool, Any]:
    """Resolve an RFC 6901 JSON Pointer without treating missing values as null."""
    if pointer == "":
        return True, document
    if not pointer.startswith("/"):
        raise CaseValidationError(f"JSON Pointer must start with '/': {pointer!r}")
    current = document
    for raw_segment in pointer[1:].split("/"):
        segment = raw_segment.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict):
            if segment not in current:
                return False, None
            current = current[segment]
        elif isinstance(current, list):
            if not segment.isdigit() or int(segment) >= len(current):
                return False, None
            current = current[int(segment)]
        else:
            return False, None
    return True, current


def evaluate_assertion(document: Any, assertion: dict[str, Any]) -> AssertionResult:
    pointer = assertion.get("pointer")
    operator = assertion.get("operator")
    if not isinstance(pointer, str) or not isinstance(operator, str):
        raise CaseValidationError("Every assertion needs string 'pointer' and 'operator' fields.")
    found, actual = resolve_pointer(document, pointer)
    expected = assertion.get("value")

    if operator == "exists":
        wanted = assertion.get("value", True)
        passed = found is wanted
        detail = "Pointer presence matches the expected value."
    elif operator == "equals":
        passed = found and actual == expected
        detail = "Value equals the expected value."
    elif operator == "not_equals":
        passed = found and actual != expected
        detail = "Value differs from the excluded value."
    elif operator == "contains":
        passed = found and isinstance(actual, (str, list, dict)) and expected in actual
        detail = "Value contains the expected member or substring."
    elif operator == "matches":
        if not isinstance(expected, str):
            raise CaseValidationError("The 'matches' operator needs a string value.")
        passed = found and isinstance(actual, str) and re.search(expected, actual) is not None
        detail = "String matches the expected regular expression."
    else:
        raise CaseValidationError(f"Unsupported assertion operator: {operator!r}.")
    return AssertionResult(pointer, operator, expected, actual, bool(passed), detail)


def verify_case(case_dir: Path) -> dict[str, Any]:
    manifest = load_case(case_dir)
    evidence = load_evidence(case_dir, manifest)
    checks: list[dict[str, Any]] = []
    for check in manifest["automated_checks"]:
        if not isinstance(check, dict):
            raise CaseValidationError("Every automated check must be a mapping.")
        for key in ("id", "requirement", "purpose", "source", "assertions"):
            if key not in check:
                raise CaseValidationError(f"Automated check is missing '{key}'.")
        if check["source"] not in evidence:
            raise CaseValidationError(f"Check '{check['id']}' uses unknown evidence '{check['source']}'.")
        if not isinstance(check["assertions"], list) or not check["assertions"]:
            raise CaseValidationError(f"Check '{check['id']}' needs at least one assertion.")
        assertions = [evaluate_assertion(evidence[check["source"]], item) for item in check["assertions"]]
        checks.append(
            {
                "id": check["id"],
                "requirement": check["requirement"],
                "purpose": check["purpose"],
                "source": check["source"],
                "passed": all(item.passed for item in assertions),
                "assertions": [item.as_dict() for item in assertions],
            }
        )
    return {"passed": all(check["passed"] for check in checks), "checks": checks}


def load_manual_results(case_dir: Path, manifest: dict[str, Any]) -> list[dict[str, Any]]:
    results_path = case_dir / "manual-results.yaml"
    raw = _load_yaml(results_path)
    results = raw.get("checks")
    if not isinstance(results, list):
        raise CaseValidationError("manual-results.yaml must contain a 'checks' list.")
    planned = {item.get("id"): item for item in manifest["manual_checks"] if isinstance(item, dict)}
    submitted = {item.get("id"): item for item in results if isinstance(item, dict)}
    normalized: list[dict[str, Any]] = []
    for check_id, planned_check in planned.items():
        result = submitted.get(check_id, {})
        status = result.get("status", "not_run")
        if status not in {"passed", "failed", "blocked", "not_run"}:
            raise CaseValidationError(f"Manual check '{check_id}' has unsupported status '{status}'.")
        normalized.append(
            {
                "id": check_id,
                "requirement": planned_check.get("requirement"),
                "purpose": planned_check.get("purpose"),
                "expected": planned_check.get("expected"),
                "status": status,
                "evidence": result.get("evidence", ""),
                "notes": result.get("notes", ""),
            }
        )
    return normalized
