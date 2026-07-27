"""HTML-catalogusrenderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import html
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.component_css_identity import componentklasse, variantklasse
from compiler.design_components import verzamel_componenten
from compiler.design_variants import resolveer_varianten


def naar_component_html(objecten: Iterable[Architectuurobject]) -> str:
    objecten = tuple(objecten)
    varianten_per_component = {}
    for variant in resolveer_varianten(objecten):
        varianten_per_component.setdefault(variant.component_id, []).append(variant)

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
                (
                    f'    <section class="{componentklasse(component.id)}" '
                    f'data-component="{html.escape(component.id)}">'
                ),
                f"      <h2>{html.escape(component.naam)}</h2>",
                f"      <p>{html.escape(component.doel)}</p>",
                "    </section>",
            ]
        )
        for variant in varianten_per_component.get(component.id, ()):
            regels.extend(
                [
                    (
                        f'    <section class="{componentklasse(component.id)} '
                        f'{variantklasse(variant.id)}" '
                        f'data-component="{html.escape(component.id)}" '
                        f'data-variant="{html.escape(variant.id)}" '
                        f'data-appearance="{html.escape(variant.appearance_id)}">'
                    ),
                    f"      <h2>{html.escape(variant.naam)}</h2>",
                    f"      <p>{html.escape(variant.doel)}</p>",
                    "    </section>",
                ]
            )
    regels.extend(["  </main>", "</body>", "</html>", ""])
    return "\n".join(regels)
