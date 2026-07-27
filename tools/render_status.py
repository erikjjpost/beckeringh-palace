#!/usr/bin/env python3
"""Validate and render the normatieve Beckeringh Palace project status."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "project" / "status.json"
OUTPUT = ROOT / "PROJECT_STATUS.md"


def load_status(path: Path = SOURCE) -> dict[str, Any]:
    status = json.loads(path.read_text(encoding="utf-8"))
    validate_status(status)
    return status


def validate_status(status: dict[str, Any]) -> None:
    if status.get("schema_version") != 1:
        raise ValueError("project/status.json: schema_version moet 1 zijn")

    overall = status.get("overall_progress")
    if not isinstance(overall, int) or not 0 <= overall <= 100:
        raise ValueError("project/status.json: overall_progress moet een geheel percentage zijn")

    areas = status.get("areas")
    if not isinstance(areas, list) or not areas:
        raise ValueError("project/status.json: areas moet ten minste één productgebied bevatten")

    ids: set[str] = set()
    required = {"id", "name", "progress", "evidence", "remaining"}
    for area in areas:
        missing = required - area.keys()
        if missing:
            raise ValueError(
                f"project/status.json: productgebied mist {', '.join(sorted(missing))}"
            )
        if area["id"] in ids:
            raise ValueError(f"project/status.json: dubbel productgebied '{area['id']}'")
        ids.add(area["id"])
        if not isinstance(area["progress"], int) or not 0 <= area["progress"] <= 100:
            raise ValueError(
                f"project/status.json: voortgang voor '{area['id']}' moet een geheel percentage zijn"
            )


def render_status(status: dict[str, Any]) -> str:
    current = status["current_milestone"]
    completed = status["last_completed_milestone"]
    next_step = status["next_step"]
    lines = [
        f"# Projectstatus {status['project']}",
        "",
        "> Dit bestand is gegenereerd uit `project/status.json`. Wijzig de bron en voer "
        "`python tools/bp.py check` uit.",
        "",
        "## Totaalbeeld",
        "",
        f"**Geschatte voortgang: {status['overall_progress']}%**",
        "",
        status["overall_method"],
        "",
        f"- Actuele milestone: **{current['id']} — {current['name']}** ({current['state']})",
        f"- Laatst voltooid: **{completed['id']} — {completed['name']}** "
        f"(PR #{completed['pull_request']})",
        f"- Volgende stap: **{next_step['id']} — {next_step['name']}**",
        "",
        "## Voortgang per productgebied",
        "",
        "| Productgebied | Voortgang | Onderbouwing | Resterend werk |",
        "|---|---:|---|---|",
    ]
    for area in status["areas"]:
        lines.append(
            f"| {area['name']} | {area['progress']}% | {area['evidence']} | "
            f"{area['remaining']} |"
        )
    lines.extend(
        [
            "",
            "## Eerstvolgende stap",
            "",
            f"### {next_step['id']} — {next_step['name']}",
            "",
            next_step["purpose"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUTPUT.write_text(render_status(load_status()), encoding="utf-8")
    print("Gegenereerd:")
    print("  PROJECT_STATUS.md")


if __name__ == "__main__":
    main()
