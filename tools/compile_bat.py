#!/usr/bin/env python3
"""Compileer BAT-bronbestanden naar CIR en presentatie-output."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from compiler.parser import parseer_bestand
from compiler.renderers import naar_json, naar_markdown
from compiler.semantic import analyseer

BRON = ROOT / "architectuur"
UITVOER = ROOT / "output" / "bat"


def main() -> None:
    objecten = []
    for pad in sorted(BRON.rglob("*.bp")):
        objecten.extend(parseer_bestand(pad))

    model = analyseer(objecten)

    UITVOER.mkdir(parents=True, exist_ok=True)
    (UITVOER / "model.cir.json").write_text(naar_json(model.objecten), encoding="utf-8")
    (UITVOER / "architectuur.md").write_text(naar_markdown(model.objecten), encoding="utf-8")

    print(f"BAT gecompileerd: {len(model.objecten)} object(en)")
    print("  output/bat/model.cir.json")
    print("  output/bat/architectuur.md")


if __name__ == "__main__":
    main()
