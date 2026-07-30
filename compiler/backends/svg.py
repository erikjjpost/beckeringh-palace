"""SVG-backendplugin voor getypeerde native vectorassets."""
from __future__ import annotations

from html import escape

from compiler.backend import Backend
from compiler.product_model import ProductDefinition


def _getal(waarde: float) -> str:
    if waarde == 0:
        return "0"
    return format(waarde, ".15g")


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

    viewbox = " ".join(_getal(waarde) for waarde in asset.viewbox)
    attributen = [
        ('xmlns', "http://www.w3.org/2000/svg"),
        ('viewBox', viewbox),
        ('fill', asset.vulling),
        ('stroke', asset.lijn),
    ]
    if asset.lijn != "none":
        attributen.extend([
            ('stroke-width', _getal(asset.lijndikte)),
            ('stroke-linecap', asset.lijneinde),
            ('stroke-linejoin', asset.lijnverbinding),
        ])
    attributen.extend([
        ('focusable', "false"),
        ('data-bp-asset', asset.id),
        ('data-bp-role', asset.rol),
        ('data-bp-snapshot', product.snapshot_ref),
    ])

    titelregel = None
    if asset.toegankelijkheid == "decoratief":
        attributen.append(('aria-hidden', "true"))
    else:
        titel_id = f"{asset.id}-title"
        attributen.extend([
            ('role', "img"),
            ('aria-labelledby', titel_id),
        ])
        titelregel = (
            f'  <title id="{escape(titel_id, quote=True)}">'
            f"{escape(asset.label)}</title>"
        )

    regels = [
        "<svg "
        + " ".join(
            f'{naam}="{escape(waarde, quote=True)}"'
            for naam, waarde in attributen
        )
        + ">"
    ]
    if titelregel is not None:
        regels.append(titelregel)
    regels.extend(
        f'  <path d="{escape(pad, quote=True)}"/>'
        for pad in asset.paden
    )
    regels.append("</svg>")
    return "\n".join(regels) + "\n"


backend = Backend("svg", _render_svg)
