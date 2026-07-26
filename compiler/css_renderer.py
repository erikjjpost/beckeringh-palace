"""CSS-renderer voor Beckeringh Palace design tokens."""
from __future__ import annotations

import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_tokens import DesignToken, verzamel_tokens


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "token"


def _css_waarde(token: DesignToken) -> str:
    if token.referentie is not None:
        return f"var(--bp-{_css_naam(token.referentie)})"
    return token.waarde


def naar_css(objecten: Iterable[Architectuurobject]) -> str:
    """Render gevalideerde tokenobjecten deterministisch naar CSS custom properties."""

    regels = ["/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */", ":root {"]
    for token in verzamel_tokens(objecten):
        regels.append(f"  --bp-{_css_naam(token.id)}: {_css_waarde(token)};")
    regels.extend(["}", ""])
    return "\n".join(regels)
