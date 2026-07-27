"""CSS-renderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.component_css_identity import componentselector
from compiler.design_variants import resolveer_varianten
from compiler.design_components import (
    ComponentAppearance,
    tokenreferentie,
    verzamel_appearances,
    verzamel_componenten,
)


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "component"


def _tokenwaarde(waarde: str) -> str:
    referentie = tokenreferentie(waarde)
    return waarde if referentie is None else f"var(--bp-{_css_naam(referentie)})"


def _appearance_regels(
    selector: str,
    appearance: ComponentAppearance,
) -> list[str]:
    material = appearance.rol("material")
    foreground = appearance.rol("foreground")
    accent = appearance.rol("accent")
    border = appearance.rol("border")
    radius = appearance.rol("radius")
    shadow = appearance.rol("shadow")
    motion = appearance.rol("motion")
    spacing = appearance.rol("spacing")
    heading = appearance.rol("heading-style")
    body = appearance.rol("body-style")
    label = appearance.rol("label-style")
    caption = appearance.rol("caption-style")
    return [
        f"{selector} {{",
        f"  background-color: var(--bp-material-{material});",
        f"  color: var(--bp-material-{foreground});",
        f"  border: var(--bp-border-{border}) var(--bp-border-style) var(--bp-material-{accent});",
        f"  border-radius: var(--bp-radius-{radius});",
        f"  box-shadow: var(--bp-shadow-{shadow});",
        f"  transition-duration: var(--bp-motion-{motion});",
        "  transition-timing-function: var(--bp-motion-easing);",
        f"  padding: var(--bp-spacing-{spacing});",
        "}",
        "",
        f"{selector} h1, {selector} h2, {selector} h3, {selector} h4, {selector} h5, {selector} h6 {{",
        "  font-family: var(--bp-font-heading);",
        f"  font-size: var(--bp-type-{heading});",
        "}",
        f"{selector} p {{",
        "  font-family: var(--bp-font-body);",
        f"  font-size: var(--bp-type-{body});",
        "}",
        f"{selector} label {{",
        "  font-family: var(--bp-font-body);",
        f"  font-size: var(--bp-type-{label});",
        "}",
        f"{selector} small, {selector} figcaption {{",
        "  font-family: var(--bp-font-body);",
        f"  font-size: var(--bp-type-{caption});",
        "}",
        "",
    ]


def naar_component_css(objecten: Iterable[Architectuurobject]) -> str:
    objecten = tuple(objecten)
    appearances = {appearance.id: appearance for appearance in verzamel_appearances(objecten)}
    regels = ["/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */"]
    for component in verzamel_componenten(objecten):
        appearance = appearances.get(component.appearance or "")
        selector = componentselector(component.id)
        if appearance is not None:
            regels.extend(_appearance_regels(selector, appearance))
        else:
            regels.append(f"{selector} {{")
            padding = component.eigenschappen.get("padding")
            if padding is not None:
                regels.append(f"  padding: {_tokenwaarde(padding)};")
            regels.extend(["}", ""])

    for variant in resolveer_varianten(objecten):
        appearance = appearances[variant.appearance_id]
        selector = componentselector(variant.component_id, variant.id)
        regels.extend(_appearance_regels(selector, appearance))
    return "\n".join(regels)
