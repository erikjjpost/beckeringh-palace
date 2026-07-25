"""Kleine, afhankelijkheidsvrije parser voor de eerste BAT-slice."""
from __future__ import annotations

import re
from pathlib import Path

from compiler.cir import Architectuurobject

SOORTEN = {"capability", "dienst", "proces", "representatie", "agent"}
KOP = re.compile(r"^(?P<soort>\w+)\s+(?P<id>[\w.-]+)\s*\{$")
EIGENSCHAP = re.compile(r"^(?P<naam>[\w-]+)\s*:\s*(?P<waarde>.+)$")


class BATFout(ValueError):
    """Ongeldige Beckeringh Architectuurtaal."""


def _waarde(tekst: str):
    tekst = tekst.strip()
    if tekst.startswith("[") and tekst.endswith("]"):
        inhoud = tekst[1:-1].strip()
        return [] if not inhoud else [_waarde(deel) for deel in inhoud.split(",")]
    if tekst.startswith('"') and tekst.endswith('"'):
        return tekst[1:-1]
    return tekst


def parseer(tekst: str) -> list[Architectuurobject]:
    regels = [regel.strip() for regel in tekst.splitlines() if regel.strip() and not regel.strip().startswith("#")]
    objecten: list[Architectuurobject] = []
    index = 0
    while index < len(regels):
        match = KOP.match(regels[index])
        if not match or match.group("soort") not in SOORTEN:
            raise BATFout(f"Ongeldige declaratie op regel {index + 1}: {regels[index]}")
        soort, object_id = match.group("soort"), match.group("id")
        eigenschappen = {}
        index += 1
        while index < len(regels) and regels[index] != "}":
            eigenschap = EIGENSCHAP.match(regels[index])
            if not eigenschap:
                raise BATFout(f"Ongeldige eigenschap op regel {index + 1}: {regels[index]}")
            naam = eigenschap.group("naam")
            if naam in eigenschappen:
                raise BATFout(f"Dubbele eigenschap '{naam}' in {object_id}")
            eigenschappen[naam] = _waarde(eigenschap.group("waarde"))
            index += 1
        if index >= len(regels):
            raise BATFout(f"Ontbrekende sluitaccolade voor {object_id}")
        if "naam" not in eigenschappen or "doel" not in eigenschappen:
            raise BATFout(f"{object_id} vereist de eigenschappen 'naam' en 'doel'")
        objecten.append(Architectuurobject(soort, object_id, eigenschappen))
        index += 1
    ids = [obj.id for obj in objecten]
    if len(ids) != len(set(ids)):
        raise BATFout("Dubbele object-id aangetroffen")
    return objecten


def parseer_bestand(pad: Path) -> list[Architectuurobject]:
    return parseer(pad.read_text(encoding="utf-8"))
