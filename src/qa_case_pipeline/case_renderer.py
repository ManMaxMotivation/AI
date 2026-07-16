"""Render a portable QA case into reviewable Markdown artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .evidence import load_case, load_manual_results
from .models import load_brief


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _table(rows: list[list[str]], headings: list[str]) -> str:
    output = ["| " + " | ".join(headings) + " |", "| " + " | ".join("---" for _ in headings) + " |"]
    output.extend("| " + " | ".join(value.replace("|", "\\|") for value in row) + " |" for row in rows)
    return "\n".join(output)


def _artifacts_dir(case_dir: Path) -> Path:
    output = case_dir / "artifacts"
    output.mkdir(parents=True, exist_ok=True)
    return output


def prepare_case(case_dir: Path) -> Path:
    """Build the first, second, and planned fourth QA stages without an LLM."""
    brief = load_brief(case_dir / "brief.yaml")
    manifest = load_case(case_dir)
    output = _artifacts_dir(case_dir)

    analysis = "\n\n".join(
        [
            f"# Analysis: {brief.title}",
            brief.summary,
            "## Change",
            brief.change,
            "## Acceptance Criteria",
            _bullets(list(brief.acceptance_criteria)),
            "## Known Risks",
            _bullets(list(brief.known_risks)),
            "## Constraints",
            _bullets(list(brief.constraints)),
            "## Traceable Requirements",
            _table(
                [[item["id"], item["text"]] for item in manifest["requirements"]],
                ["ID", "Requirement"],
            ),
        ]
    )
    algorithm_steps = [
        "Collect JSON evidence from approved test tooling. Keep every file inside this case directory.",
        "Run `qa-case-pipeline verify --case <case-directory>` to evaluate the declared assertions.",
        "Review failed assertions against their requirement and evidence source before changing a test or product.",
        "Perform the manual checks after automated evidence is available and record the actual result.",
        "Run `qa-case-pipeline report --case <case-directory>` to create the final traceability report.",
    ]
    algorithm = "\n\n".join(
        [
            "# Verification Algorithm",
            _bullets(algorithm_steps),
            "## Evidence Sources",
            _table([[name, path] for name, path in manifest["evidence"].items()], ["Name", "Local JSON file"]),
        ]
    )
    automated = "# Automated Checks\n\n" + _table(
        [[item["id"], item["requirement"], item["purpose"], item["source"]] for item in manifest["automated_checks"]],
        ["ID", "Requirement", "Purpose", "Evidence"],
    )
    manual = "# Manual Exploratory Checks\n\n" + _table(
        [[item["id"], item["requirement"], item["purpose"], item["expected"]] for item in manifest["manual_checks"]],
        ["ID", "Requirement", "Purpose", "Expected"],
    )
    (output / "analysis.md").write_text(analysis + "\n", encoding="utf-8")
    (output / "algorithm.md").write_text(algorithm + "\n", encoding="utf-8")
    (output / "automated-checks.md").write_text(automated + "\n", encoding="utf-8")
    (output / "manual-checks.md").write_text(manual + "\n", encoding="utf-8")
    return output


def render_automated_report(case_dir: Path, result: dict[str, Any]) -> Path:
    output = _artifacts_dir(case_dir)
    rows = []
    for check in result["checks"]:
        details = "; ".join(
            f"{item['pointer']} {item['operator']} {item['expected']!r}: {'PASS' if item['passed'] else 'FAIL'}"
            for item in check["assertions"]
        )
        rows.append([check["id"], check["requirement"], "PASS" if check["passed"] else "FAIL", details])
    markdown = "# Automated Evidence Report\n\n" + _table(rows, ["Check", "Requirement", "Status", "Assertions"])
    markdown += "\n\nThis report evaluates local evidence files only. It is not a release decision.\n"
    (output / "automated-report.md").write_text(markdown, encoding="utf-8")
    (output / "automated-report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output / "automated-report.md"


def render_final_report(
    case_dir: Path, automated: dict[str, Any], *, synthetic_demo: bool = False
) -> tuple[Path, bool]:
    manifest = load_case(case_dir)
    manual = load_manual_results(case_dir, manifest)
    output = _artifacts_dir(case_dir)
    automated_by_requirement: dict[str, list[str]] = {}
    for check in automated["checks"]:
        automated_by_requirement.setdefault(check["requirement"], []).append("PASS" if check["passed"] else "FAIL")
    manual_by_requirement: dict[str, list[str]] = {}
    for check in manual:
        manual_by_requirement.setdefault(check["requirement"], []).append(check["status"].upper())

    traceability = []
    for requirement in manifest["requirements"]:
        requirement_id = requirement["id"]
        traceability.append(
            [
                requirement_id,
                requirement["text"],
                ", ".join(automated_by_requirement.get(requirement_id, ["NOT COVERED"])),
                ", ".join(manual_by_requirement.get(requirement_id, ["NOT COVERED"])),
            ]
        )
    manual_passed = all(check["status"] == "passed" for check in manual)
    passed = bool(automated["passed"] and manual_passed)
    if synthetic_demo:
        status = "SYNTHETIC COMPLETED EXAMPLE - NOT A RELEASE DECISION"
    else:
        status = "READY FOR HUMAN RELEASE DECISION" if passed else "INCOMPLETE OR FAILED"
    status_note = (
        "This is a synthetic demonstration. Its completed records show the report format, not real testing."
        if synthetic_demo
        else "This status means the declared evidence and recorded manual checks are complete. It does not replace a product, security, or release decision."
    )
    markdown = "\n\n".join(
        [
            "# QA Case Report",
            f"## Status\n\n**{status}**\n\n{status_note}",
            "## Requirement Traceability\n\n" + _table(traceability, ["ID", "Requirement", "Automated", "Manual"]),
            "## Manual Evidence\n\n" + _table(
                [[item["id"], item["status"], item["evidence"] or "-", item["notes"] or "-"] for item in manual],
                ["Check", "Status", "Evidence", "Notes"],
            ),
        ]
    )
    path = output / "qa-report.md"
    path.write_text(markdown + "\n", encoding="utf-8")
    return path, passed
