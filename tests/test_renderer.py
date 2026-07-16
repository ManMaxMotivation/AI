import json
from pathlib import Path

from qa_case_pipeline.renderer import render_plan


FIXTURES = Path(__file__).parents[1] / "src" / "qa_case_pipeline" / "fixtures"


def test_render_plan_writes_all_four_stages(tmp_path: Path) -> None:
    plan = json.loads((FIXTURES / "ui-state-persistence" / "plan.en.json").read_text(encoding="utf-8"))

    output_dir = render_plan(plan, tmp_path / "artifacts", "en")

    assert output_dir == tmp_path / "artifacts"
    for filename in ("analysis.md", "algorithm.md", "automated-checks.md", "manual-checks.md", "qa-plan.json"):
        assert (output_dir / filename).is_file()
    assert "# Analysis" in (output_dir / "analysis.md").read_text(encoding="utf-8")
