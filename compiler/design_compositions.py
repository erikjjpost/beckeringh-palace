"""Getypeerd compositiemodel voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject

TOEGESTANE_RICHTINGEN = frozenset({"row", "column"})


@dataclass(frozen=True)
class DesignComposition:
    id: str
    naam: str
    doel: str
    componenten: tuple[str, ...]
    richting: str
    bron: Architectuurobject


def compositie_uit_object(obj: Architectuurobject) -> DesignComposition | None:
    if obj.soort != "compositie":
        return None
    componenten = obj.eigenschappen.get("componenten", [])
    if not isinstance(componenten, list) or not all(isinstance(item, str) for item in componenten):
        componenten = []
    richting = obj.eigenschappen.get("richting", "column")
    return DesignComposition(
        id=obj.id,
        naam=str(obj.eigenschappen.get("naam", "")),
        doel=str(obj.eigenschappen.get("doel", "")),
        componenten=tuple(componenten),
        richting=str(richting),
        bron=obj,
    )


def verzamel_composities(
    objecten: Iterable[Architectuurobject],
) -> tuple[DesignComposition, ...]:
    composities = (compositie_uit_object(obj) for obj in objecten)
    return tuple(sorted(
        (compositie for compositie in composities if compositie is not None),
        key=lambda compositie: compositie.id,
    ))
