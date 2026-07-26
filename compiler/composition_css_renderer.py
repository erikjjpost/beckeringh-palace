"""CSS-renderer voor Beckeringh Palace-composities."""
from __future__ import annotations

import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_compositions import verzamel_composities


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "composition"


def naar_compositie_css(objecten: Iterable[Architectuurobject]) -> str:
    regels = ["/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */"]
    for compositie in verzamel_composities(objecten):
        regels.extend([
            f".bp-{_css_naam(compositie.id)} {{",
            "  display: flex;",
            f"  flex-direction: {compositie.richting};",
            "  gap: var(--bp-spacing-unit);",
            "}",
            "",
        ])
    return "\n".join(regels)
