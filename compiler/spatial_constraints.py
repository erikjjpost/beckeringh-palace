"""Semantische constraints voor layouts en regio's."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


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


@dataclass(frozen=True)
class SpatialModelConstraint:
    sleutel: str = "world-model.spatial-model"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        layouts = {obj.id: obj for obj in context.objecten if obj.soort == "layout"}
        composities = {obj.id for obj in context.objecten if obj.soort == "compositie"}
        componenten = {obj.id for obj in context.objecten if obj.soort == "component"}

        for obj in layouts.values():
            toegestaan = {"naam", "doel", "compositie", "canvas-width", "canvas-height"}
            for naam in obj.eigenschappen:
                if naam not in toegestaan:
                    diagnostics.append(Diagnostic("BP3401", f"Layout '{obj.id}' heeft onbekende eigenschap '{naam}'", obj.eigenschaplocaties.get(naam, obj.bronlocatie)))
            compositie = obj.eigenschappen.get("compositie")
            if compositie not in composities:
                diagnostics.append(Diagnostic("BP3402", f"Layout '{obj.id}' verwijst naar onbekende compositie '{compositie}'", obj.eigenschaplocaties.get("compositie", obj.bronlocatie)))
            for veld in ("canvas-width", "canvas-height"):
                if not _positief_geheel_getal(obj.eigenschappen.get(veld)):
                    diagnostics.append(Diagnostic("BP3403", f"Layout '{obj.id}' vereist een positief geheel getal voor '{veld}'", obj.eigenschaplocaties.get(veld, obj.bronlocatie)))

        for obj in context.objecten:
            if obj.soort != "regio":
                continue
            toegestaan = {"naam", "doel", "layout", "component", "x", "y", "width", "height"}
            for naam in obj.eigenschappen:
                if naam not in toegestaan:
                    diagnostics.append(Diagnostic("BP3411", f"Regio '{obj.id}' heeft onbekende eigenschap '{naam}'", obj.eigenschaplocaties.get(naam, obj.bronlocatie)))
            layout_id = obj.eigenschappen.get("layout")
            component_id = obj.eigenschappen.get("component")
            if layout_id not in layouts:
                diagnostics.append(Diagnostic("BP3412", f"Regio '{obj.id}' verwijst naar onbekende layout '{layout_id}'", obj.eigenschaplocaties.get("layout", obj.bronlocatie)))
            if component_id not in componenten:
                diagnostics.append(Diagnostic("BP3413", f"Regio '{obj.id}' verwijst naar onbekend component '{component_id}'", obj.eigenschaplocaties.get("component", obj.bronlocatie)))
            for veld in ("x", "y"):
                if not _niet_negatief_geheel_getal(obj.eigenschappen.get(veld)):
                    diagnostics.append(Diagnostic("BP3414", f"Regio '{obj.id}' vereist een niet-negatief geheel getal voor '{veld}'", obj.eigenschaplocaties.get(veld, obj.bronlocatie)))
            for veld in ("width", "height"):
                if not _positief_geheel_getal(obj.eigenschappen.get(veld)):
                    diagnostics.append(Diagnostic("BP3415", f"Regio '{obj.id}' vereist een positief geheel getal voor '{veld}'", obj.eigenschaplocaties.get(veld, obj.bronlocatie)))
            layout = layouts.get(str(layout_id))
            if layout is not None and all(_niet_negatief_geheel_getal(obj.eigenschappen.get(v)) for v in ("x", "y")) and all(_positief_geheel_getal(obj.eigenschappen.get(v)) for v in ("width", "height")) and all(_positief_geheel_getal(layout.eigenschappen.get(v)) for v in ("canvas-width", "canvas-height")):
                x, y = int(str(obj.eigenschappen["x"])), int(str(obj.eigenschappen["y"]))
                width, height = int(str(obj.eigenschappen["width"])), int(str(obj.eigenschappen["height"]))
                canvas_width = int(str(layout.eigenschappen["canvas-width"]))
                canvas_height = int(str(layout.eigenschappen["canvas-height"]))
                if x + width > canvas_width or y + height > canvas_height:
                    diagnostics.append(Diagnostic("BP3416", f"Regio '{obj.id}' valt buiten canvas van layout '{layout_id}'", obj.bronlocatie))
        return tuple(diagnostics)
