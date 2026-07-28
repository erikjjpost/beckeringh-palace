"""Semantische validatie voor native layouts en regions."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.layout_model import LayoutDirection, LayoutType


LAYOUT_COMMON_FIELDS = frozenset({
    "naam", "doel", "type", "regions", "responsive-breakpoint", "compact-columns"
})
LAYOUT_TYPE_FIELDS = {
    LayoutType.GRID: frozenset({"columns", "rows"}),
    LayoutType.STACK: frozenset({"direction"}),
    LayoutType.FLOW: frozenset({"direction", "wrap"}),
    LayoutType.LAYER: frozenset(),
}
REGION_COMMON_FIELDS = frozenset({
    "naam", "doel", "layout", "instantie", "compact-order"
})
REGION_TYPE_FIELDS = {
    LayoutType.GRID: frozenset({"column", "row", "column-span", "row-span"}),
    LayoutType.STACK: frozenset(),
    LayoutType.FLOW: frozenset(),
    LayoutType.LAYER: frozenset({"layer"}),
}


def _positief_geheel_getal(waarde: object) -> bool:
    try:
        return int(str(waarde)) > 0
    except (TypeError, ValueError):
        return False


def _niet_negatief_geheel_getal(waarde: object) -> bool:
    try:
        return int(str(waarde)) >= 0
    except (TypeError, ValueError):
        return False


def _lijst_met_unieke_ids(waarde: object) -> bool:
    return (
        isinstance(waarde, list)
        and all(isinstance(item, str) and bool(item.strip()) for item in waarde)
        and len(waarde) == len(set(waarde))
    )


@dataclass(frozen=True)
class NativeLayoutConstraint:
    sleutel: str = "world-model.native-layouts"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        layouts = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "layout"
        }
        regions = {obj.id: obj for obj in context.objecten if obj.soort == "region"}
        instanties = {
            obj.id
            for obj in context.objecten
            if obj.soort == "componentinstantie"
        }

        for obj in layouts.values():
            type_waarde = obj.eigenschappen.get("type")
            try:
                layout_type = LayoutType(str(type_waarde))
            except ValueError:
                diagnostics.append(Diagnostic(
                    "BP3601",
                    f"Layout '{obj.id}' heeft onbekend type '{type_waarde}'",
                    locatie=obj.eigenschaplocaties.get("type", obj.bronlocatie),
                ))
                continue

            toegestane_velden = LAYOUT_COMMON_FIELDS | LAYOUT_TYPE_FIELDS[layout_type]
            for naam in obj.eigenschappen:
                if naam not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        "BP3602",
                        f"Layout '{obj.id}' van type '{layout_type.value}' heeft onbekende eigenschap '{naam}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))

            region_ids = obj.eigenschappen.get("regions")
            if not _lijst_met_unieke_ids(region_ids):
                diagnostics.append(Diagnostic(
                    "BP3603",
                    f"Layout '{obj.id}' vereist een expliciete lijst met unieke region-id's",
                    locatie=obj.eigenschaplocaties.get("regions", obj.bronlocatie),
                ))
                region_ids = []

            for region_id in region_ids:
                region = regions.get(region_id)
                if region is None:
                    diagnostics.append(Diagnostic(
                        "BP3604",
                        f"Layout '{obj.id}' verwijst naar onbekende region '{region_id}'",
                        locatie=obj.eigenschaplocaties.get("regions", obj.bronlocatie),
                    ))
                elif region.eigenschappen.get("layout") != obj.id:
                    diagnostics.append(Diagnostic(
                        "BP3605",
                        f"Region '{region_id}' verwijst niet terug naar layout '{obj.id}'",
                        locatie=region.eigenschaplocaties.get("layout", region.bronlocatie),
                    ))
            geplaatste_instanties = [
                regions[region_id].eigenschappen.get("instantie")
                for region_id in region_ids
                if region_id in regions
            ]
            geldige_geplaatste_instanties = [
                instance_id
                for instance_id in geplaatste_instanties
                if isinstance(instance_id, str)
            ]
            if len(geldige_geplaatste_instanties) != len(
                set(geldige_geplaatste_instanties)
            ):
                diagnostics.append(Diagnostic(
                    "BP3609",
                    f"Layout '{obj.id}' plaatst een componentinstantie meer dan één keer",
                    locatie=obj.eigenschaplocaties.get("regions", obj.bronlocatie),
                ))

            if layout_type is LayoutType.GRID:
                for veld in ("columns", "rows"):
                    if not _positief_geheel_getal(obj.eigenschappen.get(veld)):
                        diagnostics.append(Diagnostic(
                            "BP3606",
                            f"Grid-layout '{obj.id}' vereist een positief geheel getal voor '{veld}'",
                            locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                        ))
                responsive_fields = (
                    "responsive-breakpoint" in obj.eigenschappen,
                    "compact-columns" in obj.eigenschappen,
                )
                if any(responsive_fields) and not all(responsive_fields):
                    diagnostics.append(Diagnostic(
                        "BP3618",
                        f"Grid-layout '{obj.id}' vereist zowel 'responsive-breakpoint' als 'compact-columns'",
                        locatie=obj.bronlocatie,
                    ))
                for veld in ("responsive-breakpoint", "compact-columns"):
                    if (
                        veld in obj.eigenschappen
                        and not _positief_geheel_getal(obj.eigenschappen.get(veld))
                    ):
                        diagnostics.append(Diagnostic(
                            "BP3619",
                            f"Grid-layout '{obj.id}' vereist een positief geheel getal voor '{veld}'",
                            locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                        ))
                if (
                    _positief_geheel_getal(obj.eigenschappen.get("compact-columns"))
                    and _positief_geheel_getal(obj.eigenschappen.get("columns"))
                    and int(str(obj.eigenschappen["compact-columns"]))
                    > int(str(obj.eigenschappen["columns"]))
                ):
                    diagnostics.append(Diagnostic(
                        "BP3620",
                        f"Grid-layout '{obj.id}' kan compact niet meer kolommen hebben dan breed",
                        locatie=obj.eigenschaplocaties.get(
                            "compact-columns", obj.bronlocatie
                        ),
                    ))
            elif layout_type in (LayoutType.STACK, LayoutType.FLOW):
                direction = obj.eigenschappen.get("direction")
                if direction not in {item.value for item in LayoutDirection}:
                    diagnostics.append(Diagnostic(
                        "BP3607",
                        f"Layout '{obj.id}' vereist direction 'horizontal' of 'vertical'",
                        locatie=obj.eigenschaplocaties.get("direction", obj.bronlocatie),
                    ))
            if (
                layout_type is LayoutType.FLOW
                and obj.eigenschappen.get("wrap") not in {"true", "false"}
            ):
                diagnostics.append(Diagnostic(
                    "BP3608",
                    f"Flow-layout '{obj.id}' vereist expliciet wrap 'true' of 'false'",
                    locatie=obj.eigenschaplocaties.get("wrap", obj.bronlocatie),
                ))

        for obj in regions.values():
            layout_id = obj.eigenschappen.get("layout")
            layout = layouts.get(str(layout_id))
            if layout is None:
                diagnostics.append(Diagnostic(
                    "BP3611",
                    f"Region '{obj.id}' verwijst naar onbekende native layout '{layout_id}'",
                    locatie=obj.eigenschaplocaties.get("layout", obj.bronlocatie),
                ))
                continue
            if obj.id not in (layout.eigenschappen.get("regions") or []):
                diagnostics.append(Diagnostic(
                    "BP3612",
                    f"Native layout '{layout.id}' noemt region '{obj.id}' niet in 'regions'",
                    locatie=obj.bronlocatie,
                ))

            instance_id = obj.eigenschappen.get("instantie")
            if not isinstance(instance_id, str) or instance_id not in instanties:
                diagnostics.append(Diagnostic(
                    "BP3613",
                    f"Region '{obj.id}' verwijst naar onbekende componentinstantie '{instance_id}'",
                    locatie=obj.eigenschaplocaties.get("instantie", obj.bronlocatie),
                ))

            try:
                layout_type = LayoutType(str(layout.eigenschappen.get("type")))
            except ValueError:
                continue
            toegestane_velden = REGION_COMMON_FIELDS | REGION_TYPE_FIELDS[layout_type]
            for naam in obj.eigenschappen:
                if naam not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        "BP3614",
                        f"Region '{obj.id}' in '{layout_type.value}' heeft onbekende eigenschap '{naam}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))

            typevelden = REGION_TYPE_FIELDS[layout_type]
            for veld in typevelden:
                waarde = obj.eigenschappen.get(veld)
                geldig = (
                    _niet_negatief_geheel_getal(waarde)
                    if veld == "layer"
                    else _positief_geheel_getal(waarde)
                )
                if not geldig:
                    diagnostics.append(Diagnostic(
                        "BP3615",
                        f"Region '{obj.id}' vereist een geldig geheel getal voor '{veld}'",
                        locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                    ))

            if layout_type is LayoutType.GRID:
                compact_order = obj.eigenschappen.get("compact-order")
                if (
                    "responsive-breakpoint" in layout.eigenschappen
                    and not _positief_geheel_getal(compact_order)
                ):
                    diagnostics.append(Diagnostic(
                        "BP3621",
                        f"Region '{obj.id}' vereist een positieve gehele 'compact-order'",
                        locatie=obj.eigenschaplocaties.get(
                            "compact-order", obj.bronlocatie
                        ),
                    ))
                if (
                    _positief_geheel_getal(obj.eigenschappen.get("column"))
                    and _positief_geheel_getal(obj.eigenschappen.get("column-span"))
                    and _positief_geheel_getal(layout.eigenschappen.get("columns"))
                    and int(str(obj.eigenschappen["column"]))
                    + int(str(obj.eigenschappen["column-span"]))
                    - 1
                    > int(str(layout.eigenschappen["columns"]))
                ):
                    diagnostics.append(Diagnostic(
                        "BP3616",
                        f"Region '{obj.id}' valt buiten de kolommen van grid-layout '{layout.id}'",
                        locatie=obj.bronlocatie,
                    ))
                if (
                    _positief_geheel_getal(obj.eigenschappen.get("row"))
                    and _positief_geheel_getal(obj.eigenschappen.get("row-span"))
                    and _positief_geheel_getal(layout.eigenschappen.get("rows"))
                    and int(str(obj.eigenschappen["row"]))
                    + int(str(obj.eigenschappen["row-span"]))
                    - 1
                    > int(str(layout.eigenschappen["rows"]))
                ):
                    diagnostics.append(Diagnostic(
                        "BP3617",
                        f"Region '{obj.id}' valt buiten de rijen van grid-layout '{layout.id}'",
                        locatie=obj.bronlocatie,
                    ))
        for layout in layouts.values():
            if "responsive-breakpoint" not in layout.eigenschappen:
                continue
            region_ids = layout.eigenschappen.get("regions") or []
            orders = [
                regions[region_id].eigenschappen.get("compact-order")
                for region_id in region_ids
                if region_id in regions
            ]
            if (
                all(_positief_geheel_getal(order) for order in orders)
                and sorted(int(str(order)) for order in orders)
                != list(range(1, len(region_ids) + 1))
            ):
                diagnostics.append(Diagnostic(
                    "BP3622",
                    f"Layout '{layout.id}' vereist een aaneengesloten compacte volgorde",
                    locatie=layout.bronlocatie,
                ))
        return tuple(diagnostics)
