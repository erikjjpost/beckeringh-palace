"""Semantische regels voor native Beckeringh Palace-productobjecten."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
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


WORLD_MODEL_CONSTRAINTS = (
    BekendeObjectsoortenConstraint(),
    NativeVeldenConstraint(),
)
