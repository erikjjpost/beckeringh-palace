"""HTML-vertaling van een opgeloste designsystemreferentie."""
from __future__ import annotations

import html

from compiler.component_css_identity import (
    componentklasse,
    stateklasse,
    variantklasse,
)
from compiler.component_html_renderer import (
    accessibility_attributes,
    render_component_example,
)
from compiler.design_system_reference import (
    ResolvedDesignSystemReference,
    ResolvedReferenceSection,
)
from compiler.theme_resolution import ResolvedTheme


def reference_css_lines() -> tuple[str, ...]:
    """Lever uitsluitend structurele CSS voor het referentieproduct."""

    return (
        "    .bp-reference-navigation {",
        "      margin-bottom: var(--bp-spacing-large);",
        "      padding: var(--bp-spacing-medium);",
        "      background: var(--bp-material-surface);",
        "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "      border-radius: var(--bp-radius-medium);",
        "    }",
        "    .bp-reference-navigation ol {",
        "      display: flex;",
        "      flex-wrap: wrap;",
        "      gap: var(--bp-spacing-small);",
        "      margin: 0;",
        "      padding: 0;",
        "      list-style: none;",
        "    }",
        "    .bp-reference-navigation a {",
        "      display: inline-flex;",
        "      padding: var(--bp-spacing-small) var(--bp-spacing-medium);",
        "      color: var(--bp-material-interaction);",
        "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "      border-radius: var(--bp-radius-pill);",
        "      text-decoration: none;",
        "    }",
        "    .bp-reference-navigation a:focus-visible {",
        "      outline: none;",
        "      box-shadow: var(--bp-shadow-focus);",
        "    }",
        "    .bp-reference-content {",
        "      display: grid;",
        "      gap: var(--bp-spacing-xl);",
        "    }",
        "    .bp-reference-section {",
        "      scroll-margin-top: var(--bp-spacing-large);",
        "      padding-top: var(--bp-spacing-large);",
        "      border-top: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "    }",
        "    .bp-reference-section-header {",
        "      margin-bottom: var(--bp-spacing-medium);",
        "    }",
        "    .bp-reference-section-index {",
        "      color: var(--bp-material-interaction);",
        "      font-family: var(--bp-font-mono);",
        "      font-size: var(--bp-type-caption);",
        "      letter-spacing: .18em;",
        "    }",
        "    .bp-reference-grid, .bp-reference-examples {",
        "      display: grid;",
        "      grid-template-columns: repeat(2, minmax(0, 1fr));",
        "      gap: var(--bp-spacing-medium);",
        "    }",
        "    .bp-reference-card, .bp-component-example-shell {",
        "      padding: var(--bp-spacing-medium);",
        "      background: var(--bp-material-raised);",
        "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "      border-radius: var(--bp-radius-medium);",
        "    }",
        "    .bp-reference-card h4, .bp-component-example-shell h4 {",
        "      margin-top: 0;",
        "    }",
        "    .bp-reference-properties {",
        "      display: grid;",
        "      gap: var(--bp-spacing-xs);",
        "      margin: 0;",
        "    }",
        "    .bp-reference-properties div {",
        "      display: grid;",
        "      grid-template-columns: minmax(8rem, .65fr) 1.35fr;",
        "      gap: var(--bp-spacing-small);",
        "      padding-bottom: var(--bp-spacing-xs);",
        "      border-bottom: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "    }",
        "    .bp-reference-properties dt { color: var(--bp-material-muted); }",
        "    .bp-reference-properties dd { margin: 0; overflow-wrap: anywhere; }",
        "    .bp-reference-table-wrap { overflow-x: auto; }",
        "    .bp-reference-table { width: 100%; border-collapse: collapse; }",
        "    .bp-reference-table th, .bp-reference-table td {",
        "      padding: var(--bp-spacing-small);",
        "      border-bottom: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "      text-align: left;",
        "      vertical-align: top;",
        "    }",
        "    .bp-reference-table th { color: var(--bp-material-muted); }",
        "    .bp-reference-state-examples {",
        "      display: grid;",
        "      gap: var(--bp-spacing-small);",
        "      margin-top: var(--bp-spacing-medium);",
        "    }",
        "    .bp-reference-swatch {",
        "      display: inline-block;",
        "      width: 1rem;",
        "      height: 1rem;",
        "      margin-right: var(--bp-spacing-xs);",
        "      background: var(--bp-reference-color);",
        "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "      border-radius: var(--bp-radius-small);",
        "      vertical-align: middle;",
        "    }",
        "    .bp-component-example-shell { display: grid; gap: var(--bp-spacing-small); }",
        "    .bp-component-example { display: grid; gap: var(--bp-spacing-small); }",
        "    .bp-example-label, .bp-example-message {",
        "      font-family: var(--bp-font-body);",
        "      font-size: var(--bp-type-caption);",
        "    }",
        "    .bp-example-description { font-size: var(--bp-type-body); }",
        "    .bp-example-message { color: var(--bp-theme-error); }",
        "    @media (max-width: 960px) {",
        "      .bp-reference-grid, .bp-reference-examples { grid-template-columns: 1fr; }",
        "      .bp-reference-properties div { grid-template-columns: 1fr; }",
        "    }",
    )


