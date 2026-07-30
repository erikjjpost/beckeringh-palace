"""Getypeerd en veilig contract voor native SVG bronassets."""
from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


SVG_ASSET_ROLLEN = frozenset({"icoon", "logo", "illustratie", "ornament"})
SVG_TOEGANKELIJKHEID = frozenset({"informatief", "decoratief"})
SVG_LIJNEINDEN = frozenset({"butt", "round", "square"})
SVG_LIJNVERBINDINGEN = frozenset({"miter", "round", "bevel"})

_GETAL = r"[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?"
_GETAL_VOLLEDIG = re.compile(rf"^{_GETAL}$")
_PAD_TOKEN = re.compile(rf"{_GETAL}|[AaCcHhLlMmQqSsTtVvZz]")
_PAD_SCHEIDING = re.compile(r"^[\s,]*$")
_VEILIGE_KLEUR = re.compile(
    r"^(?:none|currentColor|#[0-9A-Fa-f]{3,4}|#[0-9A-Fa-f]{6}|#[0-9A-Fa-f]{8})$"
)
_COMMANDO_ARITEIT = {
    "A": 7,
    "C": 6,
    "H": 1,
    "L": 2,
    "M": 2,
    "Q": 4,
    "S": 4,
    "T": 2,
    "V": 1,
    "Z": 0,
}
_MAXIMAAL_AANTAL_PADEN = 64
_MAXIMALE_PADLENGTE = 8192


@dataclass(frozen=True)
class ResolvedSvgAsset:
    """Volledig gevalideerde SVG geometrie zonder uitvoerimplementatie."""

    id: str
    naam: str
    doel: str
    rol: str
    viewbox: tuple[float, float, float, float]
    paden: tuple[str, ...]
    vulling: str
    lijn: str
    lijndikte: float | None
    lijneinde: str | None
    lijnverbinding: str | None
    toegankelijkheid: str
    label: str | None
    familie: str | None
    variant: str | None


class SvgAssetResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot een SVG asset worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise SvgAssetResolutionError(
            f"SVG asset '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _getal(waarde: object) -> float | None:
    if not isinstance(waarde, str) or not _GETAL_VOLLEDIG.fullmatch(waarde.strip()):
        return None
    getal = float(waarde)
    return getal if math.isfinite(getal) else None


def _viewbox(waarde: object) -> tuple[float, float, float, float] | None:
    if not isinstance(waarde, str):
        return None
    delen = waarde.split()
    if len(delen) != 4:
        return None
    getallen = tuple(_getal(deel) for deel in delen)
    if any(getal is None for getal in getallen):
        return None
    x, y, breedte, hoogte = getallen
    if breedte <= 0 or hoogte <= 0:
        return None
    return x, y, breedte, hoogte


def _pad_tokens(pad: str) -> tuple[str, ...] | None:
    tokens: list[str] = []
    positie = 0
    for match in _PAD_TOKEN.finditer(pad):
        if not _PAD_SCHEIDING.fullmatch(pad[positie:match.start()]):
            return None
        tokens.append(match.group(0))
        positie = match.end()
    if not _PAD_SCHEIDING.fullmatch(pad[positie:]) or not tokens:
        return None
    return tuple(tokens)


def _geldig_svg_pad(pad: object) -> bool:
    if (
        not isinstance(pad, str)
        or not pad.strip()
        or len(pad) > _MAXIMALE_PADLENGTE
    ):
        return False
    tokens = _pad_tokens(pad)
    if tokens is None or tokens[0] not in {"M", "m"}:
        return False

    index = 0
    while index < len(tokens):
        commando = tokens[index]
        if commando.upper() not in _COMMANDO_ARITEIT:
            return False
        index += 1
        waarden: list[float] = []
        while index < len(tokens) and tokens[index].upper() not in _COMMANDO_ARITEIT:
            waarde = _getal(tokens[index])
            if waarde is None:
                return False
            waarden.append(waarde)
            index += 1

        ariteit = _COMMANDO_ARITEIT[commando.upper()]
        if ariteit == 0:
            if waarden:
                return False
            continue
        if not waarden or len(waarden) % ariteit:
            return False

        if commando.upper() == "A":
            for begin in range(0, len(waarden), ariteit):
                groep = waarden[begin:begin + ariteit]
                if groep[0] < 0 or groep[1] < 0:
                    return False
                if groep[3] not in {0.0, 1.0} or groep[4] not in {0.0, 1.0}:
                    return False
    return True


def _geldige_paden(waarde: object) -> bool:
    return (
        isinstance(waarde, list)
        and 0 < len(waarde) <= _MAXIMAAL_AANTAL_PADEN
        and all(_geldig_svg_pad(pad) for pad in waarde)
        and len(waarde) == len(set(waarde))
    )


def _veilige_kleur(waarde: object) -> bool:
    return isinstance(waarde, str) and bool(_VEILIGE_KLEUR.fullmatch(waarde))


@dataclass(frozen=True)
class SvgAssetConstraint:
    """Weiger ongetypeerde, actieve of externe SVG inhoud."""

    sleutel: str = "world-model.svg-assets"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        toegestane_velden = {
            "naam",
            "doel",
            "formaat",
            "rol",
            "viewbox",
            "paden",
            "vulling",
            "lijn",
            "lijndikte",
            "lijneinde",
            "lijnverbinding",
            "toegankelijkheid",
            "label",
            "familie",
            "variant",
        }

        for asset in (obj for obj in context.objecten if obj.soort == "asset"):
            for naam in asset.eigenschappen:
                if naam not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP4301",
                        boodschap=(
                            f"SVG asset '{asset.id}' heeft onbekende "
                            f"eigenschap '{naam}'"
                        ),
                        locatie=asset.eigenschaplocaties.get(
                            naam, asset.bronlocatie
                        ),
                    ))

            if asset.eigenschappen.get("formaat") != "svg":
                diagnostics.append(Diagnostic(
                    code="BP4302",
                    boodschap=(
                        f"Asset '{asset.id}' vereist expliciet formaat 'svg'"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "formaat", asset.bronlocatie
                    ),
                ))

            rol = asset.eigenschappen.get("rol")
            if rol not in SVG_ASSET_ROLLEN:
                diagnostics.append(Diagnostic(
                    code="BP4303",
                    boodschap=(
                        f"SVG asset '{asset.id}' heeft onbekende rol '{rol}'"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "rol", asset.bronlocatie
                    ),
                ))

            if _viewbox(asset.eigenschappen.get("viewbox")) is None:
                diagnostics.append(Diagnostic(
                    code="BP4304",
                    boodschap=(
                        f"SVG asset '{asset.id}' vereist een viewbox met vier "
                        "eindige getallen en positieve breedte en hoogte"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "viewbox", asset.bronlocatie
                    ),
                ))

            paden = asset.eigenschappen.get("paden")
            if not (
                isinstance(paden, list)
                and 0 < len(paden) <= _MAXIMAAL_AANTAL_PADEN
                and len(paden) == len(set(paden))
            ):
                diagnostics.append(Diagnostic(
                    code="BP4305",
                    boodschap=(
                        f"SVG asset '{asset.id}' vereist een niet-lege, unieke "
                        "en begrensde lijst paden"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "paden", asset.bronlocatie
                    ),
                ))
            elif not all(_geldig_svg_pad(pad) for pad in paden):
                diagnostics.append(Diagnostic(
                    code="BP4306",
                    boodschap=(
                        f"SVG asset '{asset.id}' bevat ongeldige of onveilige "
                        "padgeometrie"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "paden", asset.bronlocatie
                    ),
                ))

            vulling = asset.eigenschappen.get("vulling")
            lijn = asset.eigenschappen.get("lijn")
            if (
                not _veilige_kleur(vulling)
                or not _veilige_kleur(lijn)
                or (vulling == "none" and lijn == "none")
            ):
                diagnostics.append(Diagnostic(
                    code="BP4307",
                    boodschap=(
                        f"SVG asset '{asset.id}' vereist veilige expliciete "
                        "vulling en lijn, waarvan minstens één zichtbaar is"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "vulling", asset.bronlocatie
                    ),
                ))

            lijnvelden = ("lijndikte", "lijneinde", "lijnverbinding")
            if lijn == "none":
                geldig_lijncontract = all(
                    veld not in asset.eigenschappen for veld in lijnvelden
                )
            else:
                lijndikte = _getal(asset.eigenschappen.get("lijndikte"))
                geldig_lijncontract = (
                    lijndikte is not None
                    and lijndikte > 0
                    and asset.eigenschappen.get("lijneinde") in SVG_LIJNEINDEN
                    and asset.eigenschappen.get("lijnverbinding")
                    in SVG_LIJNVERBINDINGEN
                )
            if not geldig_lijncontract:
                diagnostics.append(Diagnostic(
                    code="BP4308",
                    boodschap=(
                        f"SVG asset '{asset.id}' heeft geen consistent "
                        "expliciet lijncontract"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "lijn", asset.bronlocatie
                    ),
                ))

            toegankelijkheid = asset.eigenschappen.get("toegankelijkheid")
            if toegankelijkheid not in SVG_TOEGANKELIJKHEID:
                diagnostics.append(Diagnostic(
                    code="BP4309",
                    boodschap=(
                        f"SVG asset '{asset.id}' heeft onbekende "
                        f"toegankelijkheid '{toegankelijkheid}'"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "toegankelijkheid", asset.bronlocatie
                    ),
                ))
            label = asset.eigenschappen.get("label")
            geldig_label = (
                toegankelijkheid == "informatief"
                and isinstance(label, str)
                and bool(label.strip())
            ) or (
                toegankelijkheid == "decoratief"
                and "label" not in asset.eigenschappen
            )
            if toegankelijkheid in SVG_TOEGANKELIJKHEID and not geldig_label:
                diagnostics.append(Diagnostic(
                    code="BP4310",
                    boodschap=(
                        f"SVG asset '{asset.id}' vereist alleen voor "
                        "informatieve inhoud een niet-leeg label"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "label", asset.bronlocatie
                    ),
                ))

        return tuple(diagnostics)


