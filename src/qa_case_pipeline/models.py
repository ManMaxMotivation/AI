"""Validation for public, sanitized QA case briefs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class BriefValidationError(ValueError):
    """Raised when a QA brief cannot be used safely by the pipeline."""


@dataclass(frozen=True)
class Brief:
    title: str
    summary: str
    change: str
    acceptance_criteria: tuple[str, ...]
    known_risks: tuple[str, ...]
    constraints: tuple[str, ...]
    case_type: str | None = None

    @classmethod
    def from_mapping(cls, data: Any) -> "Brief":
        if not isinstance(data, dict):
            raise BriefValidationError("Brief must be a YAML mapping.")

        required = ("title", "summary", "change", "acceptance_criteria", "known_risks", "constraints")
        missing = [field for field in required if field not in data]
        if missing:
            raise BriefValidationError(f"Missing required brief fields: {', '.join(missing)}.")

        def text(name: str) -> str:
            value = data[name]
            if not isinstance(value, str) or not value.strip():
                raise BriefValidationError(f"'{name}' must be a non-empty string.")
            return value.strip()

        def text_list(name: str) -> tuple[str, ...]:
            value = data[name]
            if not isinstance(value, list) or not value:
                raise BriefValidationError(f"'{name}' must be a non-empty list of strings.")
            if not all(isinstance(item, str) and item.strip() for item in value):
                raise BriefValidationError(f"'{name}' must contain only non-empty strings.")
            return tuple(item.strip() for item in value)

        case_type = data.get("case_type")
        if case_type is not None and (not isinstance(case_type, str) or not case_type.strip()):
            raise BriefValidationError("'case_type' must be a non-empty string when provided.")

        return cls(
            title=text("title"),
            summary=text("summary"),
            change=text("change"),
            acceptance_criteria=text_list("acceptance_criteria"),
            known_risks=text_list("known_risks"),
            constraints=text_list("constraints"),
            case_type=case_type.strip() if isinstance(case_type, str) else None,
        )

    def as_prompt_data(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "summary": self.summary,
            "change": self.change,
            "acceptance_criteria": list(self.acceptance_criteria),
            "known_risks": list(self.known_risks),
            "constraints": list(self.constraints),
            "case_type": self.case_type,
        }


def load_brief(path: Path) -> Brief:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise BriefValidationError(f"Cannot read brief '{path}': {error}") from error
    except yaml.YAMLError as error:
        raise BriefValidationError(f"Cannot parse YAML brief '{path}': {error}") from error
    return Brief.from_mapping(raw)
