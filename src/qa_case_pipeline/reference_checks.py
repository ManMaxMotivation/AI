"""Deterministic checks for bundled, fully synthetic QA cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"id": check_id, "passed": passed, "detail": detail}


def _ui_state_persistence(data: dict[str, Any], expected: dict[str, Any]) -> list[dict[str, Any]]:
    initial = data["initial_state"]
    after = data["after_navigation"]
    control_initial = data["control_initial"]
    control_after = data["control_after_navigation"]
    fields = expected["preserved_filters"]
    results = [
        _result(
            "destination-is-correct",
            after.get("catalog") == expected["expected_catalog"],
            "The target catalog matches the expected navigation destination.",
        )
    ]
    for field in fields:
        results.append(
            _result(
                f"preserve-{field}",
                initial["filters"].get(field) == after["filters"].get(field),
                f"Filter '{field}' is preserved after navigation.",
            )
        )
    results.append(
        _result(
            "url-query-matches-state",
            all(after["url_query"].get(field) == after["filters"].get(field) for field in fields),
            "The URL query mirrors the destination filter state.",
        )
    )
    results.append(
        _result(
            "control-regression",
            control_after.get("catalog") == expected["control_catalog"]
            and all(control_initial["filters"].get(field) == control_after["filters"].get(field) for field in fields),
            "The neighboring control flow preserves the same filter contract.",
        )
    )
    return results


def _platform_visible(key: dict[str, Any] | None, platform_types: set[str]) -> bool:
    if not key or not key.get("type"):
        return True
    return key["type"] in platform_types


def _schema_legacy_compat(data: dict[str, Any], expected: dict[str, Any]) -> list[dict[str, Any]]:
    platform_types = set(expected["platform_source_types"])
    results: list[dict[str, Any]] = []
    try:
        legacy_visible = _platform_visible(data["legacy_record"].get("key"), platform_types)
        results.append(_result("legacy-record-is-safe", legacy_visible, "A legacy record without a composite key does not raise an evaluation error."))
    except (AttributeError, KeyError, TypeError):
        results.append(_result("legacy-record-is-safe", False, "Legacy record handling raised an evaluation error."))

    for scenario in data["visibility_scenarios"]:
        visible = _platform_visible(scenario.get("key"), platform_types)
        results.append(
            _result(
                f"visibility-{scenario['id']}",
                visible == scenario["expected_platform_visible"],
                f"Platform field visibility matches scenario '{scenario['id']}'.",
            )
        )

    keys = [json.dumps(record["key"], sort_keys=True) for record in data["new_records"]]
    results.append(
        _result("composite-keys-are-unique", len(keys) == len(set(keys)), "New records have unique composite keys."))
    return results


def run_reference_checks(case_dir: Path) -> dict[str, Any]:
    brief_path = case_dir / "brief.yaml"
    input_path = case_dir / "input.json"
    expected_path = case_dir / "expected.json"
    if not all(path.exists() for path in (brief_path, input_path, expected_path)):
        raise ValueError("Case directory must contain brief.yaml, input.json, and expected.json.")

    import yaml

    brief = yaml.safe_load(brief_path.read_text(encoding="utf-8"))
    data = json.loads(input_path.read_text(encoding="utf-8"))
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    case_type = brief.get("case_type")
    if case_type == "ui_state_persistence":
        checks = _ui_state_persistence(data, expected)
    elif case_type == "schema_legacy_compat":
        checks = _schema_legacy_compat(data, expected)
    else:
        raise ValueError(f"Unsupported reference case type: {case_type!r}.")

    return {
        "case": brief["title"],
        "case_type": case_type,
        "passed": all(check["passed"] for check in checks),
        "checks": checks,
    }
