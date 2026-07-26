"""CSS-renderer voor Beckeringh Palace design tokens."""
from __future__ import annotations

import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "token"


def naar_css(objecten: Iterable[Architectuurobject]) -> str:
    """Render tokenobjecten deterministisch naar CSS custom properties."""

    tokens = sorted(
        (obj for obj in objecten if obj.soort == "token"),
        key=lambda obj: obj.id,
    )
    regels = ["/* Gegenereerd door Beckeringh Palace. Niet handmatig wijzigen. */", ":root {"]
    for token in tokens:
        waarde = token.eigenschappen.get("waarde")
        if waarde is None:
            continue
        regels.append(f"  --bp-{_css_naam(token.id)}: {waarde};")
    regels.extend(["}", ""])
    return "\n".join(regels)