def _properties(
    title: str,
    primitive_kind: str,
    values: tuple[tuple[str, str], ...],
    colors: frozenset[str] = frozenset(),
) -> list[str]:
    regels = [
        (
            '<article class="bp-reference-card" '
            f'data-primitive-kind="{html.escape(primitive_kind)}">'
        ),
        f"  <h4>{html.escape(title)}</h4>",
        '  <dl class="bp-reference-properties">',
    ]
    for name, value in values:
        swatch = (
            f'<span class="bp-reference-swatch" '
            f'style="--bp-reference-color:{html.escape(value)}"></span>'
            if name in colors
            else ""
        )
        regels.extend([
            "    <div>",
            f"      <dt>{html.escape(name)}</dt>",
            f"      <dd>{swatch}<code>{html.escape(value)}</code></dd>",
            "    </div>",
        ])
    regels.extend(["  </dl>", "</article>"])
    return regels


def _primitive_lines(theme: ResolvedTheme) -> list[str]:
    regels = ['<div class="bp-reference-grid">']
    palette_values = tuple(
        (role, color.waarde) for role, color in theme.palet.kleuren
    )
    regels.extend(_properties(
        theme.palet.naam,
        "palette",
        palette_values,
        frozenset(role for role, _ in palette_values),
    ))
    regels.extend(_properties(
        theme.typografie.naam,
        "typography",
        (
            ("heading", ", ".join(theme.typografie.heading)),
            ("body", ", ".join(theme.typografie.body)),
            ("mono", ", ".join(theme.typografie.mono)),
            ("delivery", theme.typografie.levering),
        ),
    ))
    if theme.typeschaal is not None:
        regels.extend(_properties(
            theme.typeschaal.naam,
            "type-scale",
            tuple(
                (role, getattr(theme.typeschaal, role))
                for role in (
                    "display",
                    "title",
                    "heading",
                    "body",
                    "label",
                    "caption",
                )
            ),
        ))
    if theme.materiaal is not None:
        material_values = tuple(
            (role, color.waarde) for role, color in theme.materiaal.kleuren
        )
        regels.extend(_properties(
            theme.materiaal.naam,
            "material",
            material_values,
            frozenset(role for role, _ in material_values),
        ))
    if theme.border is not None:
        regels.extend(_properties(
            theme.border.naam,
            "border",
            (
                ("hairline", theme.border.hairline),
                ("regular", theme.border.regular),
                ("strong", theme.border.strong),
                ("style", theme.border.style),
            ),
        ))
    if theme.radius is not None:
        regels.extend(_properties(
            theme.radius.naam,
            "radius",
            (
                ("small", theme.radius.small),
                ("control", theme.radius.control or ""),
                ("medium", theme.radius.medium),
                ("large", theme.radius.large),
                ("pill", theme.radius.pill),
            ),
        ))
    if theme.shadow is not None:
        regels.extend(_properties(
            theme.shadow.naam,
            "shadow",
            (
                ("none", theme.shadow.none or ""),
                ("low", theme.shadow.low),
                ("medium", theme.shadow.medium),
                ("high", theme.shadow.high),
                ("glow", theme.shadow.glow or ""),
                ("focus", theme.shadow.focus or ""),
                ("glow-accent", theme.shadow.glow_accent or ""),
            ),
        ))
    if theme.motion is not None:
        regels.extend(_properties(
            theme.motion.naam,
            "motion",
            (
                ("fast", theme.motion.fast),
                ("normal", theme.motion.normal),
                ("slow", theme.motion.slow),
                ("easing", theme.motion.easing),
                ("rest-offset", theme.motion.rest_offset or ""),
                ("hover-offset", theme.motion.hover_offset or ""),
            ),
        ))
    if theme.spacing is not None:
        regels.extend(_properties(
            theme.spacing.naam,
            "spacing",
            tuple(
                (role, getattr(theme.spacing, role))
                for role in ("none", "xs", "small", "medium", "large", "xl")
            ),
        ))
    if theme.artdirection is not None:
        art = theme.artdirection
        regels.extend(_properties(
            art.naam,
            "art-direction",
            (
                ("canvas", f"{art.canvas_role}: {art.canvas.waarde}"),
                (
                    "interaction",
                    f"{art.interaction_role}: {art.interaction.waarde}",
                ),
                (
                    "warm-accent",
                    f"{art.warm_accent_role}: {art.warm_accent.waarde}",
                ),
                ("warm-accent-limit", str(art.warm_accent_limit)),
                ("glow", art.glow),
                ("ornament", art.ornament),
                ("density", art.density),
                ("imagery", art.imagery),
            ),
        ))
    regels.append("</div>")
    return regels


