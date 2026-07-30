"""PNG-backend voor het opgeloste native wallpaperproductcontract."""
from __future__ import annotations

from compiler.backend import Backend
from compiler.product_model import ProductDefinition
from compiler.wallpaper_png_renderer import render_wallpaper_png
from compiler.wallpaper_products import WALLPAPER_CONTENT


def _render_png(_objecten, product: ProductDefinition) -> bytes:
    wallpaper = product.opgeloste_wallpaper
    if product.inhoud != WALLPAPER_CONTENT or wallpaper is None:
        raise ValueError(
            f"Wallpaperbeeld '{product.id}' vereist een opgeloste wallpaper"
        )
    if product.mode != "static" or not product.snapshot_ref:
        raise ValueError(
            f"Wallpaperbeeld '{product.id}' vereist statische "
            "snapshotidentiteit"
        )
    return render_wallpaper_png(
        wallpaper,
        product.snapshot_ref,
        product.id,
    )


backend = Backend("wallpaper-png", _render_png)
