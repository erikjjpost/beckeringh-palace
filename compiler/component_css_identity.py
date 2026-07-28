"""Canonieke CSS-identiteit voor gerenderde componenten en varianten."""
from __future__ import annotations

import re


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "component"


def componentklasse(component_id: str) -> str:
    return f"bp-{_css_naam(component_id)}"


def variantklasse(variant_id: str) -> str:
    return f"bp-variant-{_css_naam(variant_id)}"


def stateklasse(state: str) -> str:
    return f"bp-state-{_css_naam(state)}"


def componentselector(component_id: str, variant_id: str | None = None) -> str:
    selector = f".{componentklasse(component_id)}"
    if variant_id is not None:
        selector += f".{variantklasse(variant_id)}"
    return selector
