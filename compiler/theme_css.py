"""Gedeelde CSS-variabelen voor één opgelost native thema."""
from __future__ import annotations

from compiler.theme_resolution import ResolvedTheme


CSS_GENERIEKE_FONTFAMILIES = frozenset({
    "-apple-system",
    "cursive",
    "emoji",
    "fangsong",
    "fantasy",
    "math",
    "monospace",
    "sans-serif",
    "serif",
    "system-ui",
    "ui-monospace",
    "ui-rounded",
    "ui-sans-serif",
    "ui-serif",
})


def _css_string(waarde: str) -> str:
    return '"' + waarde.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _css_fontstack(families: tuple[str, ...]) -> str:
    return ", ".join(
        familie
        if familie.lower() in CSS_GENERIEKE_FONTFAMILIES
        else _css_string(familie)
        for familie in families
    )


def theme_variable_lines(
    thema: ResolvedTheme,
    indent: str = "",
) -> tuple[str, ...]:
    """Vertaal alleen opgeloste themadata naar één CSS custom-propertyblok."""

    property_indent = indent + "  "
    regels = [f"{indent}:root {{"]
    for rol, kleur in thema.palet.kleuren:
        regels.append(
            f"{property_indent}--bp-theme-{rol}: {kleur.waarde};"
        )
    regels.extend([
        f"{property_indent}--bp-font-heading: "
        f"{_css_fontstack(thema.typografie.heading)};",
        f"{property_indent}--bp-font-body: "
        f"{_css_fontstack(thema.typografie.body)};",
        f"{property_indent}--bp-font-mono: "
        f"{_css_fontstack(thema.typografie.mono)};",
    ])

    if thema.typeschaal is not None:
        regels.extend([
            f"{property_indent}--bp-type-display: {thema.typeschaal.display};",
            f"{property_indent}--bp-type-title: {thema.typeschaal.title};",
            f"{property_indent}--bp-type-heading: {thema.typeschaal.heading};",
            f"{property_indent}--bp-type-body: {thema.typeschaal.body};",
            f"{property_indent}--bp-type-label: {thema.typeschaal.label};",
            f"{property_indent}--bp-type-caption: {thema.typeschaal.caption};",
        ])
    if thema.materiaal is not None:
        for rol, kleur in thema.materiaal.kleuren:
            regels.append(
                f"{property_indent}--bp-material-{rol}: {kleur.waarde};"
            )
    if thema.border is not None:
        regels.extend([
            f"{property_indent}--bp-border-hairline: {thema.border.hairline};",
            f"{property_indent}--bp-border-regular: {thema.border.regular};",
            f"{property_indent}--bp-border-strong: {thema.border.strong};",
            f"{property_indent}--bp-border-style: {thema.border.style};",
        ])
    if thema.radius is not None:
        regels.extend([
            f"{property_indent}--bp-radius-small: {thema.radius.small};",
            f"{property_indent}--bp-radius-medium: {thema.radius.medium};",
            f"{property_indent}--bp-radius-large: {thema.radius.large};",
            f"{property_indent}--bp-radius-pill: {thema.radius.pill};",
        ])
        if thema.radius.control is not None:
            regels.append(
                f"{property_indent}--bp-radius-control: "
                f"{thema.radius.control};"
            )
    if thema.shadow is not None:
        regels.extend([
            f"{property_indent}--bp-shadow-low: {thema.shadow.low};",
            f"{property_indent}--bp-shadow-medium: {thema.shadow.medium};",
            f"{property_indent}--bp-shadow-high: {thema.shadow.high};",
        ])
        if thema.shadow.none is not None:
            regels.append(
                f"{property_indent}--bp-shadow-none: {thema.shadow.none};"
            )
        if thema.shadow.glow is not None:
            regels.append(
                f"{property_indent}--bp-shadow-glow: {thema.shadow.glow};"
            )
        if thema.shadow.focus is not None:
            regels.append(
                f"{property_indent}--bp-shadow-focus: {thema.shadow.focus};"
            )
        if thema.shadow.glow_accent is not None:
            regels.append(
                f"{property_indent}--bp-shadow-glow-accent: "
                f"{thema.shadow.glow_accent};"
            )
    if thema.motion is not None:
        regels.extend([
            f"{property_indent}--bp-motion-fast: {thema.motion.fast};",
            f"{property_indent}--bp-motion-normal: {thema.motion.normal};",
            f"{property_indent}--bp-motion-slow: {thema.motion.slow};",
            f"{property_indent}--bp-motion-easing: {thema.motion.easing};",
        ])
        if thema.motion.rest_offset is not None:
            regels.append(
                f"{property_indent}--bp-motion-rest-offset: "
                f"{thema.motion.rest_offset};"
            )
        if thema.motion.hover_offset is not None:
            regels.append(
                f"{property_indent}--bp-motion-hover-offset: "
                f"{thema.motion.hover_offset};"
            )
    if thema.spacing is not None:
        regels.extend([
            f"{property_indent}--bp-spacing-none: {thema.spacing.none};",
            f"{property_indent}--bp-spacing-xs: {thema.spacing.xs};",
            f"{property_indent}--bp-spacing-small: {thema.spacing.small};",
            f"{property_indent}--bp-spacing-medium: {thema.spacing.medium};",
            f"{property_indent}--bp-spacing-large: {thema.spacing.large};",
            f"{property_indent}--bp-spacing-xl: {thema.spacing.xl};",
        ])
    if thema.artdirection is not None:
        regels.extend([
            f"{property_indent}--bp-art-canvas: "
            f"{thema.artdirection.canvas.waarde};",
            f"{property_indent}--bp-art-interaction: "
            f"{thema.artdirection.interaction.waarde};",
            f"{property_indent}--bp-art-warm-accent: "
            f"{thema.artdirection.warm_accent.waarde};",
        ])
    regels.append(f"{indent}}}")
    return tuple(regels)
