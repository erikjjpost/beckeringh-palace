"""Manifestbackend voor het opgeloste native wallpaperproductcontract."""
from __future__ import annotations

import json

from compiler.backend import Backend
from compiler.product_model import ProductDefinition
from compiler.wallpaper_products import WALLPAPER_CONTENT


def _render_manifest(_objecten, product: ProductDefinition) -> str:
    wallpaper = product.opgeloste_wallpaper
    if product.inhoud != WALLPAPER_CONTENT or wallpaper is None:
        raise ValueError(
            f"Wallpapermanifest '{product.id}' vereist een opgeloste wallpaper"
        )
    if product.mode != "static" or not product.snapshot_ref:
        raise ValueError(
            f"Wallpapermanifest '{product.id}' vereist statische "
            "snapshotidentiteit"
        )

    wallpaper_manifest = {
        "id": wallpaper.id,
        "naam": wallpaper.naam,
        "doel": wallpaper.doel,
        "wereld": wallpaper.wereld,
        "merk": wallpaper.merk,
        "formaat": wallpaper.formaat,
        "canvas": {
            "breedte": wallpaper.breedte,
            "hoogte": wallpaper.hoogte,
            "eenheid": "px",
            "materiaalrol": wallpaper.canvas_role,
            "kleur": wallpaper.canvas.waarde,
        },
        "lagen": [
            {
                "id": laag.id,
                "naam": laag.naam,
                "doel": laag.doel,
                "rol": laag.rol,
                "plaatsingen": [
                    {
                        "id": plaatsing.id,
                        "naam": plaatsing.naam,
                        "doel": plaatsing.doel,
                        "asset": plaatsing.asset.id,
                        "x": plaatsing.x,
                        "y": plaatsing.y,
                        "breedte": plaatsing.breedte,
                        "hoogte": plaatsing.hoogte,
                        "fit": plaatsing.fit,
                        "dekking": plaatsing.dekking,
                        "materiaalrol": plaatsing.color_role,
                        "kleur": plaatsing.color.waarde,
                    }
                    for plaatsing in laag.plaatsingen
                ],
            }
            for laag in wallpaper.lagen
        ],
    }
    if wallpaper.familie:
        wallpaper_manifest["familie"] = {
            "id": wallpaper.familie,
            "variant": wallpaper.variant,
        }

    manifest = {
        "schema_version": 3,
        "product": {
            "id": product.id,
            "snapshot": product.snapshot_ref,
        },
        "wallpaper": wallpaper_manifest,
    }
    return json.dumps(
        manifest,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


backend = Backend("wallpaper-manifest", _render_manifest)
