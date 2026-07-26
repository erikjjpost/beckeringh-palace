"""Semantische constraints voor Beckeringh Palace-componenten en appearances."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.design_components import (
    APPEARANCE_EIGENSCHAPPEN,
    APPEARANCE_ROLLEN,
    COMPONENTEIGENSCHAPPEN,
    tokenreferentie,
)
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class DesignComponentConstraint:
    """Valideer appearance-contracten en resterende getypeerde tokenreferenties."""

    sleutel: str = "world-model.design-components"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        tokens = {obj.id: obj for obj in context.objecten if obj.soort == "token"}
        appearances = {obj.id: obj for obj in context.objecten if obj.soort == "appearance"}

        for appearance in appearances.values():
            for naam, waarde in appearance.eigenschappen.items():
                if naam in {"naam", "doel"}:
                    continue
                if naam not in APPEARANCE_EIGENSCHAPPEN:
                    diagnostics.append(Diagnostic(
                        code="BP3210",
                        boodschap=f"Appearance '{appearance.id}' heeft onbekende eigenschap '{naam}'",
                        locatie=appearance.eigenschaplocaties.get(naam, appearance.bronlocatie),
                    ))
                    continue
                if waarde not in APPEARANCE_ROLLEN[naam]:
                    diagnostics.append(Diagnostic(
                        code="BP3211",
                        boodschap=f"Appearance '{appearance.id}.{naam}' heeft onbekende semantische rol '{waarde}'",
                        locatie=appearance.eigenschaplocaties.get(naam, appearance.bronlocatie),
                    ))
            for naam in APPEARANCE_EIGENSCHAPPEN:
                if naam not in appearance.eigenschappen:
                    diagnostics.append(Diagnostic(
                        code="BP3212",
                        boodschap=f"Appearance '{appearance.id}' vereist rol '{naam}'",
                        locatie=appearance.bronlocatie,
                    ))

        for obj in context.objecten:
            if obj.soort != "component":
                continue
            for naam, waarde in obj.eigenschappen.items():
                if naam in {"naam", "doel"}:
                    continue
                if naam not in COMPONENTEIGENSCHAPPEN:
                    diagnostics.append(Diagnostic(
                        code="BP3201",
                        boodschap=f"Component '{obj.id}' heeft onbekende eigenschap '{naam}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))
                    continue
                if naam == "appearance":
                    if not isinstance(waarde, str) or waarde not in appearances:
                        diagnostics.append(Diagnostic(
                            code="BP3205",
                            boodschap=f"Component '{obj.id}' verwijst naar onbekende appearance '{waarde}'",
                            locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                        ))
                    continue
                verwacht_type = COMPONENTEIGENSCHAPPEN[naam]
                referentie = tokenreferentie(waarde) if isinstance(waarde, str) else None
                if referentie is None:
                    diagnostics.append(Diagnostic(
                        code="BP3202",
                        boodschap=f"Component '{obj.id}.{naam}' vereist een tokenreferentie in de vorm '{{token-id}}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))
                    continue
                token = tokens.get(referentie)
                if token is None:
                    diagnostics.append(Diagnostic(
                        code="BP3203",
                        boodschap=f"Component '{obj.id}.{naam}' verwijst naar onbekend token '{referentie}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))
                    continue
                werkelijk_type = token.eigenschappen.get("type")
                if werkelijk_type != verwacht_type.value:
                    diagnostics.append(Diagnostic(
                        code="BP3204",
                        boodschap=f"Component '{obj.id}.{naam}' verwacht token-type '{verwacht_type.value}', maar '{referentie}' is '{werkelijk_type}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))
            if "appearance" not in obj.eigenschappen:
                diagnostics.append(Diagnostic(
                    code="BP3206",
                    boodschap=f"Component '{obj.id}' vereist een expliciete appearance",
                    locatie=obj.bronlocatie,
                ))
        return tuple(diagnostics)
