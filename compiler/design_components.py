"""Getypeerd component- en appearance-model voor Beckeringh Palace."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.design_tokens import TokenType
from compiler.theme_resolution import RADIUS_ROLLEN, SHADOW_ROLLEN

TOKEN_REFERENTIE = re.compile(r"^\{(?P<id>[\w.-]+)\}$")

# Legacy padding blijft uitsluitend beschikbaar voor geïsoleerde pre-appearance fixtures.
COMPONENTEIGENSCHAPPEN = {
    "appearance": None,
    "padding": TokenType.DIMENSION,
    "rol": None,
    "anatomie": None,
    "toegankelijkheid": None,
}
COMPONENT_ANATOMIE_PER_ROL = {
    "paneel": ("titel", "tekst"),
    "actie": ("label",),
    "invoer": ("label", "waarde", "melding"),
    "status": ("label", "waarde"),
    "app-tegel": ("label", "beschrijving", "status"),
    "statistiek": ("label", "waarde", "beschrijving"),
    "terminal": (
        "label",
        "venstertitel",
        "vensterknoppen",
        "tabs",
        "actieve-tab",
        "markering",
        "gebruiker",
        "host",
        "sleutels",
        "waarden",
        "pad",
        "prompt",
        "cursor",
    ),
}
COMPONENT_ROLLEN = frozenset(COMPONENT_ANATOMIE_PER_ROL)
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
    "material": frozenset({
        "canvas",
        "surface",
        "raised",
        "field",
        "transparent",
        "interaction",
        "interaction-hover",
        "interaction-soft",
        "interaction-pressed",
        "accent",
        "accent-hover",
        "success-surface",
        "warning-surface",
        "error-surface",
        "info-surface",
    }),
    "foreground": frozenset({
        "canvas",
        "foreground",
        "muted",
        "disabled",
        "interaction",
        "interaction-hover",
        "interaction-pressed",
        "accent",
        "accent-hover",
        "success-foreground",
        "warning-foreground",
        "error-foreground",
        "info-foreground",
    }),
    "accent": frozenset({
        "accent",
        "accent-hover",
        "interaction",
        "interaction-hover",
        "interaction-pressed",
        "disabled",
        "success",
        "warning",
        "error",
        "info",
    }),
    "outline": frozenset({
        "accent",
        "accent-hover",
        "outline",
        "transparent",
        "interaction",
        "interaction-hover",
        "interaction-pressed",
        "disabled",
        "success",
        "warning",
        "error",
        "info",
    }),
    "border": frozenset({"hairline", "regular", "strong"}),
    "radius": frozenset(RADIUS_ROLLEN),
    "shadow": frozenset(SHADOW_ROLLEN),
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
    rol: str | None
    anatomie: tuple[str, ...]
    accessibility_id: str | None
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
        if (
            naam in COMPONENTEIGENSCHAPPEN
            and naam not in {
                "appearance",
                "rol",
                "anatomie",
                "toegankelijkheid",
            }
            and isinstance(waarde, str)
        )
    }
    appearance = obj.eigenschappen.get("appearance")
    rol = obj.eigenschappen.get("rol")
    anatomie = obj.eigenschappen.get("anatomie")
    accessibility_id = obj.eigenschappen.get("toegankelijkheid")
    return DesignComponent(
        id=obj.id,
        naam=str(obj.eigenschappen.get("naam", "")),
        doel=str(obj.eigenschappen.get("doel", "")),
        appearance=appearance if isinstance(appearance, str) else None,
        rol=rol if isinstance(rol, str) else None,
        anatomie=(
            tuple(str(item) for item in anatomie)
            if isinstance(anatomie, list)
            else ()
        ),
        accessibility_id=(
            accessibility_id if isinstance(accessibility_id, str) else None
        ),
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
