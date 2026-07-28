"""HTML-catalogusrenderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import html
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.component_css_identity import (
    componentklasse,
    stateklasse,
    variantklasse,
)
from compiler.design_components import verzamel_componenten
from compiler.design_variants import resolveer_varianten
from compiler.theme_css import theme_variable_lines
from compiler.theme_resolution import resolveer_alle_themas


def naar_component_html(objecten: Iterable[Architectuurobject]) -> str:
    objecten = tuple(objecten)
    themas = resolveer_alle_themas(objecten)
    thema = themas[0] if len(themas) == 1 else None
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
    ]
    if thema is not None:
        regels.extend([
            "  <style>",
            *theme_variable_lines(thema, indent="    "),
            "    body {",
            "      margin: 0;",
            "      padding: var(--bp-spacing-large);",
            "      background: var(--bp-theme-background);",
            "      color: var(--bp-theme-foreground);",
            "      font-family: var(--bp-font-body);",
            "    }",
            "    main {",
            "      display: grid;",
            "      gap: var(--bp-spacing-medium);",
            "    }",
            "  </style>",
        ])
    body = (
        f'<body data-world="{html.escape(thema.wereld_id)}" '
        f'data-theme="{html.escape(thema.thema_id)}">'
        if thema is not None
        else "<body>"
    )
    regels.extend([
        "</head>",
        body,
        "  <main>",
        "    <h1>Beckeringh Palace componenten</h1>",
    ])
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
            state_names = " ".join(
                state for state, _ in variant.state_appearances
            )
            for state, appearance_id in variant.state_appearances:
                state_class = (
                    f" {stateklasse(state)}"
                    if state != "rest"
                    else ""
                )
                disabled_attribute = (
                    ' aria-disabled="true"'
                    if state == "disabled"
                    else ""
                )
                titel = (
                    variant.naam
                    if state == "rest"
                    else f"{variant.naam} · {state}"
                )
                doel = (
                    variant.doel
                    if state == "rest"
                    else (
                        f"Toestand {state} via appearance "
                        f"{appearance_id}."
                    )
                )
                regels.extend(
                    [
                        (
                            f'    <section class="{componentklasse(component.id)} '
                            f'{variantklasse(variant.id)}{state_class}" '
                            f'data-component="{html.escape(component.id)}" '
                            f'data-variant="{html.escape(variant.id)}" '
                            f'data-component-state="{html.escape(state)}" '
                            f'data-component-states="{html.escape(state_names)}" '
                            f'data-appearance="{html.escape(appearance_id)}"'
                            f"{disabled_attribute}>"
                        ),
                        f"      <h2>{html.escape(titel)}</h2>",
                        f"      <p>{html.escape(doel)}</p>",
                        "    </section>",
                    ]
                )
    regels.extend(["  </main>", "</body>", "</html>", ""])
    return "\n".join(regels)
