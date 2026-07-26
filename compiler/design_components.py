"""Getypeerd componentmodel voor Beckeringh Palace."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.design_tokens import TokenType

TOKEN_REFERENTIE = re.compile(r"^\{(?P<id>[\w.-]+)\}$")

COMPONENTEIGENSCHAPPEN = {
    "surface": TokenType.COLOR,
    "foreground": TokenType.COLOR,
    "accent": TokenType.COLOR,
    "padding": TokenType.DIMENSION,
    "radius": TokenType.DIMENSION,
}


@dataclass(frozen=True)
class DesignComponent:
    id: str
    naam: str
    doel: str
    eigenschappen: dict[str, str]
    bron: Architectuurobject


def component_uit_object(obj: Architectuurobject) -> DesignComponent | None:
    if obj.soort != "component":
        return None
    eigenschappen = {
        naam: waarde
        for naam, waarde in obj.eigenschappen.items()
        if naam in COMPONENTEIGENSCHAPPEN and isinstance(waarde, str)
    }
    return DesignComponent(
        id=obj.id,
        naam=str(obj.eigenschappen.get("naam", "")),
        doel=str(obj.eigenschappen.get("doel", "")),
        eigenschappen=eigenschappen,
        bron=obj,
    )


def tokenreferentie(waarde: str) -> str | None:
    match = TOKEN_REFERENTIE.match(waarde)
    return match.group("id") if match else None


def verzamel_componenten(
    objecten: Iterable[Architectuurobject],
) -> tuple[DesignComponent, ...]:
    componenten = (component_uit_object(obj) for obj in objecten)
    return tuple(
        sorted(
            (component for component in componenten if component is not None),
            key=lambda component: component.id,
        )
    )