def svg_asset_uit_object(
    obj: Architectuurobject,
) -> ResolvedSvgAsset | None:
    if obj.soort != "asset":
        return None

    viewbox = _viewbox(obj.eigenschappen.get("viewbox"))
    paden = obj.eigenschappen.get("paden")
    if viewbox is None or not _geldige_paden(paden):
        raise SvgAssetResolutionError(
            f"SVG asset '{obj.id}' is niet semantisch gevalideerd"
        )

    lijn = _tekst(obj, "lijn")
    lijndikte = (
        _getal(obj.eigenschappen.get("lijndikte"))
        if lijn != "none"
        else None
    )
    return ResolvedSvgAsset(
        id=obj.id,
        naam=_tekst(obj, "naam"),
        doel=_tekst(obj, "doel"),
        rol=_tekst(obj, "rol"),
        viewbox=viewbox,
        paden=tuple(paden),
        vulling=_tekst(obj, "vulling"),
        lijn=lijn,
        lijndikte=lijndikte,
        lijneinde=(
            _tekst(obj, "lijneinde")
            if lijn != "none"
            else None
        ),
        lijnverbinding=(
            _tekst(obj, "lijnverbinding")
            if lijn != "none"
            else None
        ),
        toegankelijkheid=_tekst(obj, "toegankelijkheid"),
        label=(
            _tekst(obj, "label")
            if "label" in obj.eigenschappen
            else None
        ),
        familie=(
            _tekst(obj, "familie")
            if "familie" in obj.eigenschappen
            else None
        ),
        variant=(
            _tekst(obj, "variant")
            if "variant" in obj.eigenschappen
            else None
        ),
    )


def resolveer_svg_assets(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedSvgAsset, ...]:
    assets = (svg_asset_uit_object(obj) for obj in objecten)
    return tuple(sorted(
        (asset for asset in assets if asset is not None),
        key=lambda asset: asset.id,
    ))
