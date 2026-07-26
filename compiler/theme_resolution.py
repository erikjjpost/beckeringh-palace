"""Getypeerde resolutie van expliciete Beckeringh Palace-ontwerpwerelden."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


PALET_ROLLEN = (
    "primary",
    "secondary",
    "background",
    "surface",
    "foreground",
    "accent",
    "success",
    "warning",
    "error",
)


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
        """Geef de opgeloste kleur voor een semantische paletrol."""

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
class ResolvedTheme:
    wereld_id: str
    wereld_naam: str
    wereld_doel: str
    thema_id: str
    thema_naam: str
    thema_doel: str
    palet: ResolvedPalette
    typografie: ResolvedTypography


def _indexeer(
    objecten: Iterable[Architectuurobject],
) -> dict[str, dict[str, Architectuurobject]]:
    index: dict[str, dict[str, Architectuurobject]] = {}
    for obj in objecten:
        index.setdefault(obj.soort, {})[obj.id] = obj
    return index


def _vereis(
    index: dict[str, dict[str, Architectuurobject]],
    soort: str,
    object_id: str,
    context: str,
) -> Architectuurobject:
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


def resolveer_thema(
    objecten: Iterable[Architectuurobject],
    wereld_id: str,
) -> ResolvedTheme:
    """Los één expliciet gekozen wereldthema volledig en deterministisch op."""

    index = _indexeer(objecten)
    wereld = _vereis(index, "wereld", wereld_id, "Theme-resolutie")
    thema_id = _tekst(wereld, "thema")
    thema = _vereis(index, "thema", thema_id, f"Wereld '{wereld.id}'")

    palet_id = _tekst(thema, "palet")
    typografie_id = _tekst(thema, "typografie")
    palet = _vereis(index, "palet", palet_id, f"Thema '{thema.id}'")
    typografie = _vereis(
        index,
        "typografie",
        typografie_id,
        f"Thema '{thema.id}'",
    )

    opgeloste_kleuren = []
    for rol in PALET_ROLLEN:
        kleur_id = palet.eigenschappen.get(rol)
        if kleur_id is None:
            continue
        if not isinstance(kleur_id, str) or not kleur_id.strip():
            raise ThemeResolutionError(
                f"Palet '{palet.id}' heeft ongeldige kleurreferentie voor '{rol}'"
            )
        kleur = _vereis(index, "kleur", kleur_id, f"Palet '{palet.id}'")
        opgeloste_kleuren.append((rol, ResolvedColor(
            id=kleur.id,
            naam=_tekst(kleur, "naam"),
            doel=_tekst(kleur, "doel"),
            waarde=_tekst(kleur, "waarde"),
        )))

    resolved_palette = ResolvedPalette(
        id=palet.id,
        naam=_tekst(palet, "naam"),
        doel=_tekst(palet, "doel"),
        kleuren=tuple(opgeloste_kleuren),
    )
    resolved_typography = ResolvedTypography(
        id=typografie.id,
        naam=_tekst(typografie, "naam"),
        doel=_tekst(typografie, "doel"),
        heading=_tekst(typografie, "heading"),
        body=_tekst(typografie, "body"),
        mono=_tekst(typografie, "mono"),
    )
    return ResolvedTheme(
        wereld_id=wereld.id,
        wereld_naam=_tekst(wereld, "naam"),
        wereld_doel=_tekst(wereld, "doel"),
        thema_id=thema.id,
        thema_naam=_tekst(thema, "naam"),
        thema_doel=_tekst(thema, "doel"),
        palet=resolved_palette,
        typografie=resolved_typography,
    )


def resolveer_alle_themas(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedTheme, ...]:
    """Los alle expliciete werelden in stabiele ID-volgorde op."""

    objecten = tuple(objecten)
    wereld_ids = sorted(obj.id for obj in objecten if obj.soort == "wereld")
    return tuple(resolveer_thema(objecten, wereld_id) for wereld_id in wereld_ids)
