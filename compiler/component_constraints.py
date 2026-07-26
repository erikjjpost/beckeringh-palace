"""Semantische constraints voor Beckeringh Palace-componenten."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.design_components import COMPONENTEIGENSCHAPPEN, tokenreferentie
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class DesignComponentConstraint:
    """Valideer componenteigenschappen en hun getypeerde tokenreferenties."""

    sleutel: str = "world-model.design-components"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        tokens = {obj.id: obj for obj in context.objecten if obj.soort == "token"}

        for obj in context.objecten:
            if obj.soort != "component":
                continue
            for naam, waarde in obj.eigenschappen.items():
                if naam in {"naam", "doel"}:
                    continue
                verwacht_type = COMPONENTEIGENSCHAPPEN.get(naam)
                if verwacht_type is None:
                    diagnostics.append(
                        Diagnostic(
                            code="BP3201",
                            boodschap=f"Component '{obj.id}' heeft onbekende eigenschap '{naam}'",
                            locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                        )
                    )
                    continue
                referentie = tokenreferentie(waarde) if isinstance(waarde, str) else None
                if referentie is None:
                    diagnostics.append(
                        Diagnostic(
                            code="BP3202",
                            boodschap=(
                                f"Component '{obj.id}.{naam}' vereist een tokenreferentie "
                                "in de vorm '{token-id}'"
                            ),
                            locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                        )
                    )
                    continue
                token = tokens.get(referentie)
                if token is None:
                    diagnostics.append(
                        Diagnostic(
                            code="BP3203",
                            boodschap=(
                                f"Component '{obj.id}.{naam}' verwijst naar onbekend token "
                                f"'{referentie}'"
                            ),
                            locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                        )
                    )
                    continue
                werkelijk_type = token.eigenschappen.get("type")
                if werkelijk_type != verwacht_type.value:
                    diagnostics.append(
                        Diagnostic(
                            code="BP3204",
                            boodschap=(
                                f"Component '{obj.id}.{naam}' verwacht token-type "
                                f"'{verwacht_type.value}', maar '{referentie}' is "
                                f"'{werkelijk_type}'"
                            ),
                            locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                        )
                    )
        return tuple(diagnostics)
