"""Backend-onafhankelijk ruimtelijk model voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


@dataclass(frozen=True)
class SpatialRegion:
    id: str
    naam: str
    doel: str
    layout: str
    component: str
    x: int
    y: int
    width: int
    height: int
    bron: Architectuurobject


@dataclass(frozen=True)
class SpatialLayout:
    id: str
    naam: str
    doel: str
    compositie: str
    canvas_width: int
    canvas_height: int
    regions: tuple[SpatialRegion, ...]
    bron: Architectuurobject


def _getal(waarde: object) -> int:
    try:
        return int(str(waarde))
    except (TypeError, ValueError):
        return 0


def bouw_spatial_model(objecten: Iterable[Architectuurobject]) -> tuple[SpatialLayout, ...]:
    objecten = tuple(objecten)
    regio_objecten = [obj for obj in objecten if obj.soort == "regio"]
    layouts = []
    for obj in objecten:
        if obj.soort != "layout":
            continue
        regions = tuple(
            SpatialRegion(
                id=regio.id,
                naam=str(regio.eigenschappen.get("naam", "")),
                doel=str(regio.eigenschappen.get("doel", "")),
                layout=str(regio.eigenschappen.get("layout", "")),
                component=str(regio.eigenschappen.get("component", "")),
                x=_getal(regio.eigenschappen.get("x")),
                y=_getal(regio.eigenschappen.get("y")),
                width=_getal(regio.eigenschappen.get("width")),
                height=_getal(regio.eigenschappen.get("height")),
                bron=regio,
            )
            for regio in regio_objecten
            if regio.eigenschappen.get("layout") == obj.id
        )
        layouts.append(SpatialLayout(
            id=obj.id,
            naam=str(obj.eigenschappen.get("naam", "")),
            doel=str(obj.eigenschappen.get("doel", "")),
            compositie=str(obj.eigenschappen.get("compositie", "")),
            canvas_width=_getal(obj.eigenschappen.get("canvas-width")),
            canvas_height=_getal(obj.eigenschappen.get("canvas-height")),
            regions=regions,
            bron=obj,
        ))
    return tuple(sorted(layouts, key=lambda layout: layout.id))
