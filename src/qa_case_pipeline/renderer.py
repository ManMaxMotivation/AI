"""Render validated structured QA plans into human-readable artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


HEADINGS = {
    "en": {
        "analysis": "# Analysis",
        "scope": "## Scope",
        "risks": "## Risks and Regression Zones",
        "assumptions": "## Assumptions and Constraints",
        "algorithm": "# Verification Algorithm",
        "steps": "## Steps",
        "evidence": "## Required Evidence",
        "automated": "# Automated Checks",
        "manual": "# Manual Exploratory Checks",
        "limitations": "## Limits of Automation",
    },
    "ru": {
        "analysis": "# Анализ",
        "scope": "## Область проверки",
        "risks": "## Риски и зоны регрессии",
        "assumptions": "## Допущения и ограничения",
        "algorithm": "# Алгоритм проверки",
        "steps": "## Шаги",
        "evidence": "## Требуемые доказательства",
        "automated": "# Автопроверки",
        "manual": "# Ручные исследовательские проверки",
        "limitations": "## Границы автоматизации",
    },
}


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def _checks(items: list[dict[str, str]]) -> str:
    blocks = []
    for item in items:
        blocks.append(f"## {item['id']}: {item['purpose']}\n\n**Expected:** {item['expected']}")
    return "\n\n".join(blocks)


def render_plan(plan: dict[str, Any], output_dir: Path, language: str) -> Path:
    headings = HEADINGS[language]
    output_dir.mkdir(parents=True, exist_ok=True)

    analysis = plan["analysis"]
    analysis_text = "\n\n".join(
        [
            headings["analysis"],
            analysis["summary"],
            headings["scope"],
            _bullets(analysis["scope"]),
            headings["risks"],
            _bullets([f"{risk['risk']}: {risk['mitigation']}" for risk in analysis["risks"]]),
            headings["assumptions"],
            _bullets(plan["assumptions"]),
        ]
    )
    algorithm_text = "\n\n".join(
        [headings["algorithm"], headings["steps"], _bullets(plan["algorithm"]["steps"]), headings["evidence"], _bullets(plan["algorithm"]["evidence"])]
    )
    automated_text = "\n\n".join([headings["automated"], _checks(plan["automated_checks"]), headings["limitations"], _bullets(plan["limitations"])])
    manual_text = "\n\n".join([headings["manual"], _checks(plan["manual_checks"]), headings["limitations"], _bullets(plan["limitations"])])

    (output_dir / "analysis.md").write_text(analysis_text + "\n", encoding="utf-8")
    (output_dir / "algorithm.md").write_text(algorithm_text + "\n", encoding="utf-8")
    (output_dir / "automated-checks.md").write_text(automated_text + "\n", encoding="utf-8")
    (output_dir / "manual-checks.md").write_text(manual_text + "\n", encoding="utf-8")
    (output_dir / "qa-plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output_dir