def _token_lines(reference: ResolvedDesignSystemReference) -> list[str]:
    regels = [
        '<div class="bp-reference-table-wrap">',
        '<table class="bp-reference-table">',
        "  <thead><tr><th>Token</th><th>Type</th><th>Waarde</th><th>Doel</th></tr></thead>",
        "  <tbody>",
    ]
    for token in reference.tokens:
        regels.append(
            f'    <tr data-token="{html.escape(token.id)}">'
            f"<td><code>{html.escape(token.id)}</code></td>"
            f"<td>{html.escape(token.type.value)}</td>"
            f"<td><code>{html.escape(token.waarde)}</code></td>"
            f"<td>{html.escape(token.doel)}</td></tr>"
        )
    regels.extend(["  </tbody>", "</table>", "</div>"])
    return regels


def _state_lines(reference: ResolvedDesignSystemReference) -> list[str]:
    components = {component.id: component for component in reference.components}
    appearances = {
        appearance.id: appearance for appearance in reference.appearances
    }
    accessibility = {
        contract.component_id: contract
        for contract in reference.accessibility
    }
    examples_per_variant = {}
    for example in reference.examples:
        examples_per_variant.setdefault(example.variant_id, []).append(example)
    regels = ['<div class="bp-reference-grid">']
    for variant in reference.variants:
        component = components[variant.component_id]
        state_names = " ".join(
            state for state, _ in variant.state_appearances
        )
        regels.extend([
            (
                '<article class="bp-reference-card" '
                f'data-state-family="{html.escape(variant.id)}" '
                f'data-component="{html.escape(component.id)}">'
            ),
            f"  <h4>{html.escape(variant.naam)}</h4>",
            f"  <p>{html.escape(variant.doel)}</p>",
            '  <div class="bp-reference-table-wrap">',
            '    <table class="bp-reference-table">',
            "      <thead><tr><th>Toestand</th><th>Appearance</th><th>Doel</th></tr></thead>",
            "      <tbody>",
        ])
        for state, appearance_id in variant.state_appearances:
            appearance = appearances[appearance_id]
            regels.append(
                f'        <tr data-state-reference="{html.escape(variant.id)}:{html.escape(state)}">'
                f"<td><code>{html.escape(state)}</code></td>"
                f"<td><code>{html.escape(appearance_id)}</code></td>"
                f"<td>{html.escape(appearance.doel)}</td></tr>"
            )
        regels.extend([
            "      </tbody>",
            "    </table>",
            "  </div>",
            '  <div class="bp-reference-state-examples">',
        ])
        for state, appearance_id in variant.state_appearances:
            examples = examples_per_variant.get(variant.id, ())
            if examples:
                for example in examples:
                    rendered = render_component_example(
                        component,
                        variant,
                        example,
                        state,
                        appearance_id,
                        heading_level=5,
                        id_namespace="state",
                    )
                    regels.extend(
                        f"    {line[4:] if line.startswith('    ') else line}"
                        for line in rendered
                    )
                continue
            state_class = (
                f" {stateklasse(state)}" if state != "rest" else ""
            )
            regels.extend([
                (
                    f'    <section class="{componentklasse(component.id)} '
                    f'{variantklasse(variant.id)}{state_class}" '
                    f'data-component="{html.escape(component.id)}" '
                    f'data-variant="{html.escape(variant.id)}" '
                    f'data-component-state="{html.escape(state)}" '
                    f'data-component-states="{html.escape(state_names)}" '
                    f'data-appearance="{html.escape(appearance_id)}"'
                    f"{accessibility_attributes(accessibility.get(component.id))}>"
                ),
                (
                    f"      <h5>{html.escape(variant.naam)} · "
                    f"{html.escape(state)}</h5>"
                ),
                (
                    f"      <p>{html.escape(appearances[appearance_id].doel)}</p>"
                ),
                "    </section>",
            ])
        regels.extend(["  </div>", "</article>"])
    regels.append("</div>")
    return regels


