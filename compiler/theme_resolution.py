"""Getypeerde resolutie van expliciete Beckeringh Palace-ontwerpwerelden."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


PALET_ROLLEN = (
    "primary", "secondary", "background", "surface", "foreground",
    "accent", "success", "warning", "error",
)
MATERIAAL_ROLLEN = ("canvas", "surface", "raised", "foreground", "accent")


class ThemeResolutionError(ValueError):
    """De gevalideerde objectketen kan niet tot één expliciet thema worden opgelost."""


@dataclass(frozen=True)
class ResolvedColor:
    id: str
    naam: str
    doel: str
    waarde: str


@dataclass(frozen=True)
class ResolvedPalette:
    id: str
    naam: str
    doel: str
    kleuren: tuple[tuple[str, ResolvedColor], ...]

    def kleur(self, rol: str) -> ResolvedColor | None:
        return next((kleur for naam, kleur in self.kleuren if naam == rol), None)


@dataclass(frozen=True)
class ResolvedTypography:
    id: str
    naam: str
    doel: str
    heading: str
    body: str
    mono: str


@dataclass(frozen=True)
class ResolvedMaterial:
    id: str
    naam: str
    doel: str
    kleuren: tuple[tuple[str, ResolvedColor], ...]

    def kleur(self, rol: str) -> ResolvedColor | None:
        return next((kleur for naam, kleur in self.kleuren if naam == rol), None)


@dataclass(frozen=True)
class ResolvedBorder:
    id: str
    naam: str
    doel: str
    hairline: str
    regular: str
    strong: str
    style: str


@dataclass(frozen=True)
class ResolvedRadius:
    id: str
    naam: str
    doel: str
    small: str
    medium: str
    large: str
    pill: str


@dataclass(frozen=True)
class ResolvedShadow:
    id: str
    naam: str
    doel: str
    low: str
    medium: str
    high: str


@dataclass(frozen=True)
class ResolvedMotion:
    id: str
    naam: str
    doel: str
    fast: str
    normal: str
    slow: str
    easing: str


@dataclass(frozen=True)
class ResolvedTheme:
    wereld_id: str
    wereld_naam: str
    wereld_doel: str
    thema_id: str
    thema_naam: str
    thema_doel: str
    palet: ResolvedPalette
    typografie: ResolvedTypography
    materiaal: ResolvedMaterial
    border: ResolvedBorder
    radius: ResolvedRadius
    shadow: ResolvedShadow
    motion: ResolvedMotion


def _indexeer(objecten: Iterable[Architectuurobject]) -> dict[str, dict[str, Architectuurobject]]:
    index: dict[str, dict[str, Architectuurobject]] = {}
    for obj in objecten:
        index.setdefault(obj.soort, {})[obj.id] = obj
    return index


def _vereis(index, soort: str, object_id: str, context: str) -> Architectuurobject:
    try:
        return index[soort][object_id]
    except KeyError as exc:
        raise ThemeResolutionError(
            f"{context} verwijst naar ontbrekende {soort} '{object_id}'"
        ) from exc


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise ThemeResolutionError(
            f"{obj.soort.capitalize()} '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _resolved_color(index, kleur_id: str, context: str) -> ResolvedColor:
    kleur = _vereis(index, "kleur", kleur_id, context)
    return ResolvedColor(
        id=kleur.id,
        naam=_tekst(kleur, "naam"),
        doel=_tekst(kleur, "doel"),
        waarde=_tekst(kleur, "waarde"),
    )


def _resolved_waarden(obj: Architectuurobject, velden: tuple[str, ...]) -> dict[str, str]:
    return {veld: _tekst(obj, veld) for veld in velden}


def resolveer_thema(
    objecten: Iterable[Architectuurobject],
    wereld_id: str,
) -> ResolvedTheme:
    """Los één expliciet gekozen wereldthema volledig en deterministisch op."""

    index = _indexeer(objecten)
    wereld = _vereis(index, "wereld", wereld_id, "Theme-resolutie")
    thema = _vereis(index, "thema", _tekst(wereld, "thema"), f"Wereld '{wereld.id}'")

    palet = _vereis(index, "palet", _tekst(thema, "palet"), f"Thema '{thema.id}'")
    typografie = _vereis(index, "typografie", _tekst(thema, "typografie"), f"Thema '{thema.id}'")
    materiaal = _vereis(index, "materiaal", _tekst(thema, "materiaal"), f"Thema '{thema.id}'")
    border = _vereis(index, "border", _tekst(thema, "border"), f"Thema '{thema.id}'")
    radius = _vereis(index, "radius", _tekst(thema, "radius"), f"Thema '{thema.id}'")
    shadow = _vereis(index, "shadow", _tekst(thema, "shadow"), f"Thema '{thema.id}'")
    motion = _vereis(index, "motion", _tekst(thema, "motion"), f"Thema '{thema.id}'")

    palet_kleuren = tuple(
        (rol, _resolved_color(index, str(palet.eigenschappen[rol]), f"Palet '{palet.id}'"))
        for rol in PALET_ROLLEN if rol in palet.eigenschappen
    )
    materiaal_kleuren = tuple(
        (rol, _resolved_color(index, str(materiaal.eigenschappen[rol]), f"Materiaal '{materiaal.id}'"))
        for rol in MATERIAAL_ROLLEN if rol in materiaal.eigenschappen
    )

    return ResolvedTheme(
        wereld_id=wereld.id,
        wereld_naam=_tekst(wereld, "naam"),
        wereld_doel=_tekst(wereld, "doel"),
        thema_id=thema.id,
        thema_naam=_tekst(thema, "naam"),
        thema_doel=_tekst(thema, "doel"),
        palet=ResolvedPalette(palet.id, _tekst(palet, "naam"), _tekst(palet, "doel"), palet_kleuren),
        typografie=ResolvedTypography(
            typografie.id, _tekst(typografie, "naam"), _tekst(typografie, "doel"),
            **_resolved_waarden(typografie, ("heading", "body", "mono")),
        ),
        materiaal=ResolvedMaterial(
            materiaal.id, _tekst(materiaal, "naam"), _tekst(materiaal, "doel"), materiaal_kleuren,
        ),
        border=ResolvedBorder(
            border.id, _tekst(border, "naam"), _tekst(border, "doel"),
            **_resolved_waarden(border, ("hairline", "regular", "strong", "style")),
        ),
        radius=ResolvedRadius(
            radius.id, _tekst(radius, "naam"), _tekst(radius, "doel"),
            **_resolved_waarden(radius, ("small", "medium", "large", "pill")),
        ),
        shadow=ResolvedShadow(
            shadow.id, _tekst(shadow, "naam"), _tekst(shadow, "doel"),
            **_resolved_waarden(shadow, ("low", "medium", "high")),
        ),
        motion=ResolvedMotion(
            motion.id, _tekst(motion, "naam"), _tekst(motion, "doel"),
            **_resolved_waarden(motion, ("fast", "normal", "slow", "easing")),
        ),
    )


def resolveer_alle_themas(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedTheme, ...]:
    objecten = tuple(objecten)
    wereld_ids = sorted(obj.id for obj in objecten if obj.soort == "wereld")
    return tuple(resolveer_thema(objecten, wereld_id) for wereld_id in wereld_ids)
