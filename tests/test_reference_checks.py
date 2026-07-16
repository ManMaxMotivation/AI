import json
import shutil
from pathlib import Path

from qa_case_pipeline.reference_checks import run_reference_checks


FIXTURES = Path(__file__).parents[1] / "src" / "qa_case_pipeline" / "fixtures"


def test_all_bundled_reference_cases_pass() -> None:
    for name in ("ui-state-persistence", "schema-legacy-compat"):
        result = run_reference_checks(FIXTURES / name)
        assert result["passed"], result


def test_ui_reference_check_detects_filter_regression(tmp_path: Path) -> None:
    case_dir = tmp_path / "ui-state-persistence"
    shutil.copytree(FIXTURES / "ui-state-persistence", case_dir)
    input_path = case_dir / "input.json"
    data = json.loads(input_path.read_text(encoding="utf-8"))
    data["after_navigation"]["filters"]["term_months"] = 48
    input_path.write_text(json.dumps(data), encoding="utf-8")

    result = run_reference_checks(case_dir)

    assert not result["passed"]
    assert any(check["id"] == "preserve-term_months" and not check["passed"] for check in result["checks"])