def _example_lines(reference: ResolvedDesignSystemReference) -> list[str]:
    components = {component.id: component for component in reference.components}
    variants = {variant.id: variant for variant in reference.variants}
    regels = ['<div class="bp-reference-examples">']
    for example in reference.examples:
        variant = variants[example.variant_id]
        regels.append(
            f'<div data-reference-example="{html.escape(example.id)}">'
        )
        rendered = render_component_example(
            components[example.component_id],
            variant,
            example,
            "rest",
            variant.appearance_id,
            heading_level=4,
        )
        regels.extend(
            f"  {line[4:] if line.startswith('    ') else line}"
            for line in rendered
        )
        regels.append("</div>")
    regels.append("</div>")
    return regels


def _accessibility_lines(
    reference: ResolvedDesignSystemReference,
) -> list[str]:
    components = {component.id: component for component in reference.components}
    regels = ['<div class="bp-reference-grid">']
    for contract in reference.accessibility:
        component = components[contract.component_id]
        regels.extend([
            (
                '<article class="bp-reference-card" '
                f'data-accessibility-reference="{html.escape(contract.contract_id)}" '
                f'data-component="{html.escape(component.id)}">'
            ),
            f"  <h4>{html.escape(contract.naam)}</h4>",
            f"  <p>{html.escape(contract.doel)}</p>",
            '  <dl class="bp-reference-properties">',
        ])
        properties = (
            ("componentrol", component.rol or ""),
            ("semantische rol", contract.rol),
            ("naambron", contract.naambron),
            ("waardebron", contract.waardebron or "niet van toepassing"),
            ("foutbron", contract.foutbron or "niet van toepassing"),
            ("disabled", contract.disabled_gedrag),
            ("focus", contract.focusgedrag),
            ("toetsenbord", contract.toetsenbordgedrag),
            ("toetsen", " ".join(contract.toetsen) or "geen"),
        )
        for name, value in properties:
            regels.extend([
                "    <div>",
                f"      <dt>{html.escape(name)}</dt>",
                f"      <dd><code>{html.escape(value)}</code></dd>",
                "    </div>",
            ])
        regels.extend(["  </dl>", "</article>"])
    regels.append("</div>")
    return regels


def _section_content(
    section: ResolvedReferenceSection,
    reference: ResolvedDesignSystemReference,
    theme: ResolvedTheme,
) -> list[str]:
    if section.role == "primitieven":
        return _primitive_lines(theme)
    if section.role == "tokens":
        return _token_lines(reference)
    if section.role == "toestanden":
        return _state_lines(reference)
    if section.role == "voorbeelden":
        return _example_lines(reference)
    if section.role == "toegankelijkheid":
        return _accessibility_lines(reference)
    raise ValueError(f"Onbekende opgeloste referentiesectierol '{section.role}'")


def reference_content_lines(
    reference: ResolvedDesignSystemReference,
    theme: ResolvedTheme,
) -> tuple[str, ...]:
    """Render geordende referentiesecties als inhoud van één productinstantie."""

    regels = [
        (
            '<nav class="bp-reference-navigation" '
            'aria-label="EmberForge designsystem referentiesecties">'
        ),
        "  <ol>",
    ]
    for index, section in enumerate(reference.sections, start=1):
        regels.append(
            f'    <li><a href="#{html.escape(section.id)}" '
            f'data-reference-target="{html.escape(section.id)}">'
            f"{index:02d} · {html.escape(section.naam)}</a></li>"
        )
    regels.extend([
        "  </ol>",
        "</nav>",
        (
            '<div class="bp-reference-content" '
            f'data-reference-sections="{len(reference.sections)}">'
        ),
    ])
    for index, section in enumerate(reference.sections, start=1):
        regels.extend([
            (
                f'<section id="{html.escape(section.id)}" '
                f'data-reference-role="{html.escape(section.role)}" '
                'class="bp-reference-section">'
            ),
            '  <header class="bp-reference-section-header">',
            (
                '    <span class="bp-reference-section-index">'
                f"{index:02d}</span>"
            ),
            f"    <h3>{html.escape(section.naam)}</h3>",
            f"    <p>{html.escape(section.doel)}</p>",
            "  </header>",
        ])
        regels.extend(
            f"  {line}" if line else ""
            for line in _section_content(section, reference, theme)
        )
        regels.append("</section>")
    regels.append("</div>")
    return tuple(regels)
