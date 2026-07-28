"""Semantische constraints voor Beckeringh Palace-componenten en appearances."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.design_components import (
    APPEARANCE_EIGENSCHAPPEN,
    APPEARANCE_ROLLEN,
    COMPONENT_ANATOMIE_PER_ROL,
    COMPONENT_ROLLEN,
    COMPONENTEIGENSCHAPPEN,
    tokenreferentie,
)
from compiler.diagnostics import Diagnostic

LEGACY_VISUELE_VELDEN = frozenset({"surface", "foreground", "accent", "radius"})


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
                    diagnostics.append(Diagnostic("BP3210", f"Appearance '{appearance.id}' heeft onbekende eigenschap '{naam}'", locatie=appearance.eigenschaplocaties.get(naam, appearance.bronlocatie)))
                    continue
                if waarde not in APPEARANCE_ROLLEN[naam]:
                    diagnostics.append(Diagnostic("BP3211", f"Appearance '{appearance.id}.{naam}' heeft onbekende semantische rol '{waarde}'", locatie=appearance.eigenschaplocaties.get(naam, appearance.bronlocatie)))
            for naam in APPEARANCE_EIGENSCHAPPEN:
                if naam not in appearance.eigenschappen:
                    diagnostics.append(Diagnostic("BP3212", f"Appearance '{appearance.id}' vereist rol '{naam}'", locatie=appearance.bronlocatie))

        for obj in context.objecten:
            if obj.soort != "component":
                continue
            for naam, waarde in obj.eigenschappen.items():
                if naam in {"naam", "doel"}:
                    continue
                if not appearances and naam in LEGACY_VISUELE_VELDEN:
                    continue
                if naam not in COMPONENTEIGENSCHAPPEN:
                    diagnostics.append(Diagnostic("BP3201", f"Component '{obj.id}' heeft onbekende eigenschap '{naam}'", locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie)))
                    continue
                if naam == "appearance":
                    if not isinstance(waarde, str) or waarde not in appearances:
                        diagnostics.append(Diagnostic("BP3205", f"Component '{obj.id}' verwijst naar onbekende appearance '{waarde}'", locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie)))
                    continue
                if naam in {"rol", "anatomie"}:
                    continue
                verwacht_type = COMPONENTEIGENSCHAPPEN[naam]
                referentie = tokenreferentie(waarde) if isinstance(waarde, str) else None
                if referentie is None:
                    diagnostics.append(Diagnostic("BP3202", f"Component '{obj.id}.{naam}' vereist een tokenreferentie in de vorm '{{token-id}}'", locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie)))
                    continue
                token = tokens.get(referentie)
                if token is None:
                    diagnostics.append(Diagnostic("BP3203", f"Component '{obj.id}.{naam}' verwijst naar onbekend token '{referentie}'", locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie)))
                    continue
                werkelijk_type = token.eigenschappen.get("type")
                if werkelijk_type != verwacht_type.value:
                    diagnostics.append(Diagnostic("BP3204", f"Component '{obj.id}.{naam}' verwacht token-type '{verwacht_type.value}', maar '{referentie}' is '{werkelijk_type}'", locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie)))
            if appearances and "appearance" not in obj.eigenschappen:
                diagnostics.append(Diagnostic("BP3206", f"Component '{obj.id}' vereist een expliciete appearance zodra het model appearances bevat", locatie=obj.bronlocatie))
            rol = obj.eigenschappen.get("rol")
            anatomie = obj.eigenschappen.get("anatomie")
            if rol is not None or anatomie is not None:
                if rol not in COMPONENT_ROLLEN:
                    diagnostics.append(Diagnostic(
                        "BP3220",
                        f"Component '{obj.id}' heeft onbekende rol '{rol}'",
                        locatie=obj.eigenschaplocaties.get("rol", obj.bronlocatie),
                    ))
                geldige_anatomie = (
                    isinstance(anatomie, list)
                    and bool(anatomie)
                    and all(
                        isinstance(item, str) and bool(item.strip())
                        for item in anatomie
                    )
                    and len(anatomie) == len(set(anatomie))
                )
                if not geldige_anatomie:
                    diagnostics.append(Diagnostic(
                        "BP3221",
                        (
                            f"Component '{obj.id}' vereist een niet-lege, "
                            "unieke anatomielijst"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "anatomie", obj.bronlocatie
                        ),
                    ))
                elif rol in COMPONENT_ANATOMIE_PER_ROL and tuple(anatomie) != (
                    COMPONENT_ANATOMIE_PER_ROL[rol]
                ):
                    diagnostics.append(Diagnostic(
                        "BP3222",
                        (
                            f"Component '{obj.id}' vereist voor rol '{rol}' "
                            "anatomie "
                            f"{list(COMPONENT_ANATOMIE_PER_ROL[rol])}"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "anatomie", obj.bronlocatie
                        ),
                    ))
        return tuple(diagnostics)
