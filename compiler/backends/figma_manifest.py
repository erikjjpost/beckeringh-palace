"""Deterministische masterbeschrijving voor latere Figma synchronisatie."""
from __future__ import annotations

import json

from compiler.backend import Backend
from compiler.design_components import verzamel_appearances
from compiler.figma_master import FIGMA_MASTER_CONTENT
from compiler.product_model import ProductDefinition


def _theme_manifest(theme):
    manifest = {
        "id": theme.thema_id,
        "wereld": theme.wereld_id,
        "palet": {
            "id": theme.palet.id,
            "rollen": {
                role: {"color_id": color.id, "value": color.waarde}
                for role, color in theme.palet.kleuren
            },
        },
        "typografie": {
            "id": theme.typografie.id,
            "heading": list(theme.typografie.heading),
            "body": list(theme.typografie.body),
            "mono": list(theme.typografie.mono),
            "levering": theme.typografie.levering,
        },
    }
    if theme.typeschaal is not None:
        schaal = theme.typeschaal
        manifest["typeschaal"] = {
            "id": schaal.id,
            "rollen": {
                rol: {
                    "font_role": getattr(schaal, f"{rol}_font"),
                    "font_family": list(
                        getattr(theme.typografie, getattr(schaal, f"{rol}_font"))
                    ),
                    "font_size": getattr(schaal, rol),
                    "font_weight": getattr(schaal, f"{rol}_weight"),
                    "line_height": getattr(schaal, f"{rol}_line_height"),
                    "letter_spacing": getattr(schaal, f"{rol}_letter_spacing"),
                }
                for rol in ("display", "title", "heading", "body", "label", "caption")
            },
        }
    for naam, resolved, velden in (
        ("spacing", theme.spacing, ("none", "xs", "small", "medium", "large", "xl")),
        ("border", theme.border, ("hairline", "regular", "strong", "style")),
        ("radius", theme.radius, ("small", "medium", "large", "pill", "control")),
        ("shadow", theme.shadow, ("low", "medium", "high", "none", "glow", "focus", "glow_accent")),
        ("motion", theme.motion, ("fast", "normal", "slow", "easing", "rest_offset", "hover_offset")),
    ):
        if resolved is not None:
            manifest[naam] = {
                "id": resolved.id,
                "rollen": {
                    veld: getattr(resolved, veld)
                    for veld in velden
                    if getattr(resolved, veld, None) is not None
                },
            }
    if theme.materiaal is not None:
        manifest["materiaal"] = {
            "id": theme.materiaal.id,
            "rollen": {
                role: {"color_id": color.id, "value": color.waarde}
                for role, color in theme.materiaal.kleuren
            },
        }
    color_primitives = {}
    for _role, color in theme.palet.kleuren:
        color_primitives[color.id] = color.waarde
    if theme.materiaal is not None:
        for _role, color in theme.materiaal.kleuren:
            color_primitives[color.id] = color.waarde
    manifest["color_primitives"] = dict(sorted(color_primitives.items()))
    if theme.artdirection is not None:
        art = theme.artdirection
        manifest["art_direction"] = {
            "id": art.id,
            "canvas": {
                "rol": art.canvas_role,
                "color_id": art.canvas.id,
                "kleur": art.canvas.waarde,
            },
            "interaction": {
                "rol": art.interaction_role,
                "color_id": art.interaction.id,
                "kleur": art.interaction.waarde,
            },
            "warm_accent": {
                "rol": art.warm_accent_role,
                "color_id": art.warm_accent.id,
                "kleur": art.warm_accent.waarde,
                "limiet": art.warm_accent_limit,
            },
            "glow": art.glow,
            "ornament": art.ornament,
            "density": art.density,
            "imagery": art.imagery,
        }
    return manifest


def _render(objecten, product: ProductDefinition) -> str:
    master = product.opgelost_figma_master
    if product.inhoud != FIGMA_MASTER_CONTENT or master is None:
        raise ValueError(
            f"Figma manifest '{product.id}' vereist een opgeloste Figma master"
        )
    if product.mode != "static" or not product.snapshot_ref:
        raise ValueError(
            f"Figma manifest '{product.id}' vereist statische snapshotidentiteit"
        )

    appearance_ids = {
        appearance_id
        for component in master.componenten
        for appearance_id in (component.appearance,)
        if appearance_id
    }
    appearance_ids.update(
        appearance_id
        for variant in master.varianten
        for _state, appearance_id in variant.state_appearances
    )
    appearances = [
        item
        for item in verzamel_appearances(objecten)
        if item.id in appearance_ids
    ]

    manifest = {
        "schema_version": 2,
        "product": {
            "id": product.id,
            "snapshot": product.snapshot_ref,
        },
        "figma_master": {
            "id": master.id,
            "naam": master.naam,
            "doel": master.doel,
            "wereld": master.wereld,
        },
        "theme": _theme_manifest(master.thema),
        "assets": [
            {
                "id": asset.id,
                "naam": asset.naam,
                "rol": asset.rol,
                "viewbox": list(asset.viewbox),
                "paden": list(asset.paden),
                "vulling": asset.vulling,
                "lijn": asset.lijn,
                "lijndikte": asset.lijndikte,
                "lijneinde": asset.lijneinde,
                "lijnverbinding": asset.lijnverbinding,
                "toegankelijkheid": asset.toegankelijkheid,
                "label": asset.label,
            }
            for asset in master.assets
        ],
        "appearances": [
            {
                "id": appearance.id,
                "naam": appearance.naam,
                "rollen": dict(appearance.rollen),
            }
            for appearance in appearances
        ],
        "components": [
            {
                "id": component.id,
                "naam": component.naam,
                "rol": component.rol,
                "anatomie": list(component.anatomie),
                "appearance": component.appearance,
                "toegankelijkheid": component.accessibility_id,
            }
            for component in master.componenten
        ],
        "variants": [
            {
                "id": variant.id,
                "naam": variant.naam,
                "component": variant.component_id,
                "states": dict(variant.state_appearances),
            }
            for variant in master.varianten
        ],
        "compositions": [
            {
                "id": composition.id,
                "naam": composition.naam,
                "rol": composition.role,
                "instances": [
                    {
                        "id": instance.id,
                        "component": instance.component_id,
                        "variant": instance.variant_id,
                        "appearance": instance.appearance_id,
                    }
                    for instance in composition.instances
                ],
            }
            for composition in master.composities
        ],
        "layouts": [
            {
                "id": layout.id,
                "naam": layout.naam,
                "type": layout.type.value,
                "columns": layout.columns,
                "rows": layout.rows,
                "direction": (
                    layout.direction.value if layout.direction is not None else None
                ),
                "wrap": layout.wrap,
                "responsive_breakpoint": layout.responsive_breakpoint,
                "compact_columns": layout.compact_columns,
                "regions": [
                    {
                        "id": region.id,
                        "instance": region.instance_id,
                        "column": region.column,
                        "row": region.row,
                        "column_span": region.column_span,
                        "row_span": region.row_span,
                        "layer": region.layer,
                        "compact_order": region.compact_order,
                    }
                    for region in layout.regions
                ],
            }
            for layout in master.layouts
        ],
    }
    return json.dumps(
        manifest,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


backend = Backend("figma-manifest", _render)
