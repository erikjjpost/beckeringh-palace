"""CSS-renderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.component_css_identity import componentselector, stateklasse
from compiler.design_variants import resolveer_varianten
from compiler.design_components import (
    ComponentAppearance,
    DesignComponent,
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
    selectors: tuple[str, ...],
    appearance: ComponentAppearance,
) -> list[str]:
    selector = ", ".join(selectors)
    material = appearance.rol("material")
    foreground = appearance.rol("foreground")
    accent = appearance.rol("accent")
    outline = appearance.rol("outline")
    border = appearance.rol("border")
    radius = appearance.rol("radius")
    shadow = appearance.rol("shadow")
    motion = appearance.rol("motion")
    offset = appearance.rol("offset")
    spacing = appearance.rol("spacing")
    heading = appearance.rol("heading-style")
    body = appearance.rol("body-style")
    label = appearance.rol("label-style")
    caption = appearance.rol("caption-style")
    heading_selectors = ", ".join(
        f"{item} {heading_tag}"
        for item in selectors
        for heading_tag in ("h1", "h2", "h3", "h4", "h5", "h6")
    )
    paragraph_selectors = ", ".join(f"{item} p" for item in selectors)
    label_selectors = ", ".join(f"{item} label" for item in selectors)
    caption_selectors = ", ".join(
        f"{item} {caption_tag}"
        for item in selectors
        for caption_tag in ("small", "figcaption")
    )
    return [
        f"{selector} {{",
        f"  --bp-component-accent: var(--bp-material-{accent});",
        f"  background-color: var(--bp-material-{material});",
        f"  color: var(--bp-material-{foreground});",
        f"  border: var(--bp-border-{border}) var(--bp-border-style) var(--bp-material-{outline});",
        f"  border-radius: var(--bp-radius-{radius});",
        f"  box-shadow: var(--bp-shadow-{shadow});",
        f"  transform: translateY(var(--bp-motion-{offset}-offset));",
        "  transition-property: background-color, border-color, box-shadow, color, transform;",
        f"  transition-duration: var(--bp-motion-{motion});",
        "  transition-timing-function: var(--bp-motion-easing);",
        f"  padding: var(--bp-spacing-{spacing});",
        "}",
        "",
        f"{heading_selectors} {{",
        "  font-family: var(--bp-font-heading);",
        f"  font-size: var(--bp-type-{heading});",
        "}",
        f"{paragraph_selectors} {{",
        "  font-family: var(--bp-font-body);",
        f"  font-size: var(--bp-type-{body});",
        "}",
        f"{label_selectors} {{",
        "  font-family: var(--bp-font-body);",
        f"  font-size: var(--bp-type-{label});",
        "}",
        f"{caption_selectors} {{",
        "  font-family: var(--bp-font-body);",
        f"  font-size: var(--bp-type-{caption});",
        "}",
        "",
    ]


def _state_selectors(selector: str, state: str) -> tuple[str, ...]:
    explicit = f"{selector}.{stateklasse(state)}"
    if state == "hover":
        return (
            f'{selector}:hover:not([aria-disabled="true"])',
            explicit,
        )
    if state == "focus":
        return (
            f"{selector}:focus-visible",
            f"{selector}:focus-within",
            explicit,
        )
    if state == "pressed":
        return (
            f'{selector}:active:not([aria-disabled="true"])',
            explicit,
        )
    if state == "disabled":
        return (
            f"{selector}:disabled",
            f'{selector}[aria-disabled="true"]',
            explicit,
        )
    raise ValueError(f"Onbekende componentstate '{state}'")


def _componentrol_regels(component: DesignComponent) -> list[str]:
    selector = componentselector(component.id)
    if component.rol == "actie":
        return [
            f"{selector} {{",
            "  display: inline-flex;",
            "  align-items: center;",
            "  justify-content: center;",
            "  gap: var(--bp-spacing-small);",
            "  cursor: pointer;",
            "  font-family: var(--bp-font-body);",
            "  font-size: var(--bp-type-label);",
            "  font-weight: 600;",
            "}",
            "",
        ]
    if component.rol == "invoer":
        return [
            f"{selector} {{",
            "  display: block;",
            "  box-sizing: border-box;",
            "  width: 100%;",
            "  font-family: var(--bp-font-body);",
            "  font-size: var(--bp-type-label);",
            "}",
            "",
        ]
    if component.rol == "status":
        return [
            f"{selector} {{",
            "  display: inline-flex;",
            "  align-items: center;",
            "  gap: var(--bp-spacing-small);",
            "  width: fit-content;",
            "  font-family: var(--bp-font-body);",
            "  font-size: var(--bp-type-caption);",
            "  font-weight: 600;",
            "}",
            "",
        ]
    if component.rol == "app-tegel":
        return [
            f"{selector} {{",
            "  display: grid;",
            "  grid-template-columns: 1fr auto;",
            "  gap: var(--bp-spacing-medium);",
            "  align-items: center;",
            "}",
            f"{selector} strong {{",
            "  font-family: var(--bp-font-body);",
            "  font-size: var(--bp-type-label);",
            "}",
            f"{selector} small {{",
            "  color: var(--bp-component-accent);",
            "  font-family: var(--bp-font-mono);",
            "}",
            "",
        ]
    if component.rol == "statistiek":
        return [
            f"{selector} {{",
            "  display: flex;",
            "  flex-direction: column;",
            "  gap: var(--bp-spacing-small);",
            "}",
            f"{selector} > strong {{",
            "  color: var(--bp-component-accent);",
            "  font-family: var(--bp-font-heading);",
            "  font-size: var(--bp-type-heading);",
            "}",
            f"{selector} > small {{",
            "  font-family: var(--bp-font-mono);",
            "  letter-spacing: 0.18em;",
            "  text-transform: uppercase;",
            "}",
            "",
        ]
    return []


def naar_component_css(objecten: Iterable[Architectuurobject]) -> str:
    objecten = tuple(objecten)
    appearances = {appearance.id: appearance for appearance in verzamel_appearances(objecten)}
    regels = ["/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */"]
    for component in verzamel_componenten(objecten):
        appearance = appearances.get(component.appearance or "")
        selector = componentselector(component.id)
        if appearance is not None:
            regels.extend(_appearance_regels((selector,), appearance))
        else:
            regels.append(f"{selector} {{")
            padding = component.eigenschappen.get("padding")
            if padding is not None:
                regels.append(f"  padding: {_tokenwaarde(padding)};")
            regels.extend(["}", ""])
        regels.extend(_componentrol_regels(component))

    for variant in resolveer_varianten(objecten):
        appearance = appearances[variant.appearance_id]
        selector = componentselector(variant.component_id, variant.id)
        regels.extend(_appearance_regels((selector,), appearance))
        for state, appearance_id in variant.state_appearances:
            if state == "rest":
                continue
            state_selectors = _state_selectors(selector, state)
            regels.extend(
                _appearance_regels(
                    state_selectors,
                    appearances[appearance_id],
                )
            )
            if state == "disabled":
                regels.extend([
                    f"{', '.join(state_selectors)} {{",
                    "  cursor: not-allowed;",
                    "}",
                    "",
                ])
    return "\n".join(regels)
