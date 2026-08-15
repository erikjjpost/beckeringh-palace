#!/usr/bin/env python3
"""Validate and render the normatieve Beckeringh Palace project status."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from compiler.project_status import calculate_overall_progress, validate_project_status

SOURCE = ROOT / "project" / "status.json"
OUTPUT = ROOT / "PROJECT_STATUS.md"


def load_status(path: Path = SOURCE) -> dict[str, Any]:
    import json

    status = json.loads(path.read_text(encoding="utf-8"))
    validate_status(status)
    return status


def validate_status(status: dict[str, Any]) -> None:
    validate_project_status(status)


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
        f"**Geschatte voortgang: {calculate_overall_progress(status)}%**",
        "",
        status["overall_method"],
        "",
        f"- Actuele milestone: **{current['id']} — {current['name']}** ({current['state']})",
        f"- Verificatie: **{current['verification']['state']}**"
        + (
            f" ({current['verification']['actor']}, {current['verification']['date']})"
            if current["verification"]["state"] == "geverifieerd"
            else ""
        ),
        f"- Laatst voltooid: **{completed['id']} — {completed['name']}** "
        f"(PR #{completed['pull_request']})",
        f"- Volgende stap: **{next_step['id']} — {next_step['name']}**",
        "",
        "## Voortgang per productgebied",
        "",
        "| Productgebied | Gewicht | Voortgang | Onderbouwing | Resterend werk |",
        "|---|---:|---:|---|---|",
    ]
    for area in status["areas"]:
        lines.append(
            f"| {area['name']} | {area['weight']}% | {area['progress']}% | {area['evidence']} | "
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
