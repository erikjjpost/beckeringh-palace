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
from compiler.component_examples import (
    ResolvedComponentExample,
    resolveer_componentvoorbeelden,
)
from compiler.design_components import DesignComponent
from compiler.design_components import verzamel_componenten
from compiler.design_variants import (
    ResolvedComponentVariant,
    resolveer_varianten,
)
from compiler.theme_css import theme_variable_lines
from compiler.theme_resolution import resolveer_alle_themas


def _voorbeeld_attributen(
    component: DesignComponent,
    variant: ResolvedComponentVariant,
    example: ResolvedComponentExample,
    state: str,
    appearance_id: str,
) -> str:
    state_class = f" {stateklasse(state)}" if state != "rest" else ""
    state_names = " ".join(
        state_name for state_name, _ in variant.state_appearances
    )
    return (
        f'class="{componentklasse(component.id)} '
        f'{variantklasse(variant.id)}{state_class}" '
        f'data-example="{html.escape(example.id)}" '
        f'data-component="{html.escape(component.id)}" '
        f'data-component-role="{html.escape(example.component_role)}" '
        f'data-component-anatomy="'
        f'{html.escape(" ".join(example.component_anatomy))}" '
        f'data-variant="{html.escape(variant.id)}" '
        f'data-component-state="{html.escape(state)}" '
        f'data-component-states="{html.escape(state_names)}" '
        f'data-appearance="{html.escape(appearance_id)}"'
    )


def _voorbeeld_html(
    component: DesignComponent,
    variant: ResolvedComponentVariant,
    example: ResolvedComponentExample,
    state: str,
    appearance_id: str,
) -> list[str]:
    attributen = _voorbeeld_attributen(
        component,
        variant,
        example,
        state,
        appearance_id,
    )
    titel = (
        example.naam
        if state == "rest"
        else f"{example.naam} · {state}"
    )
    regels = [
        '    <section class="bp-component-example-shell">',
        f"      <h2>{html.escape(titel)}</h2>",
        f"      <p>{html.escape(example.doel)}</p>",
    ]
    disabled = state == "disabled"
    if example.component_role == "actie":
        disabled_attribute = " disabled" if disabled else ""
        regels.append(
            f'      <button type="button" {attributen}'
            f"{disabled_attribute}>"
            f"{html.escape(example.label)}</button>"
        )
    elif example.component_role == "invoer":
        disabled_attribute = " disabled" if disabled else ""
        regels.extend([
            '      <label class="bp-component-example bp-example-input">',
            (
                '        <span class="bp-example-label">'
                f"{html.escape(example.label)}</span>"
            ),
            (
                f"        <input {attributen} "
                f'value="{html.escape(example.waarde or "")}"'
                f"{disabled_attribute}>"
            ),
        ])
        if example.melding is not None:
            regels.append(
                '        <small class="bp-example-message">'
                f"{html.escape(example.melding)}</small>"
            )
        regels.append("      </label>")
    elif example.component_role == "status":
        regels.append(
            f"      <output {attributen}>"
            f"{html.escape(example.label)} · "
            f"{html.escape(example.waarde or '')}</output>"
        )
    elif example.component_role == "app-tegel":
        disabled_attribute = ' aria-disabled="true"' if disabled else ""
        regels.extend([
            f"      <article {attributen}{disabled_attribute}>",
            "        <div>",
            f"          <strong>{html.escape(example.label)}</strong>",
            f"          <p>{html.escape(example.beschrijving or '')}</p>",
            "        </div>",
            f"        <small>{html.escape(example.status or '')}</small>",
            "      </article>",
        ])
    elif example.component_role == "statistiek":
        regels.extend([
            f"      <article {attributen}>",
            f"        <small>{html.escape(example.label)}</small>",
            f"        <strong>{html.escape(example.waarde or '')}</strong>",
        ])
        if example.beschrijving is not None:
            regels.append(
                f"        <p>{html.escape(example.beschrijving)}</p>"
            )
        regels.append("      </article>")
    else:
        regels.extend([
            f"      <section {attributen}>",
            f"        <h3>{html.escape(example.label)}</h3>",
            "      </section>",
        ])
    regels.append("    </section>")
    return regels


def naar_component_html(objecten: Iterable[Architectuurobject]) -> str:
    objecten = tuple(objecten)
    themas = resolveer_alle_themas(objecten)
    thema = themas[0] if len(themas) == 1 else None
    componenten = verzamel_componenten(objecten)
    varianten = resolveer_varianten(objecten)
    voorbeelden = resolveer_componentvoorbeelden(objecten)
    varianten_per_component = {}
    for variant in varianten:
        varianten_per_component.setdefault(variant.component_id, []).append(variant)
    voorbeelden_per_variant = {}
    for example in voorbeelden:
        voorbeelden_per_variant.setdefault(example.variant_id, []).append(example)
    componenten_met_voorbeelden = {
        example.component_id for example in voorbeelden
    }

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
            "    .bp-component-example-shell {",
            "      display: grid;",
            "      gap: var(--bp-spacing-small);",
            "    }",
            "    .bp-component-example {",
            "      display: grid;",
            "      gap: var(--bp-spacing-small);",
            "    }",
            "    .bp-example-label, .bp-example-message {",
            "      font-family: var(--bp-font-body);",
            "      font-size: var(--bp-type-caption);",
            "    }",
            "    .bp-example-message {",
            "      color: var(--bp-theme-error);",
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
    for component in componenten:
        if component.id in componenten_met_voorbeelden:
            regels.extend([
                (
                    '    <section class="bp-component-family" '
                    f'data-component-family="{html.escape(component.id)}">'
                ),
                f"      <h2>{html.escape(component.naam)}</h2>",
                f"      <p>{html.escape(component.doel)}</p>",
                "    </section>",
            ])
        else:
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
            variant_examples = voorbeelden_per_variant.get(variant.id, ())
            if variant_examples:
                for example in variant_examples:
                    for state, appearance_id in variant.state_appearances:
                        regels.extend(_voorbeeld_html(
                            component,
                            variant,
                            example,
                            state,
                            appearance_id,
                        ))
                continue
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
