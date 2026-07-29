"""HTML-vertaling van gevalideerde native layoutintentie."""
from __future__ import annotations

import html
from collections.abc import Mapping
from pathlib import PurePosixPath
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


def _responsive_css(layout: ResolvedLayout) -> tuple[str, ...]:
    if (
        layout.type is not LayoutType.GRID
        or layout.responsive_breakpoint is None
        or layout.compact_columns is None
    ):
        return ()
    selector = f".bp-layout-{_css_naam(layout.id)}"
    regels = [
        f"    @media (max-width: {layout.responsive_breakpoint}px) {{",
        (
            f"      {selector} {{ grid-template-columns:"
            f"repeat({layout.compact_columns},minmax(0,1fr)) !important; }}"
        ),
    ]
    for region in sorted(
        layout.regions, key=lambda item: item.compact_order or 0
    ):
        regels.append(
            f"      [data-region=\"{html.escape(region.id)}\"] "
            f"{{ grid-column:1 / span {layout.compact_columns} !important; "
            f"grid-row:auto !important; order:{region.compact_order}; }}"
        )
    regels.append("    }")
    return tuple(regels)


def _style(regels: tuple[str, ...]) -> str:
    return ";".join(regels)


def naar_native_layout_html(
    compositie: ResolvedComposition,
    layout: ResolvedLayout,
    titel: str = "Beckeringh Palace product",
    wereld_naam: str | None = None,
    thema_naam: str | None = None,
    mode_label: str | None = None,
    snapshot_label: str | None = None,
    inhoud_naam: str | None = None,
    inhoud_doel: str | None = None,
    instance_content: Mapping[str, tuple[str, ...]] | None = None,
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
    if all(
        instantie.reading_order is not None
        for instantie, _ in geordende_plaatsingen
    ):
        geordende_plaatsingen = tuple(sorted(
            geordende_plaatsingen,
            key=lambda plaatsing: plaatsing[0].reading_order or 0,
        ))

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
        *_responsive_css(layout),
        "  </style>",
        "</head>",
        "<body>",
        '  <header class="bp-product-header">',
    ]
    if wereld_naam is not None and thema_naam is not None:
        mode_suffix = (
            f" · {html.escape(mode_label)}"
            if mode_label is not None
            else ""
        )
        snapshot_suffix = (
            f" · {html.escape(snapshot_label)}"
            if snapshot_label is not None
            else ""
        )
        regels.append(
            f'    <p class="bp-product-kicker">{html.escape(wereld_naam)}'
            f' · {html.escape(thema_naam)} · Gegenereerd uit BAT'
            f"{mode_suffix}{snapshot_suffix}</p>"
        )
    regels.extend([
        f"    <h1>{html.escape(inhoud_naam or compositie.naam)}</h1>",
        f'    <p class="bp-product-purpose">{html.escape(inhoud_doel or compositie.doel)}</p>',
        "  </header>",
        (
            f'  <main class="bp-layout bp-layout-{_css_naam(layout.id)}" '
            f'data-layout-type="{layout.type.value}" '
            f'data-responsive-breakpoint="{layout.responsive_breakpoint or ""}" '
            f'data-compact-columns="{layout.compact_columns or ""}" '
            f'style="{_style(_layout_css(layout))}">'
        ),
    ])
    for instantie, region in geordende_plaatsingen:
        heading_id = f"bp-instance-{_css_naam(instantie.id)}-title"
        heading_id_attribute = ""
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
        state_attributes = ""
        if instantie.state_appearances:
            state_attributes = (
                ' data-component-states="'
                + html.escape(
                    " ".join(
                        state
                        for state, _ in instantie.state_appearances
                    )
                )
                + '"'
                + "".join(
                    f' data-state-{html.escape(state)}-appearance="'
                    f'{html.escape(appearance_id)}"'
                    for state, appearance_id in instantie.state_appearances
                )
            )
        information_area_attribute = (
            f' data-information-area="{html.escape(instantie.information_area_id)}"'
            if instantie.information_area_id is not None
            else ""
        )
        homepage_area_attribute = (
            f' data-homepage-area="{html.escape(instantie.homepage_area_id)}"'
            if instantie.homepage_area_id is not None
            else ""
        )
        homepage_role_attribute = (
            f' data-homepage-role="{html.escape(instantie.homepage_role)}"'
            if instantie.homepage_role is not None
            else ""
        )
        component_role_attribute = (
            f' data-component-role="{html.escape(instantie.component_role)}"'
            if instantie.component_role is not None
            else ""
        )
        information_accessibility_attribute = (
            f' aria-label="{html.escape(instantie.accessibility_label)}"'
            if instantie.accessibility_label is not None
            else ""
        )
        component_accessibility_attributes = ""
        if instantie.accessibility is not None:
            contract = instantie.accessibility
            component_accessibility_attributes = (
                f' data-accessibility-contract="'
                f'{html.escape(contract.contract_id)}"'
                f' data-accessibility-role="{html.escape(contract.rol)}"'
                f' data-accessibility-name-source="'
                f'{html.escape(contract.naambron)}"'
            )
            if contract.waardebron is not None:
                component_accessibility_attributes += (
                    f' data-accessibility-value-source="'
                    f'{html.escape(contract.waardebron)}"'
                )
            if contract.foutbron is not None:
                component_accessibility_attributes += (
                    f' data-accessibility-error-source="'
                    f'{html.escape(contract.foutbron)}"'
                )
            component_accessibility_attributes += (
                f' data-accessibility-disabled="'
                f'{html.escape(contract.disabled_gedrag)}"'
                f' data-accessibility-focus="'
                f'{html.escape(contract.focusgedrag)}"'
                f' data-accessibility-keyboard="'
                f'{html.escape(contract.toetsenbordgedrag)}"'
            )
            if contract.toetsen:
                component_accessibility_attributes += (
                    f' data-accessibility-keys="'
                    f'{html.escape(" ".join(contract.toetsen))}"'
                )
            if (
                instantie.accessibility_label is None
                and contract.rol == "groep"
            ):
                information_accessibility_attribute = (
                    f' aria-labelledby="{html.escape(heading_id)}"'
                )
                heading_id_attribute = (
                    f' id="{html.escape(heading_id)}"'
                )
        reading_order_attribute = (
            f' data-reading-order="{instantie.reading_order}"'
            if instantie.reading_order is not None
            else ""
        )
        focus_order_attribute = (
            f' data-focus-order="{instantie.focus_order}"'
            if instantie.focus_order is not None
            else ""
        )
        navigation_behavior_attribute = (
            f' data-navigation-behavior="{html.escape(instantie.navigation_behavior)}"'
            if instantie.navigation_behavior is not None
            else ""
        )
        compact_order_attribute = (
            f' data-compact-order="{region.compact_order}"'
            if region.compact_order is not None
            else ""
        )
        regels.extend([
            (
                f'    <section class="bp-region {componentklasse(instantie.component_id)}'
                f'{variant_class}" '
                f'data-region="{html.escape(region.id)}" '
                f'data-instance="{html.escape(instantie.id)}" '
                f'data-component="{html.escape(instantie.component_id)}"'
                f"{variant_attribute}{appearance_attribute}"
                f"{state_attributes}"
                f"{information_area_attribute}{homepage_area_attribute}"
                f"{homepage_role_attribute}{component_role_attribute}"
                f"{reading_order_attribute}{focus_order_attribute}"
                f"{navigation_behavior_attribute}{compact_order_attribute}"
                f"{component_accessibility_attributes}"
                f"{information_accessibility_attribute}{style_attribute}>"
            ),
            f"      <h2{heading_id_attribute}>"
            f"{html.escape(instantie.naam)}</h2>",
        ])
        if (
            instance_content is not None
            and instantie.id in instance_content
        ):
            regels.extend(
                f"      {line}" if line else ""
                for line in instance_content[instantie.id]
            )
        if instantie.metric_value is not None:
            regels.append(
                f'      <p class="bp-metric" '
                f'data-metric-kind="{html.escape(instantie.metric_kind or "")}">'
                f"{instantie.metric_value}</p>"
            )
        if instantie.core_message is not None:
            regels.append(
                '      <p class="bp-core-message">'
                f"{html.escape(instantie.core_message)}</p>"
            )
        if instantie.brand is not None:
            regels.extend([
                f'      <p class="bp-brand-name">{html.escape(instantie.brand.naam)}</p>',
                f'      <p class="bp-brand-tagline">{html.escape(instantie.brand.tagline)}</p>',
                f'      <p class="bp-brand-promise">{html.escape(instantie.brand.promise)}</p>',
                (
                    f'      <ul class="bp-brand-principles" '
                    f'data-brand="{html.escape(instantie.brand.id)}" '
                    f'data-language="{html.escape(instantie.brand.language)}" '
                    f'data-voice="{html.escape(instantie.brand.voice)}">'
                ),
            ])
            for principe in instantie.brand.principles:
                regels.append(f"        <li>{html.escape(principe)}</li>")
            regels.append("      </ul>")
            regels.append(
                '      <ul class="bp-brand-products" aria-label="Productfamilie">'
            )
            for product in instantie.brand.products:
                regels.append(f"        <li>{html.escape(product)}</li>")
            regels.append("      </ul>")
        if instantie.metric_details:
            regels.append('      <ul class="bp-metric-details">')
            for detail in instantie.metric_details:
                waarde = (
                    f'<span class="bp-metric-detail-value">{detail.value}</span>'
                    if detail.value is not None
                    else ""
                )
                regels.append(
                    f'        <li><span>{html.escape(detail.label)}</span>'
                    f"{waarde}</li>"
                )
            regels.append("      </ul>")
        if instantie.content_anchors:
            regels.append('      <ul class="bp-content-anchors" aria-label="Kerninhoud">')
            for anker in instantie.content_anchors:
                regels.append(
                    f'        <li data-content-anchor="{html.escape(anker.id)}" '
                    f'data-object-kind="{html.escape(anker.object_kind)}">'
                    f"<strong>{html.escape(anker.naam)}</strong>"
                    f"<span>{html.escape(anker.doel)}</span></li>"
                )
            regels.append("      </ul>")
        if instantie.navigation_targets:
            regels.append('      <nav class="bp-product-navigation" aria-label="Productnavigatie">')
            regels.append("        <ul>")
            for doel in instantie.navigation_targets:
                regels.append(
                    f'          <li><a href="{html.escape(PurePosixPath(doel.artifact_path).name)}" '
                    f'data-navigation-target="{html.escape(doel.id)}" '
                    f'data-navigation-kind="{html.escape(doel.target_kind)}">'
                    f"{html.escape(doel.naam)}</a></li>"
                )
            regels.append("        </ul>")
            regels.append("      </nav>")
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
