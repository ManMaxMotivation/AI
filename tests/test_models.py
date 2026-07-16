from pathlib import Path

import pytest

from qa_case_pipeline.models import BriefValidationError, load_brief


FIXTURES = Path(__file__).parents[1] / "src" / "qa_case_pipeline" / "fixtures"


def test_loads_sanitized_brief() -> None:
    brief = load_brief(FIXTURES / "ui-state-persistence" / "brief.yaml")

    assert brief.case_type == "ui_state_persistence"
    assert brief.acceptance_criteria[0] == "The selected catalog remains selected after navigation."


def test_rejects_missing_required_field(tmp_path: Path) -> None:
    brief_path = tmp_path / "brief.yaml"
    brief_path.write_text("title: Missing fields\n", encoding="utf-8")

    with pytest.raises(BriefValidationError, match="Missing required"):
        load_brief(brief_path)
