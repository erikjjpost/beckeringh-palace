"""CSS-renderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_components import tokenreferentie, verzamel_componenten

CSS_EIGENSCHAPPEN = {
    "surface": "background-color",
    "foreground": "color",
    "accent": "border-color",
    "padding": "padding",
    "radius": "border-radius",
}


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "component"


def _css_waarde(waarde: str) -> str:
    referentie = tokenreferentie(waarde)
    if referentie is None:
        return waarde
    return f"var(--bp-{_css_naam(referentie)})"


def naar_component_css(objecten: Iterable[Architectuurobject]) -> str:
    regels = ["/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */"]
    for component in verzamel_componenten(objecten):
        regels.append(f".bp-{_css_naam(component.id)} {{")
        for naam in CSS_EIGENSCHAPPEN:
            waarde = component.eigenschappen.get(naam)
            if waarde is not None:
                regels.append(f"  {CSS_EIGENSCHAPPEN[naam]}: {_css_waarde(waarde)};")
        regels.extend(["}", ""])
    return "\n".join(regels)
