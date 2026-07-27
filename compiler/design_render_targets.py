"""Getypeerd, backend-onafhankelijk model voor renderdoelen."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


@dataclass(frozen=True)
class ResolvedRenderTarget:
    id: str
    naam: str
    doel: str
    formaat: str
    pad: str


class RenderTargetResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot renderdoelen worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise RenderTargetResolutionError(
            f"Renderdoel '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def resolveer_renderdoelen(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedRenderTarget, ...]:
    renderdoelen = (
        ResolvedRenderTarget(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            formaat=_tekst(obj, "formaat"),
            pad=_tekst(obj, "pad"),
        )
        for obj in objecten
        if obj.soort == "renderdoel"
    )
    return tuple(sorted(renderdoelen, key=lambda renderdoel: renderdoel.id))
