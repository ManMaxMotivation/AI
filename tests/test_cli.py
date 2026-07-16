from pathlib import Path

from qa_case_pipeline.cli import main


def test_demo_generates_artifacts_and_evidence(tmp_path: Path) -> None:
    output_dir = tmp_path / "demo"

    exit_code = main(
        ["demo", "--case", "schema-legacy-compat", "--language", "ru", "--output", str(output_dir)]
    )

    assert exit_code == 0
    assert (output_dir / "manual-checks.md").is_file()
    assert (output_dir / "reference-checks.json").is_file()


def test_validate_writes_evidence(tmp_path: Path) -> None:
    root = Path(__file__).parents[1]
    case = root / "src" / "qa_case_pipeline" / "fixtures" / "ui-state-persistence"
    evidence = tmp_path / "evidence.json"

    exit_code = main(["validate", "--case", str(case), "--evidence", str(evidence)])

    assert exit_code == 0
    assert '"passed": true' in evidence.read_text(encoding="utf-8")
