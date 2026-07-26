"""HTML-catalogusrenderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import html
import re
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_components import verzamel_componenten


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "component"


def naar_component_html(objecten: Iterable[Architectuurobject]) -> str:
    regels = [
        "<!doctype html>",
        '<html lang="nl">',
        "<head>",
        '  <meta charset="utf-8">',
        "  <title>Beckeringh Palace componenten</title>",
        '  <link rel="stylesheet" href="tokens.css">',
        '  <link rel="stylesheet" href="components.css">',
        "</head>",
        "<body>",
        "  <main>",
        "    <h1>Beckeringh Palace componenten</h1>",
    ]
    for component in verzamel_componenten(objecten):
        regels.extend(
            [
                f'    <section class="bp-{_css_naam(component.id)}">',
                f"      <h2>{html.escape(component.naam)}</h2>",
                f"      <p>{html.escape(component.doel)}</p>",
                "    </section>",
            ]
        )
    regels.extend(["  </main>", "</body>", "</html>", ""])
    return "\n".join(regels)
