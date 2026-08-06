"""Backendonafhankelijk contract voor reproduceerbare wallpaperproducten."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import PurePosixPath
import re
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.svg_assets import ResolvedSvgAsset, resolveer_svg_assets
from compiler.music_circle import resolveer_muziekcirkels
from compiler.theme_resolution import ResolvedColor, resolveer_thema


WALLPAPER_CONTENT = "wallpaper"
WALLPAPER_MANIFEST_BACKEND = "wallpaper-manifest"
WALLPAPER_PNG_BACKEND = "wallpaper-png"
WALLPAPER_BACKENDS = frozenset({
    WALLPAPER_MANIFEST_BACKEND,
    WALLPAPER_PNG_BACKEND,
})
WALLPAPER_BACKEND_SUFFIXES = {
    WALLPAPER_MANIFEST_BACKEND: ".wallpaper.json",
    WALLPAPER_PNG_BACKEND: ".png",
}
WALLPAPER_FORMATEN = frozenset({"png"})
WALLPAPER_LAAGROLLEN = frozenset({
    "ornament",
    "illustratie",
    "merk",
    "voorgrond",
})
WALLPAPER_FIT_MODES = frozenset({"contain", "cover", "stretch"})
WALLPAPER_EFFECTS = frozenset({"solid", "radial-glow"})
WALLPAPER_LAAG_ASSETROLLEN = {
    "ornament": frozenset({"ornament"}),
    "illustratie": frozenset({"illustratie"}),
    "merk": frozenset({"logo"}),
    "voorgrond": frozenset({"icoon", "logo", "illustratie", "ornament"}),
}
_POSITIEF_GEHEEL = re.compile(r"^[1-9]\d*$")
_NIET_NEGATIEF_GEHEEL = re.compile(r"^(?:0|[1-9]\d*)$")
_DEKKING = re.compile(r"^(?:0|1|0\.\d*[1-9])$")
_MAXIMALE_CANVASMAAT = 16384


@dataclass(frozen=True)
class ResolvedWallpaperAssetPlacement:
    """Eén expliciete SVG assetplaatsing binnen een wallpaperlaag."""

    id: str
    naam: str
    doel: str
    laag: str
    asset: ResolvedSvgAsset
    x: int
    y: int
    breedte: int
    hoogte: int
    fit: str
    dekking: float
    color_role: str
    color: ResolvedColor
    effect: str


@dataclass(frozen=True)
class ResolvedWallpaperLayer:
    """Eén geordende semantische laag van een wallpaper."""

    id: str
    naam: str
    doel: str
    wallpaper: str
    rol: str
    plaatsingen: tuple[ResolvedWallpaperAssetPlacement, ...]


@dataclass(frozen=True)
class ResolvedWallpaper:
    """Volledig opgeloste wallpaperintentie zonder beeldbackend."""

    id: str
    naam: str
    doel: str
    wereld: str
    merk: str
    familie: str
    variant: str
    formaat: str
    breedte: int
    hoogte: int
    canvas_role: str
    canvas: ResolvedColor
    lagen: tuple[ResolvedWallpaperLayer, ...]


class WallpaperResolutionError(ValueError):
    """Niet gevalideerde CIR kan niet tot een wallpaper worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise WallpaperResolutionError(
            f"{obj.soort.capitalize()} '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _positief_geheel(waarde: object) -> int | None:
    if not isinstance(waarde, str) or not _POSITIEF_GEHEEL.fullmatch(waarde):
        return None
    getal = int(waarde)
    if getal > _MAXIMALE_CANVASMAAT:
        return None
    return getal


def _niet_negatief_geheel(waarde: object) -> int | None:
    if (
        not isinstance(waarde, str)
        or not _NIET_NEGATIEF_GEHEEL.fullmatch(waarde)
    ):
        return None
    return int(waarde)


def _dekking(waarde: object) -> float | None:
    if not isinstance(waarde, str) or not _DEKKING.fullmatch(waarde):
        return None
    try:
        getal = Decimal(waarde)
    except InvalidOperation:
        return None
    if not Decimal("0") <= getal <= Decimal("1"):
        return None
    return float(getal)


def resolveer_wallpapers(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedWallpaper, ...]:
    """Los wallpapers, lagen en plaatsingen op zonder uitvoerimplementatie."""

    objecten = tuple(objecten)
    assets = {
        asset.id: asset
        for asset in resolveer_svg_assets(objecten)
    }
    assets.update(
        {circle.id: circle.asset for circle in resolveer_muziekcirkels(objecten)}
    )
    lagen = {
        obj.id: obj
        for obj in objecten
        if obj.soort == "wallpaperlaag"
    }
    plaatsingen = {
        obj.id: obj
        for obj in objecten
        if obj.soort == "assetplaatsing"
    }
    wallpapers = []
    for obj in objecten:
        if obj.soort != "wallpaper":
            continue
        laag_ids = obj.eigenschappen.get("lagen")
        if (
            not isinstance(laag_ids, list)
            or not laag_ids
            or not all(isinstance(laag_id, str) for laag_id in laag_ids)
        ):
            raise WallpaperResolutionError(
                f"Wallpaper '{obj.id}' is niet semantisch gevalideerd"
            )
        wereld = _tekst(obj, "wereld")
        thema = resolveer_thema(objecten, wereld)
        canvas_role = _tekst(obj, "canvas")
        canvas = (
            thema.materiaal.kleur(canvas_role)
            if thema.materiaal is not None
            else None
        )
        if canvas is None:
            raise WallpaperResolutionError(
                f"Wallpaper '{obj.id}' kan canvasrol '{canvas_role}' niet oplossen"
            )
        opgeloste_lagen = []
        for laag_id in laag_ids:
            laag = lagen.get(laag_id)
            if laag is None:
                raise WallpaperResolutionError(
                    f"Wallpaper '{obj.id}' bevat onbekende laag '{laag_id}'"
                )
            plaatsing_ids = laag.eigenschappen.get("plaatsingen")
            if (
                not isinstance(plaatsing_ids, list)
                or not plaatsing_ids
                or not all(
                    isinstance(plaatsing_id, str)
                    for plaatsing_id in plaatsing_ids
                )
            ):
                raise WallpaperResolutionError(
                    f"Wallpaperlaag '{laag.id}' is niet semantisch gevalideerd"
                )
            opgeloste_plaatsingen = []
            for plaatsing_id in plaatsing_ids:
                plaatsing = plaatsingen.get(plaatsing_id)
                if plaatsing is None:
                    raise WallpaperResolutionError(
                        f"Wallpaperlaag '{laag.id}' bevat onbekende "
                        f"assetplaatsing '{plaatsing_id}'"
                    )
                asset_id = _tekst(plaatsing, "asset")
                asset = assets.get(asset_id)
                if asset is None:
                    raise WallpaperResolutionError(
                        f"Assetplaatsing '{plaatsing.id}' bevat onbekend "
                        f"asset '{asset_id}'"
                    )
                x = _niet_negatief_geheel(plaatsing.eigenschappen.get("x"))
                y = _niet_negatief_geheel(plaatsing.eigenschappen.get("y"))
                breedte = _positief_geheel(
                    plaatsing.eigenschappen.get("breedte")
                )
                hoogte = _positief_geheel(
                    plaatsing.eigenschappen.get("hoogte")
                )
                dekking = _dekking(plaatsing.eigenschappen.get("dekking"))
                if None in {x, y, breedte, hoogte, dekking}:
                    raise WallpaperResolutionError(
                        f"Assetplaatsing '{plaatsing.id}' is niet semantisch "
                        "gevalideerd"
                    )
                color_role = _tekst(plaatsing, "kleur")
                color = (
                    thema.materiaal.kleur(color_role)
                    if thema.materiaal is not None
                    else None
                )
                if color is None:
                    raise WallpaperResolutionError(
                        f"Assetplaatsing '{plaatsing.id}' kan kleurrol "
                        f"'{color_role}' niet oplossen"
                    )
                opgeloste_plaatsingen.append(
                    ResolvedWallpaperAssetPlacement(
                        id=plaatsing.id,
                        naam=_tekst(plaatsing, "naam"),
                        doel=_tekst(plaatsing, "doel"),
                        laag=laag.id,
                        asset=asset,
                        x=x,
                        y=y,
                        breedte=breedte,
                        hoogte=hoogte,
                        fit=_tekst(plaatsing, "fit"),
                        dekking=dekking,
                        color_role=color_role,
                        color=color,
                        effect=plaatsing.eigenschappen.get("effect", "solid"),
                    )
                )
            opgeloste_lagen.append(
                ResolvedWallpaperLayer(
                    id=laag.id,
                    naam=_tekst(laag, "naam"),
                    doel=_tekst(laag, "doel"),
                    wallpaper=obj.id,
                    rol=_tekst(laag, "rol"),
                    plaatsingen=tuple(opgeloste_plaatsingen),
                )
            )
        breedte = _positief_geheel(obj.eigenschappen.get("breedte"))
        hoogte = _positief_geheel(obj.eigenschappen.get("hoogte"))
        if breedte is None or hoogte is None:
            raise WallpaperResolutionError(
                f"Wallpaper '{obj.id}' is niet semantisch gevalideerd"
            )
        wallpapers.append(
            ResolvedWallpaper(
                id=obj.id,
                naam=_tekst(obj, "naam"),
                doel=_tekst(obj, "doel"),
                wereld=wereld,
                merk=_tekst(obj, "merk"),
                familie=str(obj.eigenschappen.get("familie", "")),
                variant=str(obj.eigenschappen.get("variant", "")),
                formaat=_tekst(obj, "formaat"),
                breedte=breedte,
                hoogte=hoogte,
                canvas_role=canvas_role,
                canvas=canvas,
                lagen=tuple(opgeloste_lagen),
            )
        )
    return tuple(sorted(wallpapers, key=lambda wallpaper: wallpaper.id))


@dataclass(frozen=True)
class WallpaperProductConstraint:
    """Valideer canvas, formaat, lagen, plaatsingen en productkoppeling."""

    sleutel: str = "world-model.wallpaper-products"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        wallpapers = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "wallpaper"
        }
        lagen = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "wallpaperlaag"
        }
        plaatsingen = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "assetplaatsing"
        }
        assets = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort in {"asset", "muziekcirkel"}
        }
        werelden = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "wereld"
        }
        themas = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "thema"
        }
        materialen = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "materiaal"
        }
        merken = {
            obj.id
            for obj in context.objecten
            if obj.soort == "merk"
        }

        for wallpaper in wallpapers.values():
            toegestane_velden = {
                "naam",
                "doel",
                "wereld",
                "merk",
                "familie",
                "variant",
                "formaat",
                "breedte",
                "hoogte",
                "canvas",
                "lagen",
            }
            for veld in wallpaper.eigenschappen:
                if veld not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP4351",
                        boodschap=(
                            f"Wallpaper '{wallpaper.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=wallpaper.eigenschaplocaties.get(
                            veld, wallpaper.bronlocatie
                        ),
                    ))

            wereld_id = wallpaper.eigenschappen.get("wereld")
            wereld = werelden.get(wereld_id)
            if wereld is None:
                diagnostics.append(Diagnostic(
                    code="BP4352",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' verwijst naar onbekende "
                        f"wereld '{wereld_id}'"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "wereld", wallpaper.bronlocatie
                    ),
                ))

            merk = wallpaper.eigenschappen.get("merk")
            if merk not in merken:
                diagnostics.append(Diagnostic(
                    code="BP4353",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' verwijst naar onbekend "
                        f"merk '{merk}'"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "merk", wallpaper.bronlocatie
                    ),
                ))

            formaat = wallpaper.eigenschappen.get("formaat")
            if formaat not in WALLPAPER_FORMATEN:
                diagnostics.append(Diagnostic(
                    code="BP4354",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' heeft onbekend formaat "
                        f"'{formaat}'"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "formaat", wallpaper.bronlocatie
                    ),
                ))

            breedte = _positief_geheel(
                wallpaper.eigenschappen.get("breedte")
            )
            hoogte = _positief_geheel(
                wallpaper.eigenschappen.get("hoogte")
            )
            if breedte is None or hoogte is None:
                diagnostics.append(Diagnostic(
                    code="BP4355",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' vereist positieve, "
                        f"canonieke canvasmaten tot {_MAXIMALE_CANVASMAAT}px"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "breedte", wallpaper.bronlocatie
                    ),
                ))

            canvas_role = wallpaper.eigenschappen.get("canvas")
            materiaal = None
            if wereld is not None:
                thema = themas.get(wereld.eigenschappen.get("thema"))
                if thema is not None:
                    materiaal = materialen.get(
                        thema.eigenschappen.get("materiaal")
                    )
            if (
                materiaal is None
                or not isinstance(canvas_role, str)
                or canvas_role not in materiaal.eigenschappen
            ):
                diagnostics.append(Diagnostic(
                    code="BP4356",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' kan canvasrol "
                        f"'{canvas_role}' niet uit zijn wereldthema oplossen"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "canvas", wallpaper.bronlocatie
                    ),
                ))

            laag_ids = wallpaper.eigenschappen.get("lagen")
            geldige_lijst = (
                isinstance(laag_ids, list)
                and bool(laag_ids)
                and all(
                    isinstance(laag_id, str) and laag_id.strip()
                    for laag_id in laag_ids
                )
                and len(laag_ids) == len(set(laag_ids))
            )
            if not geldige_lijst:
                diagnostics.append(Diagnostic(
                    code="BP4357",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' vereist een niet-lege, "
                        "unieke en geordende lijst lagen"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "lagen", wallpaper.bronlocatie
                    ),
                ))
                continue
            onbekende_lagen = [
                laag_id for laag_id in laag_ids if laag_id not in lagen
            ]
            if onbekende_lagen:
                diagnostics.append(Diagnostic(
                    code="BP4358",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' verwijst naar onbekende "
                        f"laag '{onbekende_lagen[0]}'"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "lagen", wallpaper.bronlocatie
                    ),
                ))
            verwezen_lagen = {
                laag.id
                for laag in lagen.values()
                if laag.eigenschappen.get("wallpaper") == wallpaper.id
            }
            if (
                onbekende_lagen
                or verwezen_lagen != set(laag_ids)
                or any(
                    lagen[laag_id].eigenschappen.get("wallpaper")
                    != wallpaper.id
                    for laag_id in laag_ids
                    if laag_id in lagen
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4359",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' vereist een exact "
                        "wederkerige lagenlijst"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "lagen", wallpaper.bronlocatie
                    ),
                ))

        for laag in lagen.values():
            toegestane_velden = {
                "naam",
                "doel",
                "wallpaper",
                "rol",
                "plaatsingen",
            }
            for veld in laag.eigenschappen:
                if veld not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP4360",
                        boodschap=(
                            f"Wallpaperlaag '{laag.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=laag.eigenschaplocaties.get(
                            veld, laag.bronlocatie
                        ),
                    ))

            wallpaper_id = laag.eigenschappen.get("wallpaper")
            if wallpaper_id not in wallpapers:
                diagnostics.append(Diagnostic(
                    code="BP4361",
                    boodschap=(
                        f"Wallpaperlaag '{laag.id}' verwijst naar onbekende "
                        f"wallpaper '{wallpaper_id}'"
                    ),
                    locatie=laag.eigenschaplocaties.get(
                        "wallpaper", laag.bronlocatie
                    ),
                ))

            rol = laag.eigenschappen.get("rol")
            if rol not in WALLPAPER_LAAGROLLEN:
                diagnostics.append(Diagnostic(
                    code="BP4362",
                    boodschap=(
                        f"Wallpaperlaag '{laag.id}' heeft onbekende rol "
                        f"'{rol}'"
                    ),
                    locatie=laag.eigenschaplocaties.get(
                        "rol", laag.bronlocatie
                    ),
                ))

            plaatsing_ids = laag.eigenschappen.get("plaatsingen")
            geldige_lijst = (
                isinstance(plaatsing_ids, list)
                and bool(plaatsing_ids)
                and all(
                    isinstance(plaatsing_id, str) and plaatsing_id.strip()
                    for plaatsing_id in plaatsing_ids
                )
                and len(plaatsing_ids) == len(set(plaatsing_ids))
            )
            if not geldige_lijst:
                diagnostics.append(Diagnostic(
                    code="BP4363",
                    boodschap=(
                        f"Wallpaperlaag '{laag.id}' vereist een niet-lege, "
                        "unieke en geordende lijst assetplaatsingen"
                    ),
                    locatie=laag.eigenschaplocaties.get(
                        "plaatsingen", laag.bronlocatie
                    ),
                ))
                continue
            onbekende_plaatsingen = [
                plaatsing_id
                for plaatsing_id in plaatsing_ids
                if plaatsing_id not in plaatsingen
            ]
            if onbekende_plaatsingen:
                diagnostics.append(Diagnostic(
                    code="BP4364",
                    boodschap=(
                        f"Wallpaperlaag '{laag.id}' verwijst naar onbekende "
                        f"assetplaatsing '{onbekende_plaatsingen[0]}'"
                    ),
                    locatie=laag.eigenschaplocaties.get(
                        "plaatsingen", laag.bronlocatie
                    ),
                ))
            verwezen_plaatsingen = {
                plaatsing.id
                for plaatsing in plaatsingen.values()
                if plaatsing.eigenschappen.get("laag") == laag.id
            }
            if (
                onbekende_plaatsingen
                or verwezen_plaatsingen != set(plaatsing_ids)
                or any(
                    plaatsingen[plaatsing_id].eigenschappen.get("laag")
                    != laag.id
                    for plaatsing_id in plaatsing_ids
                    if plaatsing_id in plaatsingen
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4365",
                    boodschap=(
                        f"Wallpaperlaag '{laag.id}' vereist een exact "
                        "wederkerige plaatsingenlijst"
                    ),
                    locatie=laag.eigenschaplocaties.get(
                        "plaatsingen", laag.bronlocatie
                    ),
                ))

        for plaatsing in plaatsingen.values():
            toegestane_velden = {
                "naam",
                "doel",
                "laag",
                "asset",
                "x",
                "y",
                "breedte",
                "hoogte",
                "fit",
                "dekking",
                "kleur",
                "effect",
            }
            for veld in plaatsing.eigenschappen:
                if veld not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP4366",
                        boodschap=(
                            f"Assetplaatsing '{plaatsing.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=plaatsing.eigenschaplocaties.get(
                            veld, plaatsing.bronlocatie
                        ),
                    ))

            laag_id = plaatsing.eigenschappen.get("laag")
            laag = lagen.get(laag_id)
            if laag is None:
                diagnostics.append(Diagnostic(
                    code="BP4367",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' verwijst naar "
                        f"onbekende wallpaperlaag '{laag_id}'"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "laag", plaatsing.bronlocatie
                    ),
                ))

            asset_id = plaatsing.eigenschappen.get("asset")
            asset = assets.get(asset_id)
            if asset is None:
                diagnostics.append(Diagnostic(
                    code="BP4368",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' verwijst naar "
                        f"onbekend asset '{asset_id}'"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "asset", plaatsing.bronlocatie
                    ),
                ))

            x = _niet_negatief_geheel(plaatsing.eigenschappen.get("x"))
            y = _niet_negatief_geheel(plaatsing.eigenschappen.get("y"))
            breedte = _positief_geheel(
                plaatsing.eigenschappen.get("breedte")
            )
            hoogte = _positief_geheel(
                plaatsing.eigenschappen.get("hoogte")
            )
            if None in {x, y, breedte, hoogte}:
                diagnostics.append(Diagnostic(
                    code="BP4369",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' vereist canonieke, "
                        "niet-negatieve coördinaten en positieve afmetingen"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "x", plaatsing.bronlocatie
                    ),
                ))
            elif laag is not None:
                wallpaper = wallpapers.get(
                    laag.eigenschappen.get("wallpaper")
                )
                canvas_breedte = (
                    _positief_geheel(wallpaper.eigenschappen.get("breedte"))
                    if wallpaper is not None
                    else None
                )
                canvas_hoogte = (
                    _positief_geheel(wallpaper.eigenschappen.get("hoogte"))
                    if wallpaper is not None
                    else None
                )
                if (
                    canvas_breedte is not None
                    and canvas_hoogte is not None
                    and (
                        x + breedte > canvas_breedte
                        or y + hoogte > canvas_hoogte
                    )
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4370",
                        boodschap=(
                            f"Assetplaatsing '{plaatsing.id}' valt buiten "
                            f"canvas {canvas_breedte}×{canvas_hoogte}"
                        ),
                        locatie=plaatsing.bronlocatie,
                    ))

            fit = plaatsing.eigenschappen.get("fit")
            if fit not in WALLPAPER_FIT_MODES:
                diagnostics.append(Diagnostic(
                    code="BP4371",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' heeft onbekende "
                        f"fitmodus '{fit}'"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "fit", plaatsing.bronlocatie
                    ),
                ))

            if _dekking(plaatsing.eigenschappen.get("dekking")) is None:
                diagnostics.append(Diagnostic(
                    code="BP4372",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' vereist een "
                        "canonieke dekking tussen 0 en 1"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "dekking", plaatsing.bronlocatie
                    ),
                    ))

            color_role = plaatsing.eigenschappen.get("kleur")
            materiaal = None
            if laag is not None:
                wallpaper = wallpapers.get(
                    laag.eigenschappen.get("wallpaper")
                )
                wereld = (
                    werelden.get(wallpaper.eigenschappen.get("wereld"))
                    if wallpaper is not None
                    else None
                )
                thema = (
                    themas.get(wereld.eigenschappen.get("thema"))
                    if wereld is not None
                    else None
                )
                materiaal = (
                    materialen.get(thema.eigenschappen.get("materiaal"))
                    if thema is not None
                    else None
                )
            if (
                materiaal is None
                or not isinstance(color_role, str)
                or color_role not in materiaal.eigenschappen
            ):
                diagnostics.append(Diagnostic(
                    code="BP4374",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' kan kleurrol "
                        f"'{color_role}' niet uit het wallpaperthema oplossen"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "kleur", plaatsing.bronlocatie
                    ),
                ))

            effect = plaatsing.eigenschappen.get("effect", "solid")
            if effect not in WALLPAPER_EFFECTS:
                diagnostics.append(Diagnostic(
                    code="BP4387",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' heeft onbekend "
                        f"beeldeffect '{effect}'"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "effect", plaatsing.bronlocatie
                    ),
                ))
            elif (
                effect == "radial-glow"
                and asset is not None
                and (
                    asset.eigenschappen.get("vulling") == "none"
                    or asset.eigenschappen.get("lijn") != "none"
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4388",
                    boodschap=(
                        f"Assetplaatsing '{plaatsing.id}' vereist voor "
                        "radial-glow een gevuld asset zonder lijn"
                    ),
                    locatie=plaatsing.eigenschaplocaties.get(
                        "effect", plaatsing.bronlocatie
                    ),
                ))

            if laag is not None and asset is not None:
                laagrol = laag.eigenschappen.get("rol")
                toegestane_assetrollen = WALLPAPER_LAAG_ASSETROLLEN.get(
                    laagrol
                )
                assetrol = (
                    "illustratie"
                    if asset.soort == "muziekcirkel"
                    else asset.eigenschappen.get("rol")
                )
                if (
                    toegestane_assetrollen is not None
                    and assetrol not in toegestane_assetrollen
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4373",
                        boodschap=(
                            f"Assetplaatsing '{plaatsing.id}' gebruikt assetrol "
                            f"'{assetrol}' in "
                            f"wallpaperlaagrol '{laagrol}'"
                        ),
                        locatie=plaatsing.eigenschaplocaties.get(
                            "asset", plaatsing.bronlocatie
                        ),
                    ))

        for product in (
            obj for obj in context.objecten if obj.soort == "product"
        ):
            inhoud = product.eigenschappen.get("inhoud", "composition")
            wallpaper_id = product.eigenschappen.get("wallpaper")
            backend = product.eigenschappen.get("backend")
            if inhoud != WALLPAPER_CONTENT:
                if (
                    "wallpaper" in product.eigenschappen
                    or backend in WALLPAPER_BACKENDS
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4380",
                        boodschap=(
                            f"Product '{product.id}' gebruikt het wallpaperveld "
                            "of de manifestbackend zonder inhoud "
                            f"'{WALLPAPER_CONTENT}'"
                        ),
                        locatie=product.eigenschaplocaties.get(
                            "wallpaper", product.bronlocatie
                        ),
                    ))
                continue

            wallpaper = wallpapers.get(wallpaper_id)
            if wallpaper is None:
                diagnostics.append(Diagnostic(
                    code="BP4381",
                    boodschap=(
                        f"Wallpaperproduct '{product.id}' verwijst naar "
                        f"onbekende wallpaper '{wallpaper_id}'"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "wallpaper", product.bronlocatie
                    ),
                ))
            if backend not in WALLPAPER_BACKENDS:
                diagnostics.append(Diagnostic(
                    code="BP4382",
                    boodschap=(
                        f"Wallpaperproduct '{product.id}' vereist een "
                        "expliciete wallpaperbackend"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "backend", product.bronlocatie
                    ),
                ))
            if product.eigenschappen.get("mode", "interactive") != "static":
                diagnostics.append(Diagnostic(
                    code="BP4383",
                    boodschap=(
                        f"Wallpaperproduct '{product.id}' moet een statische "
                        "architectuursnapshot zijn"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "mode", product.bronlocatie
                    ),
                ))
            if (
                wallpaper is not None
                and product.eigenschappen.get("wereld")
                != wallpaper.eigenschappen.get("wereld")
            ):
                diagnostics.append(Diagnostic(
                    code="BP4384",
                    boodschap=(
                        f"Wallpaperproduct '{product.id}' en wallpaper "
                        f"'{wallpaper.id}' vereisen dezelfde wereld"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "wereld", product.bronlocatie
                    ),
                ))
            if any(
                veld in product.eigenschappen
                for veld in (
                    "compositie",
                    "layout",
                    "asset",
                    "assets",
                    "referentiesecties",
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4385",
                    boodschap=(
                        f"Wallpaperproduct '{product.id}' mag geen compositie, "
                        "layout of ander inhoudscontract declareren"
                    ),
                    locatie=product.bronlocatie,
                ))
            pad = product.eigenschappen.get("pad")
            suffix = WALLPAPER_BACKEND_SUFFIXES.get(backend)
            if (
                not isinstance(pad, str)
                or suffix is None
                or not pad.lower().endswith(suffix)
                or PurePosixPath(pad).is_absolute()
            ):
                diagnostics.append(Diagnostic(
                    code="BP4386",
                    boodschap=(
                        f"Wallpaperproduct '{product.id}' vereist een bij "
                        f"backend '{backend}' passend artifactpad"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "pad", product.bronlocatie
                    ),
                ))

        return tuple(diagnostics)
