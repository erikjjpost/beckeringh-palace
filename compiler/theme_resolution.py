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
class ResolvedSpacing:
    id: str
    naam: str
    doel: str
    none: str
    xs: str
    small: str
    medium: str
    large: str
    xl: str


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
    materiaal: ResolvedMaterial | None = None
    border: ResolvedBorder | None = None
    radius: ResolvedRadius | None = None
    shadow: ResolvedShadow | None = None
    motion: ResolvedMotion | None = None
    spacing: ResolvedSpacing | None = None


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
    return ResolvedColor(kleur.id, _tekst(kleur, "naam"), _tekst(kleur, "doel"), _tekst(kleur, "waarde"))


def _waarden(obj: Architectuurobject, velden: tuple[str, ...]) -> dict[str, str]:
    return {veld: _tekst(obj, veld) for veld in velden}


def _optioneel_object(index, thema: Architectuurobject, soort: str) -> Architectuurobject | None:
    object_id = thema.eigenschappen.get(soort)
    if object_id is None:
        return None
    if not isinstance(object_id, str) or not object_id.strip():
        raise ThemeResolutionError(f"Thema '{thema.id}' heeft ongeldige {soort}referentie")
    return _vereis(index, soort, object_id, f"Thema '{thema.id}'")


def resolveer_thema(objecten: Iterable[Architectuurobject], wereld_id: str) -> ResolvedTheme:
    """Los één expliciet gekozen wereldthema volledig en deterministisch op."""

    index = _indexeer(objecten)
    wereld = _vereis(index, "wereld", wereld_id, "Theme-resolutie")
    thema = _vereis(index, "thema", _tekst(wereld, "thema"), f"Wereld '{wereld.id}'")
    palet = _vereis(index, "palet", _tekst(thema, "palet"), f"Thema '{thema.id}'")
    typografie = _vereis(index, "typografie", _tekst(thema, "typografie"), f"Thema '{thema.id}'")

    materiaal = _optioneel_object(index, thema, "materiaal")
    border = _optioneel_object(index, thema, "border")
    radius = _optioneel_object(index, thema, "radius")
    shadow = _optioneel_object(index, thema, "shadow")
    motion = _optioneel_object(index, thema, "motion")
    spacing = _optioneel_object(index, thema, "spacing")

    palet_kleuren = tuple(
        (rol, _resolved_color(index, str(palet.eigenschappen[rol]), f"Palet '{palet.id}'"))
        for rol in PALET_ROLLEN if rol in palet.eigenschappen
    )
    resolved_materiaal = None
    if materiaal is not None:
        resolved_materiaal = ResolvedMaterial(
            materiaal.id, _tekst(materiaal, "naam"), _tekst(materiaal, "doel"),
            tuple(
                (rol, _resolved_color(index, str(materiaal.eigenschappen[rol]), f"Materiaal '{materiaal.id}'"))
                for rol in MATERIAAL_ROLLEN if rol in materiaal.eigenschappen
            ),
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
            **_waarden(typografie, ("heading", "body", "mono")),
        ),
        materiaal=resolved_materiaal,
        border=None if border is None else ResolvedBorder(
            border.id, _tekst(border, "naam"), _tekst(border, "doel"),
            **_waarden(border, ("hairline", "regular", "strong", "style")),
        ),
        radius=None if radius is None else ResolvedRadius(
            radius.id, _tekst(radius, "naam"), _tekst(radius, "doel"),
            **_waarden(radius, ("small", "medium", "large", "pill")),
        ),
        shadow=None if shadow is None else ResolvedShadow(
            shadow.id, _tekst(shadow, "naam"), _tekst(shadow, "doel"),
            **_waarden(shadow, ("low", "medium", "high")),
        ),
        motion=None if motion is None else ResolvedMotion(
            motion.id, _tekst(motion, "naam"), _tekst(motion, "doel"),
            **_waarden(motion, ("fast", "normal", "slow", "easing")),
        ),
        spacing=None if spacing is None else ResolvedSpacing(
            spacing.id, _tekst(spacing, "naam"), _tekst(spacing, "doel"),
            **_waarden(spacing, ("none", "xs", "small", "medium", "large", "xl")),
        ),
    )


def resolveer_alle_themas(objecten: Iterable[Architectuurobject]) -> tuple[ResolvedTheme, ...]:
    objecten = tuple(objecten)
    wereld_ids = sorted(obj.id for obj in objecten if obj.soort == "wereld")
    return tuple(resolveer_thema(objecten, wereld_id) for wereld_id in wereld_ids)
