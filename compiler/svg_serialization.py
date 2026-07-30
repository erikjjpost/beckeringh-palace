"""Veilige, gedeelde serialisatie van vooraf gevalideerde SVG assets."""
from __future__ import annotations

from html import escape
from typing import Iterable

from compiler.svg_assets import ResolvedSvgAsset


def _getal(waarde: float) -> str:
    if waarde == 0:
        return "0"
    return format(waarde, ".15g")


def svg_element_lines(
    asset: ResolvedSvgAsset,
    snapshot_ref: str,
    *,
    extra_attributes: Iterable[tuple[str, str]] = (),
    force_decorative: bool = False,
) -> tuple[str, ...]:
    """Serialiseer één asset zonder ruwe markup of externe referenties."""

    viewbox = " ".join(_getal(waarde) for waarde in asset.viewbox)
    attributen = [
        ("xmlns", "http://www.w3.org/2000/svg"),
        ("viewBox", viewbox),
        ("fill", asset.vulling),
        ("stroke", asset.lijn),
    ]
    if asset.lijn != "none":
        if (
            asset.lijndikte is None
            or asset.lijneinde is None
            or asset.lijnverbinding is None
        ):
            raise ValueError(
                f"SVG asset '{asset.id}' mist opgelost lijncontract"
            )
        attributen.extend([
            ("stroke-width", _getal(asset.lijndikte)),
            ("stroke-linecap", asset.lijneinde),
            ("stroke-linejoin", asset.lijnverbinding),
        ])
    attributen.extend([
        ("focusable", "false"),
        ("data-bp-asset", asset.id),
        ("data-bp-role", asset.rol),
    ])
    if asset.familie is not None and asset.variant is not None:
        attributen.extend([
            ("data-bp-family", asset.familie),
            ("data-bp-variant", asset.variant),
        ])
    if snapshot_ref:
        attributen.append(("data-bp-snapshot", snapshot_ref))
    attributen.extend(tuple(extra_attributes))

    titelregel = None
    if force_decorative or asset.toegankelijkheid == "decoratief":
        attributen.append(("aria-hidden", "true"))
    else:
        if asset.label is None:
            raise ValueError(
                f"Informatief SVG asset '{asset.id}' mist opgelost label"
            )
        titel_id = f"{asset.id}-title"
        attributen.extend([
            ("role", "img"),
            ("aria-labelledby", titel_id),
        ])
        titelregel = (
            f'  <title id="{escape(titel_id, quote=True)}">'
            f"{escape(asset.label)}</title>"
        )

    namen = tuple(naam for naam, _ in attributen)
    if len(namen) != len(set(namen)):
        raise ValueError(
            f"SVG asset '{asset.id}' bevat dubbele rootattributen"
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
    return tuple(regels)
