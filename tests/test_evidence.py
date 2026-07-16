import json
import shutil
from pathlib import Path

from qa_case_pipeline.evidence import verify_case


TEMPLATE = (
    Path(__file__).parents[1]
    / "src"
    / "qa_case_pipeline"
    / "templates"
    / "reservation-state-propagation"
)


def test_template_evidence_passes_all_declared_assertions() -> None:
    result = verify_case(TEMPLATE)

    assert result["passed"]
    assert len(result["checks"]) == 7


def test_verifier_reports_a_stale_action_regression(tmp_path: Path) -> None:
    case_dir = tmp_path / "case"
    shutil.copytree(TEMPLATE, case_dir)
    evidence_path = case_dir / "evidence" / "transition-window.json"
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["page_snapshot"]["ui"]["desktop_action"]["enabled"] = True
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    result = verify_case(case_dir)

    assert not result["passed"]
    assert not next(check for check in result["checks"] if check["id"] == "AUTO-007")["passed"]
