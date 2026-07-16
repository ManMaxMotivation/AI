"""Command-line entry point for the public QA case pipeline."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from .codex_adapter import CodexAdapter, CodexExecutionError, codex_login_available
from .models import BriefValidationError, load_brief
from .reference_checks import run_reference_checks
from .renderer import render_plan


PACKAGE_ROOT = Path(__file__).resolve().parent
FIXTURES_ROOT = PACKAGE_ROOT / "fixtures"
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
        "--case", choices=("ui-state-persistence", "schema-legacy-compat"), required=True
    )
    demo_parser.add_argument("--output", type=Path, help="Directory for generated demo artifacts.")
    demo_parser.add_argument("--language", choices=("en", "ru"), default="en")
    demo_parser.set_defaults(handler=_demo)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except (BriefValidationError, CodexExecutionError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
