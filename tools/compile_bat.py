#!/usr/bin/env python3
"""Compileer BAT-bronbestanden naar CIR en productoutput."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from compiler.component_css_renderer import naar_component_css
from compiler.component_html_renderer import naar_component_html
from compiler.css_renderer import naar_css
from compiler.parser import parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.renderers import naar_json, naar_markdown
from compiler.semantic import analyseer
from compiler.token_json_renderer import naar_token_json

BRON = ROOT / "architectuur"
UITVOER = ROOT / "output" / "bat"
PRODUCTUITVOER = ROOT / "output" / "products"


def main() -> None:
    objecten = []
    for pad in sorted(BRON.rglob("*.bp")):
        objecten.extend(parseer_bestand(pad))
    model = analyseer(objecten, constraints=WORLD_MODEL_CONSTRAINTS)
    UITVOER.mkdir(parents=True, exist_ok=True)
    PRODUCTUITVOER.mkdir(parents=True, exist_ok=True)
    (UITVOER / "model.cir.json").write_text(naar_json(model.objecten), encoding="utf-8")
    (UITVOER / "architectuur.md").write_text(naar_markdown(model.objecten), encoding="utf-8")
    (PRODUCTUITVOER / "tokens.css").write_text(naar_css(model.objecten), encoding="utf-8")
    (PRODUCTUITVOER / "tokens.json").write_text(naar_token_json(model.objecten), encoding="utf-8")
    (PRODUCTUITVOER / "components.css").write_text(naar_component_css(model.objecten), encoding="utf-8")
    (PRODUCTUITVOER / "components.html").write_text(naar_component_html(model.objecten), encoding="utf-8")
    productpaden = []
    for product in compileer_producten(model.objecten, standaard_backend_registry()):
        pad = ROOT / product.definitie.pad
        pad.parent.mkdir(parents=True, exist_ok=True)
        pad.write_text(product.inhoud, encoding="utf-8")
        productpaden.append(product.definitie.pad)

    print(f"BAT gecompileerd: {len(model.objecten)} object(en)")
    for pad in (
        "output/bat/model.cir.json", "output/bat/architectuur.md",
        "output/products/tokens.css", "output/products/tokens.json",
        "output/products/components.css", "output/products/components.html",
        *productpaden,
    ):
        print(f"  {pad}")


if __name__ == "__main__":
    main()
