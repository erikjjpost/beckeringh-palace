"""Valideer gecontroleerde externe ontwerpinput zonder haar normatief te maken."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {
    "mapbaar",
    "gedeeltelijk-mapbaar",
    "besluit-nodig",
    "geblokkeerd",
    "gemigreerd",
}


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"ontwerpbron: '{field}' moet niet-lege tekst zijn")
    return value


def validate_design_input(source: dict[str, Any]) -> None:
    if source.get("schema_version") != 1:
        raise ValueError("ontwerpbron: schema_version moet 1 zijn")
    for field in ("id", "naam", "status", "ontvangen_op"):
        _text(source.get(field), field)
    digest = source.get("archief_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise ValueError("ontwerpbron: archief_sha256 moet een SHA-256 zijn")
    if not isinstance(source.get("bestanden"), int) or source["bestanden"] < 1:
        raise ValueError("ontwerpbron: bestanden moet positief zijn")

    contract = source.get("broncontract")
    if not isinstance(contract, dict):
        raise ValueError("ontwerpbron: broncontract ontbreekt")
    if contract.get("normatief") is not False:
        raise ValueError("ontwerpbron: externe input mag niet normatief zijn")
    if contract.get("externe_afhankelijkheden_toegestaan") is not False:
        raise ValueError("ontwerpbron: externe runtimeafhankelijkheden zijn verboden")
    _text(contract.get("rol"), "broncontract.rol")
    _text(contract.get("activering"), "broncontract.activering")

    areas = source.get("gebieden")
    if not isinstance(areas, list) or not areas:
        raise ValueError("ontwerpbron: gebieden moet niet leeg zijn")
    ids: set[str] = set()
    for area in areas:
        if not isinstance(area, dict):
            raise ValueError("ontwerpbron: ieder gebied moet een object zijn")
        area_id = _text(area.get("id"), "gebieden.id")
        if area_id in ids:
            raise ValueError(f"ontwerpbron: dubbel gebied '{area_id}'")
        ids.add(area_id)
        if area.get("status") not in ALLOWED_STATUSES:
            raise ValueError(f"ontwerpbron: ongeldig status voor '{area_id}'")
        _text(area.get("doel"), f"gebieden.{area_id}.doel")
        _text(area.get("bewijs"), f"gebieden.{area_id}.bewijs")

    exclusions = source.get("uitsluitingen")
    if not isinstance(exclusions, list) or not exclusions:
        raise ValueError("ontwerpbron: uitsluitingen moet niet leeg zijn")
    for exclusion in exclusions:
        _text(exclusion, "uitsluitingen")


def load_design_input(path: Path) -> dict[str, Any]:
    source = json.loads(path.read_text(encoding="utf-8"))
    validate_design_input(source)
    return source
