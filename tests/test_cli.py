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


def test_init_prepare_verify_and_report_form_a_usable_case(tmp_path: Path) -> None:
    case_dir = tmp_path / "reservation-case"

    assert main(["init", "--template", "reservation-state-propagation", "--output", str(case_dir)]) == 0
    assert not (case_dir / "demo-manual-results.yaml").exists()
    assert main(["prepare", "--case", str(case_dir)]) == 0
    assert main(["verify", "--case", str(case_dir)]) == 0
    assert main(["report", "--case", str(case_dir)]) == 1
    assert "INCOMPLETE OR FAILED" in (case_dir / "artifacts" / "qa-report.md").read_text(encoding="utf-8")


def test_full_demo_case_produces_a_traceable_final_report(tmp_path: Path) -> None:
    case_dir = tmp_path / "demo"

    assert main(["demo", "--case", "reservation-state-propagation", "--output", str(case_dir)]) == 0
    report = (case_dir / "artifacts" / "qa-report.md").read_text(encoding="utf-8")
    assert "SYNTHETIC COMPLETED EXAMPLE - NOT A RELEASE DECISION" in report
    assert "R-004" in report
