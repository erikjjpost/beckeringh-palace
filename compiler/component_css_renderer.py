"""CSS-renderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_components import tokenreferentie, verzamel_appearances, verzamel_componenten


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "component"


def _tokenwaarde(waarde: str) -> str:
    referentie = tokenreferentie(waarde)
    return waarde if referentie is None else f"var(--bp-{_css_naam(referentie)})"


def naar_component_css(objecten: Iterable[Architectuurobject]) -> str:
    objecten = tuple(objecten)
    appearances = {appearance.id: appearance for appearance in verzamel_appearances(objecten)}
    regels = ["/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */"]
    for component in verzamel_componenten(objecten):
        appearance = appearances.get(component.appearance or "")
        regels.append(f".bp-{_css_naam(component.id)} {{")
        if appearance is not None:
            material = appearance.rol("material")
            foreground = appearance.rol("foreground")
            accent = appearance.rol("accent")
            border = appearance.rol("border")
            radius = appearance.rol("radius")
            shadow = appearance.rol("shadow")
            motion = appearance.rol("motion")
            regels.extend([
                f"  background-color: var(--bp-material-{material});",
                f"  color: var(--bp-material-{foreground});",
                f"  border: var(--bp-border-{border}) var(--bp-border-style) var(--bp-material-{accent});",
                f"  border-radius: var(--bp-radius-{radius});",
                f"  box-shadow: var(--bp-shadow-{shadow});",
                f"  transition-duration: var(--bp-motion-{motion});",
                "  transition-timing-function: var(--bp-motion-easing);",
            ])
        padding = component.eigenschappen.get("padding")
        if padding is not None:
            regels.append(f"  padding: {_tokenwaarde(padding)};")
        regels.extend(["}", ""])
    return "\n".join(regels)
