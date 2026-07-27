"""Getypeerd, backend-onafhankelijk model voor componentvarianten."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


@dataclass(frozen=True)
class ResolvedComponentVariant:
    id: str
    naam: str
    doel: str
    component_id: str
    appearance_id: str


class VariantResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot componentvarianten worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise VariantResolutionError(
            f"Variant '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def resolveer_varianten(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedComponentVariant, ...]:
    varianten = (
        ResolvedComponentVariant(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            component_id=_tekst(obj, "component"),
            appearance_id=_tekst(obj, "appearance"),
        )
        for obj in objecten
        if obj.soort == "variant"
    )
    return tuple(sorted(varianten, key=lambda variant: variant.id))
