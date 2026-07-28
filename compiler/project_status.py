"""Getypeerde, gevalideerde projectstatus voor productcompilatie."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MilestoneStatus:
    id: str
    name: str
    state: str = ""
    pull_request: int | None = None


@dataclass(frozen=True)
class NextStep:
    id: str
    name: str
    purpose: str


@dataclass(frozen=True)
class ProductAreaStatus:
    id: str
    name: str
    progress: int
    weight: int
    evidence: str
    remaining: str


@dataclass(frozen=True)
class ProjectStatus:
    schema_version: int
    project: str
    overall_progress: int
    overall_method: str
    current_milestone: MilestoneStatus
    last_completed_milestone: MilestoneStatus
    next_step: NextStep
    areas: tuple[ProductAreaStatus, ...]


def _required_text(mapping: dict[str, Any], key: str, context: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context}: '{key}' moet niet-lege tekst zijn")
    return value


def validate_project_status(status: dict[str, Any]) -> None:
    context = "project/status.json"
    if status.get("schema_version") != 1:
        raise ValueError(f"{context}: schema_version moet 1 zijn")

    for key in ("project", "overall_method"):
        _required_text(status, key, context)

    if "overall_progress" in status:
        raise ValueError(
            f"{context}: overall_progress wordt berekend en mag niet worden opgeslagen"
        )

    current = status.get("current_milestone")
    completed = status.get("last_completed_milestone")
    next_step = status.get("next_step")
    if not isinstance(current, dict):
        raise ValueError(f"{context}: current_milestone moet een object zijn")
    if not isinstance(completed, dict):
        raise ValueError(f"{context}: last_completed_milestone moet een object zijn")
    if not isinstance(next_step, dict):
        raise ValueError(f"{context}: next_step moet een object zijn")
    for key in ("id", "name", "state"):
        _required_text(current, key, f"{context}: current_milestone")
    for key in ("id", "name"):
        _required_text(completed, key, f"{context}: last_completed_milestone")
    pull_request = completed.get("pull_request")
    if not isinstance(pull_request, int) or pull_request < 1:
        raise ValueError(
            f"{context}: last_completed_milestone.pull_request moet positief zijn"
        )
    for key in ("id", "name", "purpose"):
        _required_text(next_step, key, f"{context}: next_step")

    areas = status.get("areas")
    if not isinstance(areas, list) or not areas:
        raise ValueError(f"{context}: areas moet ten minste één productgebied bevatten")

    ids: set[str] = set()
    required = {"id", "name", "progress", "weight", "evidence", "remaining"}
    total_weight = 0
    for area in areas:
        if not isinstance(area, dict):
            raise ValueError(f"{context}: ieder productgebied moet een object zijn")
        missing = required - area.keys()
        if missing:
            raise ValueError(
                f"{context}: productgebied mist {', '.join(sorted(missing))}"
            )
        area_id = _required_text(area, "id", f"{context}: productgebied")
        for key in ("name", "evidence", "remaining"):
            _required_text(area, key, f"{context}: productgebied '{area_id}'")
        if area_id in ids:
            raise ValueError(f"{context}: dubbel productgebied '{area_id}'")
        ids.add(area_id)
        progress = area["progress"]
        if not isinstance(progress, int) or not 0 <= progress <= 100:
            raise ValueError(
                f"{context}: voortgang voor '{area_id}' moet een geheel percentage zijn"
            )
        weight = area["weight"]
        if not isinstance(weight, int) or not 0 < weight <= 100:
            raise ValueError(
                f"{context}: gewicht voor '{area_id}' moet een positief geheel percentage zijn"
            )
        total_weight += weight
    if total_weight != 100:
        raise ValueError(
            f"{context}: gewichten van productgebieden moeten samen 100 zijn"
        )


def calculate_overall_progress(status: dict[str, Any]) -> int:
    validate_project_status(status)
    weighted = sum(
        area["progress"] * area["weight"] for area in status["areas"]
    )
    return (weighted + 50) // 100


def project_status_from_dict(status: dict[str, Any]) -> ProjectStatus:
    validate_project_status(status)
    current = status["current_milestone"]
    completed = status["last_completed_milestone"]
    next_step = status["next_step"]
    return ProjectStatus(
        schema_version=status["schema_version"],
        project=status["project"],
        overall_progress=calculate_overall_progress(status),
        overall_method=status["overall_method"],
        current_milestone=MilestoneStatus(
            id=current["id"],
            name=current["name"],
            state=current["state"],
        ),
        last_completed_milestone=MilestoneStatus(
            id=completed["id"],
            name=completed["name"],
            pull_request=completed["pull_request"],
        ),
        next_step=NextStep(
            id=next_step["id"],
            name=next_step["name"],
            purpose=next_step["purpose"],
        ),
        areas=tuple(
            ProductAreaStatus(
                id=area["id"],
                name=area["name"],
                progress=area["progress"],
                weight=area["weight"],
                evidence=area["evidence"],
                remaining=area["remaining"],
            )
            for area in status["areas"]
        ),
    )


def load_project_status(path: Path) -> ProjectStatus:
    return project_status_from_dict(json.loads(path.read_text(encoding="utf-8")))
