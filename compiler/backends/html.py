"""HTML-backendplugin voor native, theme-driven producten."""
from __future__ import annotations

from collections.abc import Iterable

from compiler.backend import Backend
from compiler.cir import Architectuurobject
from compiler.native_layout_html_renderer import naar_native_layout_html
from compiler.product_model import ProductDefinition, SNAPSHOT_ID_LENGTH


def _css_string(waarde: str) -> str:
    return '"' + waarde.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _theme_css(product: ProductDefinition) -> str:
    thema = product.thema
    if thema is None:
        return ""

    regels = ["    :root {"]
    for rol, kleur in thema.palet.kleuren:
        regels.append(f"      --bp-theme-{rol}: {kleur.waarde};")
    regels.extend([
        f"      --bp-font-heading: {_css_string(thema.typografie.heading)};",
        f"      --bp-font-body: {_css_string(thema.typografie.body)};",
        f"      --bp-font-mono: {_css_string(thema.typografie.mono)};",
    ])

    if thema.typeschaal is not None:
        regels.extend([
            f"      --bp-type-display: {thema.typeschaal.display};",
            f"      --bp-type-title: {thema.typeschaal.title};",
            f"      --bp-type-heading: {thema.typeschaal.heading};",
            f"      --bp-type-body: {thema.typeschaal.body};",
            f"      --bp-type-label: {thema.typeschaal.label};",
            f"      --bp-type-caption: {thema.typeschaal.caption};",
        ])
    if thema.materiaal is not None:
        for rol, kleur in thema.materiaal.kleuren:
            regels.append(f"      --bp-material-{rol}: {kleur.waarde};")
    if thema.border is not None:
        regels.extend([
            f"      --bp-border-hairline: {thema.border.hairline};",
            f"      --bp-border-regular: {thema.border.regular};",
            f"      --bp-border-strong: {thema.border.strong};",
            f"      --bp-border-style: {thema.border.style};",
        ])
    if thema.radius is not None:
        regels.extend([
            f"      --bp-radius-small: {thema.radius.small};",
            f"      --bp-radius-medium: {thema.radius.medium};",
            f"      --bp-radius-large: {thema.radius.large};",
            f"      --bp-radius-pill: {thema.radius.pill};",
        ])
    if thema.shadow is not None:
        regels.extend([
            f"      --bp-shadow-low: {thema.shadow.low};",
            f"      --bp-shadow-medium: {thema.shadow.medium};",
            f"      --bp-shadow-high: {thema.shadow.high};",
        ])
    if thema.motion is not None:
        regels.extend([
            f"      --bp-motion-fast: {thema.motion.fast};",
            f"      --bp-motion-normal: {thema.motion.normal};",
            f"      --bp-motion-slow: {thema.motion.slow};",
            f"      --bp-motion-easing: {thema.motion.easing};",
        ])
    if thema.spacing is not None:
        regels.extend([
            f"      --bp-spacing-none: {thema.spacing.none};",
            f"      --bp-spacing-xs: {thema.spacing.xs};",
            f"      --bp-spacing-small: {thema.spacing.small};",
            f"      --bp-spacing-medium: {thema.spacing.medium};",
            f"      --bp-spacing-large: {thema.spacing.large};",
            f"      --bp-spacing-xl: {thema.spacing.xl};",
        ])

    regels.extend([
        "    }",
        "    body {",
        "      margin: 0;",
        "      min-height: 100vh;",
        "      padding: var(--bp-spacing-xl);",
        "      box-sizing: border-box;",
        "      background: var(--bp-theme-background);",
        "      color: var(--bp-theme-foreground);",
        "      font-family: var(--bp-font-body);",
        "    }",
        "    h1, h2, h3, h4, h5, h6 { font-family: var(--bp-font-heading); }",
        "    code, pre, kbd, samp { font-family: var(--bp-font-mono); }",
        "    .bp-product-header {",
        "      max-width: 72rem;",
        "      margin-bottom: var(--bp-spacing-xl);",
        "      padding: var(--bp-spacing-large);",
        "      box-sizing: border-box;",
        "      background: var(--bp-material-surface);",
        "      border-left: var(--bp-border-strong) var(--bp-border-style) var(--bp-material-accent);",
        "      border-radius: var(--bp-radius-medium);",
        "    }",
        "    .bp-product-kicker {",
        "      margin: 0 0 var(--bp-spacing-small);",
        "      color: var(--bp-theme-accent);",
        "      font-size: var(--bp-type-label);",
        "      font-weight: 700;",
        "      letter-spacing: .08em;",
        "      text-transform: uppercase;",
        "    }",
        "    .bp-product-header h1 {",
        "      margin: 0;",
        "      font-size: var(--bp-type-title);",
        "    }",
        "    .bp-product-purpose {",
        "      margin: var(--bp-spacing-small) 0 0;",
        "      color: var(--bp-material-muted);",
        "      font-size: var(--bp-type-body);",
        "    }",
        "    .bp-layout { gap: var(--bp-spacing-medium); }",
        "    .bp-region { padding: var(--bp-spacing-large); }",
        "    .bp-region h2 { margin-top: 0; }",
        "    @media (max-width: 960px) {",
        "      body { padding: var(--bp-spacing-large); }",
        "      .bp-layout { grid-template-columns: 1fr !important; }",
        "      .bp-region { grid-column: 1 !important; grid-row: auto !important; }",
        "    }",
    ])

    if thema.materiaal is not None:
        regels.append("    .bp-canvas { background: var(--bp-material-canvas); }")
    if all((thema.materiaal, thema.border, thema.radius, thema.shadow, thema.motion)):
        regels.extend([
            "    .bp-region {",
            "      background: var(--bp-material-raised);",
            "      color: var(--bp-material-foreground);",
            "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
            "      border-radius: var(--bp-radius-medium);",
            "      box-shadow: var(--bp-shadow-low);",
            "      transition: box-shadow var(--bp-motion-normal) var(--bp-motion-easing);",
            "    }",
            "    .bp-metric {",
            "      margin: var(--bp-spacing-small) 0;",
            "      color: var(--bp-material-accent);",
            "      font-family: var(--bp-font-heading);",
            "      font-size: calc(var(--bp-type-heading) * 2);",
            "      font-weight: 700;",
            "      line-height: 1;",
            "    }",
            "    .bp-description {",
            "      margin: var(--bp-spacing-small) 0 0;",
            "      color: var(--bp-material-muted);",
            "      font-size: var(--bp-type-body);",
            "    }",
            "    .bp-metric-details {",
            "      display: grid;",
            "      gap: var(--bp-spacing-xs);",
            "      margin: var(--bp-spacing-small) 0;",
            "      padding: 0;",
            "      list-style: none;",
            "      color: var(--bp-material-muted);",
            "      font-size: var(--bp-type-caption);",
            "    }",
            "    .bp-metric-details li {",
            "      display: flex;",
            "      justify-content: space-between;",
            "      gap: var(--bp-spacing-small);",
            "      border-bottom: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
            "    }",
            "    .bp-metric-detail-value {",
            "      color: var(--bp-material-foreground);",
            "      font-weight: 700;",
            "    }",
        ])

    return "\n".join(regels) + "\n"


