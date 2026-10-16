"""Native, backend-onafhankelijk presentatiemodel voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.design_compositions import ResolvedComposition, resolveer_composities
from compiler.layout_model import ResolvedLayout, resolveer_layouts


class DiaFormaat(str, Enum):
    """De native dia-archetypen: een gecontroleerd, gesloten vocabulaire.

    Een dia hergebruikt het compositie/layoutcontract 1 op 1 voor haar
    concrete inhoud en plaatsing, maar dat contract draagt geen semantiek
    over wát voor dia dit is. Zonder die semantiek is iedere dia voor een
    toekomstige renderer ononderscheidbaar van een dashboardpaneel. Formaat
    lost dat op als expliciet, gesloten veld, naar hetzelfde precedent als
    `layout.type`: geen vrije string, geen impliciete standaardwaarde.
    """

    COVER = "cover"
    SECTIE = "sectie"
    KAARTENGRID = "kaartengrid"
    VERGELIJKING = "vergelijking"
    TIJDLIJN = "tijdlijn"
    CITAAT = "citaat"
    AFSLUITING = "afsluiting"


@dataclass(frozen=True)
class ResolvedDia:
    """Eén benoemde presentatiedia die een bestaande compositie en layout hergebruikt."""

    id: str
    naam: str
    doel: str
    formaat: DiaFormaat
    opgeloste_compositie: ResolvedComposition
    opgeloste_layout: ResolvedLayout


@dataclass(frozen=True)
class ResolvedPresentation:
    """Geordende presentatie van zelfstandig opgeloste dia's."""

    id: str
    naam: str
    doel: str
    dias: tuple[ResolvedDia, ...]


class PresentationResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot een presentatie worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise PresentationResolutionError(
            f"{obj.soort.capitalize()} '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _dia_uit_object(
    obj: Architectuurobject,
    composities: dict[str, ResolvedComposition],
    layouts: dict[str, ResolvedLayout],
) -> ResolvedDia:
    compositie_id = _tekst(obj, "compositie")
    layout_id = _tekst(obj, "layout")
    try:
        formaat = DiaFormaat(_tekst(obj, "formaat"))
    except ValueError as exc:
        raise PresentationResolutionError(
            f"Dia '{obj.id}' heeft onbekend formaat "
            f"'{obj.eigenschappen.get('formaat')}'"
        ) from exc
    try:
        opgeloste_compositie = composities[compositie_id]
    except KeyError as exc:
        raise PresentationResolutionError(
            f"Dia '{obj.id}' verwijst naar onbekende compositie '{compositie_id}'"
        ) from exc
    try:
        opgeloste_layout = layouts[layout_id]
    except KeyError as exc:
        raise PresentationResolutionError(
            f"Dia '{obj.id}' verwijst naar onbekende layout '{layout_id}'"
        ) from exc
    return ResolvedDia(
        id=obj.id,
        naam=_tekst(obj, "naam"),
        doel=_tekst(obj, "doel"),
        formaat=formaat,
        opgeloste_compositie=opgeloste_compositie,
        opgeloste_layout=opgeloste_layout,
    )


def resolveer_presentaties(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedPresentation, ...]:
    """Los gevalideerde presentaties deterministisch op vanuit de CIR.

    Hergebruikt `resolveer_composities`/`resolveer_layouts`: een presentatie
    introduceert geen tweede compositie- of layoutresolver, zij ordent
    uitsluitend bestaande, elders al opgeloste composities en layouts per dia.
    """

    objecten = tuple(objecten)
    dias = {
        obj.id: obj
        for obj in objecten
        if obj.soort == "dia"
    }
    composities = {
        compositie.id: compositie
        for compositie in resolveer_composities(objecten)
    }
    layouts = {layout.id: layout for layout in resolveer_layouts(objecten)}

    presentaties = []
    for obj in objecten:
        if obj.soort != "presentatie":
            continue
        dia_ids = obj.eigenschappen.get("dias")
        if not isinstance(dia_ids, list):
            raise PresentationResolutionError(
                f"Presentatie '{obj.id}' vereist lijstveld 'dias'"
            )
        try:
            resolved_dias = tuple(
                _dia_uit_object(dias[dia_id], composities, layouts)
                for dia_id in dia_ids
            )
        except KeyError as exc:
            raise PresentationResolutionError(
                f"Presentatie '{obj.id}' bevat een onbekende dia"
            ) from exc
        presentaties.append(ResolvedPresentation(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            dias=resolved_dias,
        ))
    return tuple(sorted(presentaties, key=lambda presentatie: presentatie.id))
