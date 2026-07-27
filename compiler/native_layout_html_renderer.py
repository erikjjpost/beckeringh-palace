"""HTML-vertaling van gevalideerde native layoutintentie."""
from __future__ import annotations

import html
import re

from compiler.component_css_identity import componentklasse, variantklasse
from compiler.design_compositions import ResolvedComposition
from compiler.layout_model import (
    LayoutDirection,
    LayoutType,
    ResolvedLayout,
    ResolvedRegion,
)


def _css_naam(identifier: str) -> str:
    naam = re.sub(r"[^a-zA-Z0-9_-]+", "-", identifier).strip("-").lower()
    return naam or "object"


def _layout_css(layout: ResolvedLayout) -> tuple[str, ...]:
    if layout.type is LayoutType.GRID:
        return (
            "display:grid",
            f"grid-template-columns:repeat({layout.columns},minmax(0,1fr))",
            f"grid-template-rows:repeat({layout.rows},minmax(0,1fr))",
        )
    if layout.type is LayoutType.STACK:
        return (
            "display:flex",
            f"flex-direction:{_flex_direction(layout.direction)}",
        )
    if layout.type is LayoutType.FLOW:
        return (
            "display:flex",
            f"flex-direction:{_flex_direction(layout.direction)}",
            f"flex-wrap:{'wrap' if layout.wrap else 'nowrap'}",
        )
    return ("display:grid",)


def _flex_direction(direction: LayoutDirection | None) -> str:
    if direction is LayoutDirection.HORIZONTAL:
        return "row"
    if direction is LayoutDirection.VERTICAL:
        return "column"
    raise ValueError("Gevalideerde stack- of flow-layout vereist een richting")


def _region_css(layout: ResolvedLayout, region: ResolvedRegion) -> tuple[str, ...]:
    if layout.type is LayoutType.GRID:
        return (
            f"grid-column:{region.column} / span {region.column_span}",
            f"grid-row:{region.row} / span {region.row_span}",
        )
    if layout.type is LayoutType.LAYER:
        return (
            "grid-area:1 / 1",
            f"z-index:{region.layer}",
        )
    return ()


def _style(regels: tuple[str, ...]) -> str:
    return ";".join(regels)


def naar_native_layout_html(
    compositie: ResolvedComposition,
    layout: ResolvedLayout,
    titel: str = "Beckeringh Palace product",
) -> str:
    """Vertaal resolved inhoud en layout deterministisch naar HTML en CSS."""

    regions_per_instantie = {
        region.instance_id: region
        for region in layout.regions
    }
    instance_ids = tuple(instantie.id for instantie in compositie.instances)
    if (
        len(regions_per_instantie) != len(layout.regions)
        or set(regions_per_instantie) != set(instance_ids)
    ):
        raise ValueError(
            f"Compositie '{compositie.id}' en layout '{layout.id}' vereisen "
            "exact dezelfde componentinstanties"
        )
    geordende_plaatsingen = tuple(
        (instantie, regions_per_instantie[instantie.id])
        for instantie in compositie.instances
    )

    regels = [
        "<!doctype html>",
        '<html lang="nl">',
        "<head>",
        '  <meta charset="utf-8">',
        f"  <title>{html.escape(titel)}</title>",
        '  <link rel="stylesheet" href="tokens.css">',
        '  <link rel="stylesheet" href="components.css">',
        "  <style>",
        "    .bp-layout { box-sizing: border-box; }",
        "    .bp-region { box-sizing: border-box; }",
        "  </style>",
        "</head>",
        "<body>",
        f"  <header><h1>{html.escape(layout.naam)}</h1></header>",
        (
            f'  <main class="bp-layout bp-layout-{_css_naam(layout.id)}" '
            f'data-layout-type="{layout.type.value}" '
            f'style="{_style(_layout_css(layout))}">'
        ),
    ]
    for instantie, region in geordende_plaatsingen:
        region_style = _style(_region_css(layout, region))
        style_attribute = f' style="{region_style}"' if region_style else ""
        variant_class = (
            f" {variantklasse(instantie.variant_id)}"
            if instantie.variant_id is not None
            else ""
        )
        variant_attribute = (
            f' data-variant="{html.escape(instantie.variant_id)}"'
            if instantie.variant_id is not None
            else ""
        )
        appearance_attribute = (
            f' data-appearance="{html.escape(instantie.appearance_id)}"'
            if instantie.appearance_id is not None
            else ""
        )
        regels.extend([
            (
                f'    <section class="bp-region {componentklasse(instantie.component_id)}'
                f'{variant_class}" '
                f'data-region="{html.escape(region.id)}" '
                f'data-instance="{html.escape(instantie.id)}" '
                f'data-component="{html.escape(instantie.component_id)}"'
                f"{variant_attribute}{appearance_attribute}{style_attribute}>"
            ),
            f"      <h2>{html.escape(instantie.naam)}</h2>",
        ])
        if instantie.metric_value is not None:
            regels.append(
                f'      <p class="bp-metric" '
                f'data-metric-kind="{html.escape(instantie.metric_kind or "")}">'
                f"{instantie.metric_value}</p>"
            )
        regels.extend([
            f'      <p class="bp-description">{html.escape(instantie.doel)}</p>',
            "    </section>",
        ])
    regels.extend([
        "  </main>",
        "</body>",
        "</html>",
        "",
    ])
    return "\n".join(regels)
