"""Semantische analyse voor Beckeringh Architectuurtaal."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


RELATIE_EIGENSCHAPPEN = {
    "afhankelijk_van",
    "eigenaar",
    "gebruikt",
    "realiseert",
    "ondersteunt",
}


class SemantischeFout(ValueError):
    """BAT is syntactisch geldig, maar semantisch inconsistent."""


@dataclass(frozen=True)
class SemantischModel:
    """Gevalideerde objecten en hun symbolentabel."""

    objecten: tuple[Architectuurobject, ...]
    symbolen: dict[str, Architectuurobject]


def _referenties(waarde: object) -> tuple[str, ...]:
    if isinstance(waarde, str):
        return (waarde,)
    if isinstance(waarde, list) and all(isinstance(item, str) for item in waarde):
        return tuple(waarde)
    raise SemantischeFout("Een relatie moet een object-id of een lijst met object-id's bevatten")


def analyseer(objecten: Iterable[Architectuurobject]) -> SemantischModel:
    """Bouw een symbolentabel en valideer alle bekende objectreferenties."""
    vaste_objecten = tuple(objecten)
    symbolen: dict[str, Architectuurobject] = {}

    for obj in vaste_objecten:
        if obj.id in symbolen:
            raise SemantischeFout(f"Dubbele object-id: {obj.id}")
        symbolen[obj.id] = obj

    for obj in vaste_objecten:
        for eigenschap, waarde in obj.eigenschappen.items():
            if eigenschap not in RELATIE_EIGENSCHAPPEN:
                continue
            for doel_id in _referenties(waarde):
                if doel_id not in symbolen:
                    raise SemantischeFout(
                        f"Onbekende referentie '{doel_id}' in {obj.id}.{eigenschap}"
                    )

    return SemantischModel(objecten=vaste_objecten, symbolen=symbolen)
