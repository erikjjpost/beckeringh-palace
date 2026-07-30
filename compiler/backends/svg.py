"""SVG-backendplugin voor getypeerde native vectorassets."""
from __future__ import annotations

from compiler.backend import Backend
from compiler.product_model import ProductDefinition
from compiler.svg_serialization import svg_element_lines


def _render_svg(_objecten, product: ProductDefinition) -> str:
    asset = product.opgelost_asset
    if product.inhoud != "asset" or asset is None:
        raise ValueError(
            f"SVG product '{product.id}' vereist een opgelost native asset"
        )
    if product.mode != "static" or not product.snapshot_ref:
        raise ValueError(
            f"SVG product '{product.id}' vereist statische snapshotidentiteit"
        )

    return "\n".join(
        svg_element_lines(asset, product.snapshot_ref)
    ) + "\n"


backend = Backend("svg", _render_svg)
