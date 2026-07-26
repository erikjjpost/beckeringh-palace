"""Getypeerd design-tokenmodel voor Beckeringh Palace."""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from compiler.cir import Architectuurobject


class TokenType(str, Enum):
    COLOR = "color"
    DIMENSION = "dimension"
    FONT_FAMILY = "font-family"
    NUMBER = "number"
    STRING = "string"


TOKEN_REFERENTIE = re.compile(r"^\{(?P<id>[\w.-]+)\}$")
KLEUR = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")
DIMENSIE = re.compile(r"^-?(?:\d+(?:\.\d+)?|\.\d+)(?:px|rem|em|%|vh|vw)$")
GETAL = re.compile(r"^-?(?:\d+(?:\.\d+)?|\.\d+)$")


@dataclass(frozen=True)
class DesignToken:
    id: str
    naam: str
    doel: str
    type: TokenType
    waarde: str
    bron: Architectuurobject

    @property
    def referentie(self) -> str | None:
        match = TOKEN_REFERENTIE.match(self.waarde)
        return match.group("id") if match else None


def token_uit_object(obj: Architectuurobject) -> DesignToken | None:
    if obj.soort != "token":
        return None
    eigenschappen = obj.eigenschappen
    try:
        token_type = TokenType(str(eigenschappen["type"]))
    except (KeyError, ValueError):
        return None
    waarde = eigenschappen.get("waarde")
    if not isinstance(waarde, str):
        return None
    return DesignToken(
        id=obj.id,
        naam=str(eigenschappen.get("naam", "")),
        doel=str(eigenschappen.get("doel", "")),
        type=token_type,
        waarde=waarde,
        bron=obj,
    )


def verzamel_tokens(objecten: Iterable[Architectuurobject]) -> tuple[DesignToken, ...]:
    tokens = (token_uit_object(obj) for obj in objecten)
    return tuple(sorted((token for token in tokens if token is not None), key=lambda token: token.id))


def waarde_past_bij_type(token_type: TokenType, waarde: str) -> bool:
    if TOKEN_REFERENTIE.match(waarde):
        return True
    if token_type is TokenType.COLOR:
        return bool(KLEUR.match(waarde))
    if token_type is TokenType.DIMENSION:
        return bool(DIMENSIE.match(waarde))
    if token_type is TokenType.NUMBER:
        return bool(GETAL.match(waarde))
    return bool(waarde.strip())
