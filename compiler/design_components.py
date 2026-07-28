"""Getypeerd component- en appearance-model voor Beckeringh Palace."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.design_tokens import TokenType

TOKEN_REFERENTIE = re.compile(r"^\{(?P<id>[\w.-]+)\}$")

# Legacy padding blijft uitsluitend beschikbaar voor geïsoleerde pre-appearance fixtures.
COMPONENTEIGENSCHAPPEN = {
    "appearance": None,
    "padding": TokenType.DIMENSION,
}
APPEARANCE_EIGENSCHAPPEN = (
    "material",
    "foreground",
    "accent",
    "outline",
    "border",
    "radius",
    "shadow",
    "motion",
    "offset",
    "spacing",
    "heading-style",
    "body-style",
    "label-style",
    "caption-style",
)
APPEARANCE_ROLLEN = {
    "material": frozenset({"canvas", "surface", "raised"}),
    "foreground": frozenset({"foreground", "muted", "disabled"}),
    "accent": frozenset({
        "accent",
        "interaction",
        "interaction-pressed",
        "disabled",
    }),
    "outline": frozenset({
        "accent",
        "outline",
        "interaction",
        "interaction-pressed",
        "disabled",
    }),
    "border": frozenset({"hairline", "regular", "strong"}),
    "radius": frozenset({"small", "medium", "large", "pill"}),
    "shadow": frozenset({"none", "low", "medium", "high", "glow"}),
    "motion": frozenset({"fast", "normal", "slow"}),
    "offset": frozenset({"rest", "hover"}),
    "spacing": frozenset({"none", "xs", "small", "medium", "large", "xl"}),
    "heading-style": frozenset({"display", "title", "heading"}),
    "body-style": frozenset({"body"}),
    "label-style": frozenset({"label"}),
    "caption-style": frozenset({"caption"}),
}


@dataclass(frozen=True)
class ComponentAppearance:
    id: str
    naam: str
    doel: str
    rollen: tuple[tuple[str, str], ...]
    bron: Architectuurobject

    def rol(self, naam: str) -> str | None:
        return next((waarde for sleutel, waarde in self.rollen if sleutel == naam), None)


@dataclass(frozen=True)
class DesignComponent:
    id: str
    naam: str
    doel: str
    appearance: str | None
    eigenschappen: dict[str, str]
    bron: Architectuurobject


def appearance_uit_object(obj: Architectuurobject) -> ComponentAppearance | None:
    if obj.soort != "appearance":
        return None
    rollen = tuple(
        (naam, str(obj.eigenschappen[naam]))
        for naam in APPEARANCE_EIGENSCHAPPEN
        if naam in obj.eigenschappen
    )
    return ComponentAppearance(
        id=obj.id,
        naam=str(obj.eigenschappen.get("naam", "")),
        doel=str(obj.eigenschappen.get("doel", "")),
        rollen=rollen,
        bron=obj,
    )


def component_uit_object(obj: Architectuurobject) -> DesignComponent | None:
    if obj.soort != "component":
        return None
    eigenschappen = {
        naam: waarde
        for naam, waarde in obj.eigenschappen.items()
        if naam in COMPONENTEIGENSCHAPPEN and naam != "appearance" and isinstance(waarde, str)
    }
    appearance = obj.eigenschappen.get("appearance")
    return DesignComponent(
        id=obj.id,
        naam=str(obj.eigenschappen.get("naam", "")),
        doel=str(obj.eigenschappen.get("doel", "")),
        appearance=appearance if isinstance(appearance, str) else None,
        eigenschappen=eigenschappen,
        bron=obj,
    )


def tokenreferentie(waarde: str) -> str | None:
    match = TOKEN_REFERENTIE.match(waarde)
    return match.group("id") if match else None


def verzamel_appearances(
    objecten: Iterable[Architectuurobject],
) -> tuple[ComponentAppearance, ...]:
    appearances = (appearance_uit_object(obj) for obj in objecten)
    return tuple(sorted((item for item in appearances if item is not None), key=lambda item: item.id))


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
