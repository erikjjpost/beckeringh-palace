"""Semantische regels voor native Beckeringh Palace-productobjecten."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.component_constraints import DesignComponentConstraint
from compiler.constraints import ConstraintContext
from compiler.design_tokens import TokenType, token_uit_object, waarde_past_bij_type
from compiler.diagnostics import Diagnostic
from compiler.world_model import Domeinstatus, objectsoortdefinitie


@dataclass(frozen=True)
class BekendeObjectsoortenConstraint:
    """Weiger objectsoorten zonder expliciete plaats in het World Model."""

    sleutel: str = "world-model.bekende-objectsoorten"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        for obj in context.objecten:
            if objectsoortdefinitie(obj.soort) is None:
                diagnostics.append(
                    Diagnostic(
                        code="BP3001",
                        boodschap=f"Onbekende objectsoort '{obj.soort}'",
                        locatie=obj.bronlocatie,
                    )
                )
        return tuple(diagnostics)


@dataclass(frozen=True)
class NativeVeldenConstraint:
    """Bewaak de minimale vorm van native productobjecten."""

    sleutel: str = "world-model.native-verplichte-velden"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        for obj in context.objecten:
            definitie = objectsoortdefinitie(obj.soort)
            if definitie is None or definitie.status is not Domeinstatus.NATIVE:
                continue
            for veld in ("naam", "doel"):
                waarde = obj.eigenschappen.get(veld)
                if not isinstance(waarde, str) or not waarde.strip():
                    diagnostics.append(
                        Diagnostic(
                            code="BP3002",
                            boodschap=(
                                f"Native object '{obj.id}' van soort '{obj.soort}' "
                                f"vereist tekstveld '{veld}'"
                            ),
                            locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                        )
                    )
        return tuple(diagnostics)


@dataclass(frozen=True)
class DesignTokenConstraint:
    """Valideer type, waarde en referenties van design tokens."""

    sleutel: str = "world-model.design-tokens"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        token_objecten = {obj.id: obj for obj in context.objecten if obj.soort == "token"}

        for obj in token_objecten.values():
            type_waarde = obj.eigenschappen.get("type")
            waarde = obj.eigenschappen.get("waarde")

            if type_waarde not in {token_type.value for token_type in TokenType}:
                diagnostics.append(
                    Diagnostic(
                        code="BP3101",
                        boodschap=f"Token '{obj.id}' heeft onbekend type '{type_waarde}'",
                        locatie=obj.eigenschaplocaties.get("type", obj.bronlocatie),
                    )
                )
                continue
            if not isinstance(waarde, str) or not waarde.strip():
                diagnostics.append(
                    Diagnostic(
                        code="BP3102",
                        boodschap=f"Token '{obj.id}' vereist tekstveld 'waarde'",
                        locatie=obj.eigenschaplocaties.get("waarde", obj.bronlocatie),
                    )
                )
                continue

            token = token_uit_object(obj)
            if token is None:
                continue
            referentie = token.referentie
            if referentie is not None:
                doel = token_objecten.get(referentie)
                if doel is None:
                    diagnostics.append(
                        Diagnostic(
                            code="BP3103",
                            boodschap=f"Token '{obj.id}' verwijst naar onbekend token '{referentie}'",
                            locatie=obj.eigenschaplocaties.get("waarde", obj.bronlocatie),
                        )
                    )
                    continue
                doeltype = doel.eigenschappen.get("type")
                if doeltype != token.type.value:
                    diagnostics.append(
                        Diagnostic(
                            code="BP3104",
                            boodschap=(
                                f"Token '{obj.id}' van type '{token.type.value}' verwijst naar "
                                f"token '{referentie}' van type '{doeltype}'"
                            ),
                            locatie=obj.eigenschaplocaties.get("waarde", obj.bronlocatie),
                        )
                    )
            elif not waarde_past_bij_type(token.type, token.waarde):
                diagnostics.append(
                    Diagnostic(
                        code="BP3105",
                        boodschap=(
                            f"Waarde '{token.waarde}' past niet bij token-type "
                            f"'{token.type.value}'"
                        ),
                        locatie=obj.eigenschaplocaties.get("waarde", obj.bronlocatie),
                    )
                )

        return tuple(diagnostics)


WORLD_MODEL_CONSTRAINTS = (
    BekendeObjectsoortenConstraint(),
    NativeVeldenConstraint(),
    DesignTokenConstraint(),
    DesignComponentConstraint(),
)
