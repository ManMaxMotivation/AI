import json
import subprocess
from pathlib import Path

from qa_case_pipeline.codex_adapter import CodexAdapter, build_prompt
from qa_case_pipeline.models import load_brief


ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "src" / "qa_case_pipeline" / "fixtures"
SCHEMA = ROOT / "src" / "qa_case_pipeline" / "schemas" / "qa-plan.schema.json"


def test_prompt_preserves_safety_boundary() -> None:
    brief = load_brief(FIXTURES / "ui-state-persistence" / "brief.yaml")
    prompt = build_prompt(brief, "en")

    assert "Do not request secrets" in prompt
    assert "manual exploratory testing" in prompt


def test_adapter_uses_read_only_ephemeral_workspace() -> None:
    brief = load_brief(FIXTURES / "ui-state-persistence" / "brief.yaml")
    expected_plan = (FIXTURES / "ui-state-persistence" / "plan.en.json").read_text(encoding="utf-8")
    captured: dict[str, object] = {}

    def runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        captured["command"] = command
        captured["input"] = kwargs["input"]
        output_path = Path(command[command.index("--output-last-message") + 1])
        output_path.write_text(expected_plan, encoding="utf-8")
        return subprocess.CompletedProcess(command, 0, "", "")

    plan = CodexAdapter(runner=runner).generate(brief, "en", SCHEMA)

    command = captured["command"]
    assert isinstance(command, list)
    assert command[1:6] == ["exec", "--sandbox", "read-only", "--ephemeral", "--skip-git-repo-check"]
    assert "--ignore-rules" in command
    assert "--output-schema" in command
    assert plan["analysis"]["summary"].startswith("The change crosses")
