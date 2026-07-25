"""Semantische analyse voor Beckeringh Architectuurtaal."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.diagnostics import Diagnostic


class RelatieVorm(str, Enum):
    ENKELVOUDIG_OF_LIJST = "enkelvoudig_of_lijst"


@dataclass(frozen=True)
class RelatieType:
    naam: str
    vorm: RelatieVorm = RelatieVorm.ENKELVOUDIG_OF_LIJST


RELATIETYPEN = {
    naam: RelatieType(naam)
    for naam in (
        "afhankelijk_van",
        "eigenaar",
        "gebruikt",
        "realiseert",
        "ondersteunt",
    )
}


class SemantischeFout(ValueError):
    """BAT is syntactisch geldig, maar semantisch inconsistent."""

    def __init__(self, diagnostics: Iterable[Diagnostic]):
        self.diagnostics = tuple(diagnostics)
        if not self.diagnostics:
            raise ValueError("SemantischeFout vereist ten minste één diagnostic")
        super().__init__("\n".join(str(diagnostic) for diagnostic in self.diagnostics))


@dataclass(frozen=True)
class SemantischModel:
    """Gevalideerde objecten en hun symbolentabel."""

    objecten: tuple[Architectuurobject, ...]
    symbolen: dict[str, Architectuurobject]


def _referenties(waarde: object) -> tuple[str, ...] | None:
    if isinstance(waarde, str):
        return (waarde,)
    if isinstance(waarde, list) and all(isinstance(item, str) for item in waarde):
        return tuple(waarde)
    return None


def analyseer(objecten: Iterable[Architectuurobject]) -> SemantischModel:
    """Bouw een symbolentabel en verzamel alle semantische diagnostics."""
    vaste_objecten = tuple(objecten)
    symbolen: dict[str, Architectuurobject] = {}
    diagnostics: list[Diagnostic] = []

    for obj in vaste_objecten:
        if obj.id in symbolen:
            diagnostics.append(
                Diagnostic(
                    code="BP2001",
                    boodschap=f"Dubbele object-id: {obj.id}",
                    locatie=obj.bronlocatie,
                )
            )
            continue
        symbolen[obj.id] = obj

    for obj in vaste_objecten:
        for eigenschap, waarde in obj.eigenschappen.items():
            if eigenschap not in RELATIETYPEN:
                continue
            locatie = obj.eigenschaplocaties.get(eigenschap, obj.bronlocatie)
            referenties = _referenties(waarde)
            if referenties is None:
                diagnostics.append(
                    Diagnostic(
                        code="BP2101",
                        boodschap=(
                            "Een relatie moet een object-id of een lijst met "
                            "object-id's bevatten"
                        ),
                        locatie=locatie,
                    )
                )
                continue
            for doel_id in referenties:
                if doel_id not in symbolen:
                    diagnostics.append(
                        Diagnostic(
                            code="BP2102",
                            boodschap=(
                                f"Onbekende referentie '{doel_id}' in "
                                f"{obj.id}.{eigenschap}"
                            ),
                            locatie=locatie,
                        )
                    )

    if diagnostics:
        raise SemantischeFout(diagnostics)

    return SemantischModel(objecten=vaste_objecten, symbolen=symbolen)
