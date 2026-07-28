"""Native, backend-onafhankelijk layoutmodel voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from compiler.cir import Architectuurobject


class LayoutType(str, Enum):
    """De vier native vormen van layoutintentie."""

    GRID = "grid"
    STACK = "stack"
    FLOW = "flow"
    LAYER = "layer"


class LayoutDirection(str, Enum):
    """Backend-onafhankelijke leesrichting voor stack en flow."""

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


@dataclass(frozen=True)
class ResolvedRegion:
    id: str
    naam: str
    doel: str
    layout_id: str
    instance_id: str
    column: int | None = None
    row: int | None = None
    column_span: int | None = None
    row_span: int | None = None
    layer: int | None = None
    compact_order: int | None = None


@dataclass(frozen=True)
class ResolvedLayout:
    id: str
    naam: str
    doel: str
    type: LayoutType
    regions: tuple[ResolvedRegion, ...]
    columns: int | None = None
    rows: int | None = None
    direction: LayoutDirection | None = None
    wrap: bool | None = None
    responsive_breakpoint: int | None = None
    compact_columns: int | None = None


class LayoutResolutionError(ValueError):
    """Een niet-gevalideerde CIR kan niet tot een native layout worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise LayoutResolutionError(
            f"{obj.soort.capitalize()} '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _getal(obj: Architectuurobject, veld: str) -> int:
    try:
        return int(_tekst(obj, veld))
    except ValueError as exc:
        raise LayoutResolutionError(
            f"{obj.soort.capitalize()} '{obj.id}' vereist een geheel getal voor '{veld}'"
        ) from exc


def _optioneel_getal(obj: Architectuurobject, veld: str) -> int | None:
    return _getal(obj, veld) if veld in obj.eigenschappen else None


def _region_uit_object(obj: Architectuurobject) -> ResolvedRegion:
    instance_id = _tekst(obj, "instantie")
    return ResolvedRegion(
        id=obj.id,
        naam=_tekst(obj, "naam"),
        doel=_tekst(obj, "doel"),
        layout_id=_tekst(obj, "layout"),
        instance_id=instance_id,
        column=_optioneel_getal(obj, "column"),
        row=_optioneel_getal(obj, "row"),
        column_span=_optioneel_getal(obj, "column-span"),
        row_span=_optioneel_getal(obj, "row-span"),
        layer=_optioneel_getal(obj, "layer"),
        compact_order=_optioneel_getal(obj, "compact-order"),
    )


def resolveer_layouts(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedLayout, ...]:
    """Los gevalideerde native layouts deterministisch op vanuit de CIR."""

    objecten = tuple(objecten)
    regions = {
        obj.id: obj
        for obj in objecten
        if obj.soort == "region"
    }
    layouts = []
    for obj in objecten:
        if obj.soort != "layout" or "type" not in obj.eigenschappen:
            continue
        try:
            layout_type = LayoutType(_tekst(obj, "type"))
            region_ids = obj.eigenschappen.get("regions")
            if not isinstance(region_ids, list):
                raise LayoutResolutionError(
                    f"Layout '{obj.id}' vereist lijstveld 'regions'"
                )
            resolved_regions = tuple(
                _region_uit_object(regions[region_id])
                for region_id in region_ids
            )
            direction = (
                LayoutDirection(_tekst(obj, "direction"))
                if "direction" in obj.eigenschappen
                else None
            )
            wrap = (
                {"true": True, "false": False}[_tekst(obj, "wrap")]
                if "wrap" in obj.eigenschappen
                else None
            )
        except (KeyError, ValueError) as exc:
            raise LayoutResolutionError(
                f"Layout '{obj.id}' bevat onoplosbare layoutsemantiek"
            ) from exc
        layouts.append(
            ResolvedLayout(
                id=obj.id,
                naam=_tekst(obj, "naam"),
                doel=_tekst(obj, "doel"),
                type=layout_type,
                regions=resolved_regions,
                columns=_optioneel_getal(obj, "columns"),
                rows=_optioneel_getal(obj, "rows"),
                direction=direction,
                wrap=wrap,
                responsive_breakpoint=_optioneel_getal(
                    obj, "responsive-breakpoint"
                ),
                compact_columns=_optioneel_getal(obj, "compact-columns"),
            )
        )
    return tuple(sorted(layouts, key=lambda layout: layout.id))