def _render(
    objecten: Iterable[Architectuurobject],
    product: ProductDefinition,
) -> str:
    if product.opgeloste_layout is None:
        raise ValueError(
            f"Product '{product.id}' vereist een opgeloste native layout"
        )
    if product.opgeloste_compositie is None:
        raise ValueError(
            f"Product '{product.id}' vereist een opgeloste native compositie"
        )
    inhoud = naar_native_layout_html(
        product.opgeloste_compositie,
        product.opgeloste_layout,
        titel=product.naam,
        wereld_naam=product.thema.wereld_naam if product.thema else None,
        thema_naam=product.thema.thema_naam if product.thema else None,
        mode_label=product.mode_label,
        snapshot_label=(
            f"Snapshot {product.snapshot_id[:SNAPSHOT_ID_LENGTH]}"
            if product.snapshot_id
            else None
        ),
    )
    if product.thema is None:
        return inhoud

    thema = product.thema
    snapshot_attribuut = (
        f' data-snapshot-id="{product.snapshot_id}"'
        f' data-snapshot-ref="{product.snapshot_ref}"'
        if product.snapshot_id
        else ""
    )
    inhoud = inhoud.replace("  <style>\n", "  <style>\n" + _theme_css(product), 1)
    inhoud = inhoud.replace(
        "<body>",
        f'<body data-world="{thema.wereld_id}" data-theme="{thema.thema_id}" '
        f'data-product-mode="{product.mode}" '
        f'data-time-context="{"applicable" if product.has_time_context else "none"}"'
        f"{snapshot_attribuut}>",
        1,
    )
    return inhoud


backend = Backend("html", _render)
