#!/usr/bin/env python3
"""Compileer BAT-bronbestanden naar CIR en productoutput."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from compiler.parser import parseer_bestand
from compiler.figma_plugin_adapter import package_plugin
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.project_status import load_project_status
from compiler.render_target_renderer import render_renderdoelen
from compiler.render_target_renderers import standaard_render_target_registry
from compiler.renderers import naar_json, naar_markdown
from compiler.semantic import analyseer

BRON = ROOT / "architectuur"
UITVOER = ROOT / "output" / "bat"
PRODUCTUITVOER = ROOT / "output" / "products"
PROJECTSTATUS = ROOT / "project" / "status.json"
FIGMA_MANIFEST = PRODUCTUITVOER / "emberforge-master.figma.json"
FIGMA_PLUGIN = PRODUCTUITVOER / "figma-plugin"


def main() -> None:
    objecten = []
    for pad in sorted(BRON.rglob("*.bp")):
        objecten.extend(parseer_bestand(pad))
    model = analyseer(objecten, constraints=WORLD_MODEL_CONSTRAINTS)
    UITVOER.mkdir(parents=True, exist_ok=True)
    PRODUCTUITVOER.mkdir(parents=True, exist_ok=True)
    (UITVOER / "model.cir.json").write_text(naar_json(model.objecten), encoding="utf-8")
    (UITVOER / "architectuur.md").write_text(naar_markdown(model.objecten), encoding="utf-8")
    renderdoelpaden = []
    for artifact in render_renderdoelen(
        model.objecten, standaard_render_target_registry()
    ):
        pad = ROOT / artifact.definitie.pad
        pad.parent.mkdir(parents=True, exist_ok=True)
        pad.write_text(artifact.inhoud, encoding="utf-8")
        renderdoelpaden.append(artifact.definitie.pad)

    productpaden = []
    project_status = load_project_status(PROJECTSTATUS)
    for product in compileer_producten(
        model.objecten,
        standaard_backend_registry(),
        project_status=project_status,
    ):
        pad = ROOT / product.definitie.pad
        pad.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(product.inhoud, bytes):
            pad.write_bytes(product.inhoud)
        else:
            pad.write_text(product.inhoud, encoding="utf-8")
        productpaden.append(product.definitie.pad)

    plugin_code, plugin_manifest = package_plugin(FIGMA_MANIFEST, FIGMA_PLUGIN)
    productpaden.extend((
        str(plugin_code.relative_to(ROOT)),
        str(plugin_manifest.relative_to(ROOT)),
    ))

    print(f"BAT gecompileerd: {len(model.objecten)} object(en)")
    for pad in (
        "output/bat/model.cir.json", "output/bat/architectuur.md",
        *renderdoelpaden,
        *productpaden,
    ):
        print(f"  {pad}")


if __name__ == "__main__":
    main()
