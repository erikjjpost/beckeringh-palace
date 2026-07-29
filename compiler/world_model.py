"""Domeingrens voor het Beckeringh Palace World Model.

BAT is een product- en ontwerpcompiler. Dit module legt vast welke objectsoorten
native onderdeel zijn van dat domein en welke soorten alleen tijdens de migratie
of via externe adapters mogen voorkomen.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Domeinstatus(str, Enum):
    """Plaats van een objectsoort ten opzichte van het BAT-kernmodel."""

    NATIVE = "native"
    EXTERN = "extern"
    MIGRATIE = "migratie"


@dataclass(frozen=True)
class ObjectsoortDefinitie:
    """Normatieve definitie van één objectsoort."""

    naam: str
    status: Domeinstatus
    doel: str


_OBJECTSOORTEN = (
    ObjectsoortDefinitie("wereld", Domeinstatus.NATIVE, "Begrenst één digitale wereld en kiest expliciet een thema."),
    ObjectsoortDefinitie("merk", Domeinstatus.NATIVE, "Beschrijft identiteit en merkregels."),
    ObjectsoortDefinitie("kleur", Domeinstatus.NATIVE, "Definieert één canonieke kleurwaarde."),
    ObjectsoortDefinitie("palet", Domeinstatus.NATIVE, "Koppelt semantische kleurrollen aan canonieke kleuren."),
    ObjectsoortDefinitie("typografie", Domeinstatus.NATIVE, "Bundelt expliciete typografische familierollen."),
    ObjectsoortDefinitie("typeschaal", Domeinstatus.NATIVE, "Definieert een normatieve schaal voor semantische tekstgroottes."),
    ObjectsoortDefinitie("materiaal", Domeinstatus.NATIVE, "Bundelt semantische oppervlaktekleuren voor productmaterialen."),
    ObjectsoortDefinitie("border", Domeinstatus.NATIVE, "Definieert normatieve randdiktes en randstijlen."),
    ObjectsoortDefinitie("radius", Domeinstatus.NATIVE, "Definieert normatieve hoekafrondingen."),
    ObjectsoortDefinitie("shadow", Domeinstatus.NATIVE, "Definieert normatieve diepteniveaus als schaduwwaarden."),
    ObjectsoortDefinitie("motion", Domeinstatus.NATIVE, "Definieert normatieve duur- en easingrollen."),
    ObjectsoortDefinitie("spacing", Domeinstatus.NATIVE, "Definieert een normatieve schaal voor tussenruimte en interne ruimte."),
    ObjectsoortDefinitie("artdirection", Domeinstatus.NATIVE, "Legt de visuele balans, ornamentiek en beeldtaal van een thema vast."),
    ObjectsoortDefinitie("thema", Domeinstatus.NATIVE, "Koppelt alle ontwerpprimitieven tot één ontwerpidentiteit."),
    ObjectsoortDefinitie("appearance", Domeinstatus.NATIVE, "Koppelt een component aan semantische theme-rollen en primitiveprofielen."),
    ObjectsoortDefinitie("token", Domeinstatus.NATIVE, "Definieert een herbruikbare ontwerpwaarde."),
    ObjectsoortDefinitie("asset", Domeinstatus.NATIVE, "Beschrijft een reproduceerbaar bronasset."),
    ObjectsoortDefinitie("component", Domeinstatus.NATIVE, "Definieert een herbruikbaar productonderdeel."),
    ObjectsoortDefinitie("toegankelijkheid", Domeinstatus.NATIVE, "Legt naam, rol, waarde, fout, disabled, focus en toetsenbordgedrag van een component vast."),
    ObjectsoortDefinitie("componentvoorbeeld", Domeinstatus.NATIVE, "Legt productgedragen voorbeeldinhoud voor één componentvariant vast."),
    ObjectsoortDefinitie("informatiegebied", Domeinstatus.NATIVE, "Bundelt objectsoorten tot één benoemd informatiegebied voor producten."),
    ObjectsoortDefinitie("homepagegebied", Domeinstatus.NATIVE, "Definieert één geordend inhoudsgebied met kernboodschap en productroute voor de homepage."),
    ObjectsoortDefinitie("compositie", Domeinstatus.NATIVE, "Bundelt benoemde componentinstanties tot productinhoud."),
    ObjectsoortDefinitie("componentinstantie", Domeinstatus.NATIVE, "Beschrijft één benoemd gebruik van een component in een compositie."),
    ObjectsoortDefinitie("layout", Domeinstatus.NATIVE, "Beschrijft backend-onafhankelijke layoutintentie."),
    ObjectsoortDefinitie("region", Domeinstatus.NATIVE, "Plaatst een component expliciet binnen een native layout."),
    ObjectsoortDefinitie("product", Domeinstatus.NATIVE, "Koppelt een layout aan een backend en artifactpad."),
    ObjectsoortDefinitie("variant", Domeinstatus.NATIVE, "Legt een gecontroleerde componentappearance vast."),
    ObjectsoortDefinitie("renderdoel", Domeinstatus.NATIVE, "Beschrijft een te genereren representatie."),
    ObjectsoortDefinitie("capability", Domeinstatus.MIGRATIE, "Bestaand architectuurconcept tijdens de BAT-migratie."),
    ObjectsoortDefinitie("dienst", Domeinstatus.MIGRATIE, "Bestaand architectuurconcept tijdens de BAT-migratie."),
    ObjectsoortDefinitie("agent", Domeinstatus.MIGRATIE, "Bestaand architectuurconcept tijdens de BAT-migratie."),
    ObjectsoortDefinitie("archimate", Domeinstatus.EXTERN, "Extern architectuurmodel dat uitsluitend via een adapter binnenkomt."),
)

OBJECTSOORTEN = {definitie.naam: definitie for definitie in _OBJECTSOORTEN}
NATIVE_OBJECTSOORTEN = frozenset(
    definitie.naam
    for definitie in _OBJECTSOORTEN
    if definitie.status is Domeinstatus.NATIVE
)


def objectsoortdefinitie(naam: str) -> ObjectsoortDefinitie | None:
    """Geef de domeindefinitie van één objectsoort terug."""

    return OBJECTSOORTEN.get(naam)


def is_native_objectsoort(naam: str) -> bool:
    """Bepaal of een objectsoort tot de BAT-kern behoort."""

    return naam in NATIVE_OBJECTSOORTEN
