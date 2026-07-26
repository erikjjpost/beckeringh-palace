"""Semantische constraints voor Beckeringh Palace-composities."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.design_compositions import TOEGESTANE_RICHTINGEN
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class DesignCompositionConstraint:
    sleutel: str = "world-model.design-compositions"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        componenten = {obj.id for obj in context.objecten if obj.soort == "component"}
        for obj in context.objecten:
            if obj.soort != "compositie":
                continue
            toegestane_velden = {"naam", "doel", "componenten", "richting"}
            for naam in obj.eigenschappen:
                if naam not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP3301",
                        boodschap=f"Compositie '{obj.id}' heeft onbekende eigenschap '{naam}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))
            waarden = obj.eigenschappen.get("componenten")
            if not isinstance(waarden, list) or not waarden or not all(isinstance(item, str) for item in waarden):
                diagnostics.append(Diagnostic(
                    code="BP3302",
                    boodschap=f"Compositie '{obj.id}' vereist een niet-lege lijst 'componenten'",
                    locatie=obj.eigenschaplocaties.get("componenten", obj.bronlocatie),
                ))
            else:
                for component_id in waarden:
                    if component_id not in componenten:
                        diagnostics.append(Diagnostic(
                            code="BP3303",
                            boodschap=f"Compositie '{obj.id}' verwijst naar onbekend component '{component_id}'",
                            locatie=obj.eigenschaplocaties.get("componenten", obj.bronlocatie),
                        ))
            richting = obj.eigenschappen.get("richting", "column")
            if richting not in TOEGESTANE_RICHTINGEN:
                diagnostics.append(Diagnostic(
                    code="BP3304",
                    boodschap=f"Compositie '{obj.id}' heeft ongeldige richting '{richting}'",
                    locatie=obj.eigenschaplocaties.get("richting", obj.bronlocatie),
                ))
        return tuple(diagnostics)
