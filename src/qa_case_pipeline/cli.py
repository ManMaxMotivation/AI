"""Command-line entry point for the public QA case pipeline."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .case_renderer import prepare_case, render_automated_report, render_final_report
from .codex_adapter import CodexAdapter, CodexExecutionError, codex_login_available
from .evidence import CaseValidationError, verify_case
from .models import BriefValidationError, load_brief
from .reference_checks import run_reference_checks
from .renderer import render_plan


PACKAGE_ROOT = Path(__file__).resolve().parent
FIXTURES_ROOT = PACKAGE_ROOT / "fixtures"
TEMPLATES_ROOT = PACKAGE_ROOT / "templates"
SCHEMA_PATH = PACKAGE_ROOT / "schemas" / "qa-plan.schema.json"


def _write_evidence(output_dir: Path, result: dict[str, object]) -> None:
    (output_dir / "reference-checks.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _plan(args: argparse.Namespace) -> int:
    brief = load_brief(args.brief)
    if not codex_login_available():
        raise CodexExecutionError(
            "Codex CLI is not authenticated. Run `codex login` before the plan command."
        )

    plan = CodexAdapter().generate(brief, args.language, SCHEMA_PATH)
    output_dir = render_plan(plan, args.output, args.language)
    print(f"QA plan written to {output_dir}")
    return 0


def _validate(args: argparse.Namespace) -> int:
    result = run_reference_checks(args.case)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    if args.evidence:
        args.evidence.parent.mkdir(parents=True, exist_ok=True)
        args.evidence.write_text(payload + "\n", encoding="utf-8")
    return 0 if result["passed"] else 1


def _demo(args: argparse.Namespace) -> int:
    if args.case == "reservation-state-propagation":
        output_dir = args.output or Path.cwd() / "qa-case-pipeline-demo" / args.case
        if output_dir.exists() and any(output_dir.iterdir()):
            raise ValueError(f"Refusing to overwrite non-empty directory: {output_dir}")
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(TEMPLATES_ROOT / args.case, output_dir, dirs_exist_ok=True)
        shutil.copy2(output_dir / "demo-manual-results.yaml", output_dir / "manual-results.yaml")
        (output_dir / "demo-manual-results.yaml").unlink()
        prepare_case(output_dir)
        automated = verify_case(output_dir)
        render_automated_report(output_dir, automated)
        report_path, passed = render_final_report(output_dir, automated, synthetic_demo=True)
        print(f"Complete synthetic QA case written to {output_dir}")
        print(f"Final report: {report_path}")
        return 0 if passed else 1

    case_dir = FIXTURES_ROOT / args.case
    if not case_dir.is_dir():
        raise ValueError(f"Unknown demo case: {args.case}")

    output_dir = args.output or Path.cwd() / "qa-case-pipeline-demo" / args.case
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = case_dir / f"plan.{args.language}.json"
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    render_plan(plan, output_dir, args.language)

    for filename in ("brief.yaml", "input.json", "expected.json"):
        shutil.copy2(case_dir / filename, output_dir / filename)

    result = run_reference_checks(case_dir)
    _write_evidence(output_dir, result)
    print(f"Demo artifacts written to {output_dir}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


def _init(args: argparse.Namespace) -> int:
    source = TEMPLATES_ROOT / args.template
    output_dir = args.output
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"Refusing to overwrite non-empty directory: {output_dir}")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, output_dir, dirs_exist_ok=True)
    demo_record = output_dir / "demo-manual-results.yaml"
    if demo_record.exists():
        demo_record.unlink()
    print(f"Created QA case at {output_dir}")
    print("Edit brief.yaml, verification.yaml, evidence/*.json, and manual-results.yaml before running it.")
    return 0


def _prepare(args: argparse.Namespace) -> int:
    output_dir = prepare_case(args.case)
    print(f"Four-stage QA artifacts written to {output_dir}")
    return 0


def _verify(args: argparse.Namespace) -> int:
    result = verify_case(args.case)
    report_path = render_automated_report(args.case, result)
    print(f"Automated evidence report written to {report_path}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


def _report(args: argparse.Namespace) -> int:
    prepare_case(args.case)
    automated = verify_case(args.case)
    render_automated_report(args.case, automated)
    report_path, passed = render_final_report(args.case, automated)
    print(f"QA report written to {report_path}")
    return 0 if passed else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qa-case-pipeline",
        description="Create structured QA artifacts from a sanitized task brief.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="Generate QA artifacts with Codex CLI.")
    plan_parser.add_argument("--brief", type=Path, required=True, help="Sanitized YAML brief.")
    plan_parser.add_argument("--output", type=Path, required=True, help="Directory for artifacts.")
    plan_parser.add_argument("--language", choices=("en", "ru"), default="en")
    plan_parser.set_defaults(handler=_plan)

    validate_parser = subparsers.add_parser(
        "validate", help="Run deterministic checks for a synthetic fixture."
    )
    validate_parser.add_argument("--case", type=Path, required=True, help="Fixture directory.")
    validate_parser.add_argument("--evidence", type=Path, help="Optional JSON evidence path.")
    validate_parser.set_defaults(handler=_validate)

    demo_parser = subparsers.add_parser(
        "demo", help="Render a bundled synthetic case and run its reference checks."
    )
    demo_parser.add_argument(
        "--case",
        choices=("reservation-state-propagation", "ui-state-persistence", "schema-legacy-compat"),
        required=True,
    )
    demo_parser.add_argument("--output", type=Path, help="Directory for generated demo artifacts.")
    demo_parser.add_argument("--language", choices=("en", "ru"), default="en")
    demo_parser.set_defaults(handler=_demo)

    init_parser = subparsers.add_parser("init", help="Create an editable, portable QA case.")
    init_parser.add_argument("--template", choices=("reservation-state-propagation",), required=True)
    init_parser.add_argument("--output", type=Path, required=True)
    init_parser.set_defaults(handler=_init)

    prepare_parser = subparsers.add_parser(
        "prepare", help="Render analysis, algorithm, automated, and manual artifacts from a case."
    )
    prepare_parser.add_argument("--case", type=Path, required=True)
    prepare_parser.set_defaults(handler=_prepare)

    verify_parser = subparsers.add_parser(
        "verify", help="Evaluate local JSON evidence against the declarative assertions."
    )
    verify_parser.add_argument("--case", type=Path, required=True)
    verify_parser.set_defaults(handler=_verify)

    report_parser = subparsers.add_parser(
        "report", help="Create a final traceability report from automated and manual evidence."
    )
    report_parser.add_argument("--case", type=Path, required=True)
    report_parser.set_defaults(handler=_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (
        BriefValidationError,
        CaseValidationError,
        CodexExecutionError,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
