"""Getypeerde merkfamilies voor zelfstandige native wallpapers."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.wallpaper_products import (
    ResolvedWallpaper,
    _positief_geheel,
    resolveer_wallpapers,
)


@dataclass(frozen=True)
class ResolvedWallpaperFamily:
    """Geordende merkfamilie van zelfstandig gespecificeerde wallpapers."""

    id: str
    naam: str
    doel: str
    merk: str
    wallpapers: tuple[ResolvedWallpaper, ...]


class WallpaperFamilyResolutionError(ValueError):
    """Niet gevalideerde CIR kan niet tot wallpaperfamilies worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise WallpaperFamilyResolutionError(
            f"Wallpaperfamilie '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def resolveer_wallpaperfamilies(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedWallpaperFamily, ...]:
    """Los merkgebonden families op zonder een formaat af te leiden."""

    objecten = tuple(objecten)
    wallpapers = {
        wallpaper.id: wallpaper
        for wallpaper in resolveer_wallpapers(objecten)
    }
    families = []
    for obj in objecten:
        if obj.soort != "wallpaperfamilie":
            continue
        wallpaper_ids = obj.eigenschappen.get("wallpapers")
        if (
            not isinstance(wallpaper_ids, list)
            or len(wallpaper_ids) < 2
            or not all(
                isinstance(wallpaper_id, str)
                for wallpaper_id in wallpaper_ids
            )
        ):
            raise WallpaperFamilyResolutionError(
                f"Wallpaperfamilie '{obj.id}' is niet semantisch gevalideerd"
            )
        try:
            familie_wallpapers = tuple(
                wallpapers[wallpaper_id]
                for wallpaper_id in wallpaper_ids
            )
        except KeyError as fout:
            raise WallpaperFamilyResolutionError(
                f"Wallpaperfamilie '{obj.id}' bevat onbekende wallpaper "
                f"'{fout.args[0]}'"
            ) from fout
        families.append(ResolvedWallpaperFamily(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            merk=_tekst(obj, "merk"),
            wallpapers=familie_wallpapers,
        ))
    return tuple(sorted(families, key=lambda familie: familie.id))


@dataclass(frozen=True)
class WallpaperFamilyConstraint:
    """Valideer merkbinding, varianten en zelfstandige canvasformaten."""

    sleutel: str = "world-model.wallpaper-families"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        families = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "wallpaperfamilie"
        }
        wallpapers = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "wallpaper"
        }
        merken = {
            obj.id
            for obj in context.objecten
            if obj.soort == "merk"
        }

        for familie in families.values():
            toegestane_velden = {
                "naam",
                "doel",
                "merk",
                "wallpapers",
            }
            for veld in familie.eigenschappen:
                if veld not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP4390",
                        boodschap=(
                            f"Wallpaperfamilie '{familie.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=familie.eigenschaplocaties.get(
                            veld, familie.bronlocatie
                        ),
                    ))

            familie_merk = familie.eigenschappen.get("merk")
            if familie_merk not in merken:
                diagnostics.append(Diagnostic(
                    code="BP4391",
                    boodschap=(
                        f"Wallpaperfamilie '{familie.id}' verwijst naar "
                        f"onbekend merk '{familie_merk}'"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "merk", familie.bronlocatie
                    ),
                ))

            wallpaper_ids = familie.eigenschappen.get("wallpapers")
            geldige_lijst = (
                isinstance(wallpaper_ids, list)
                and len(wallpaper_ids) >= 2
                and all(
                    isinstance(wallpaper_id, str) and wallpaper_id.strip()
                    for wallpaper_id in wallpaper_ids
                )
                and len(wallpaper_ids) == len(set(wallpaper_ids))
            )
            if not geldige_lijst:
                diagnostics.append(Diagnostic(
                    code="BP4392",
                    boodschap=(
                        f"Wallpaperfamilie '{familie.id}' vereist minstens "
                        "twee unieke geordende wallpapers"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "wallpapers", familie.bronlocatie
                    ),
                ))
                continue

            onbekende_wallpapers = [
                wallpaper_id
                for wallpaper_id in wallpaper_ids
                if wallpaper_id not in wallpapers
            ]
            if onbekende_wallpapers:
                diagnostics.append(Diagnostic(
                    code="BP4393",
                    boodschap=(
                        f"Wallpaperfamilie '{familie.id}' verwijst naar "
                        f"onbekende wallpaper '{onbekende_wallpapers[0]}'"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "wallpapers", familie.bronlocatie
                    ),
                ))

            bekende_leden = [
                wallpapers[wallpaper_id]
                for wallpaper_id in wallpaper_ids
                if wallpaper_id in wallpapers
            ]
            verwezen_leden = {
                wallpaper.id
                for wallpaper in wallpapers.values()
                if wallpaper.eigenschappen.get("familie") == familie.id
            }
            if (
                onbekende_wallpapers
                or verwezen_leden != set(wallpaper_ids)
                or any(
                    wallpaper.eigenschappen.get("familie") != familie.id
                    for wallpaper in bekende_leden
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4394",
                    boodschap=(
                        f"Wallpaperfamilie '{familie.id}' vereist een exact "
                        "wederkerige ledenlijst"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "wallpapers", familie.bronlocatie
                    ),
                ))

            varianten = [
                wallpaper.eigenschappen.get("variant")
                for wallpaper in bekende_leden
            ]
            if (
                len(varianten) != len(wallpaper_ids)
                or not all(
                    isinstance(variant, str) and variant.strip()
                    for variant in varianten
                )
                or len(varianten) != len(set(varianten))
            ):
                diagnostics.append(Diagnostic(
                    code="BP4395",
                    boodschap=(
                        f"Wallpaperfamilie '{familie.id}' vereist voor ieder "
                        "lid een unieke betekenisvolle variant"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "wallpapers", familie.bronlocatie
                    ),
                ))

            if any(
                wallpaper.eigenschappen.get("merk") != familie_merk
                for wallpaper in bekende_leden
            ):
                diagnostics.append(Diagnostic(
                    code="BP4396",
                    boodschap=(
                        f"Wallpaperfamilie '{familie.id}' en al haar leden "
                        "vereisen hetzelfde merk"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "merk", familie.bronlocatie
                    ),
                ))

            canvasformaten = [
                (
                    _positief_geheel(
                        wallpaper.eigenschappen.get("breedte")
                    ),
                    _positief_geheel(
                        wallpaper.eigenschappen.get("hoogte")
                    ),
                )
                for wallpaper in bekende_leden
            ]
            geldige_canvasformaten = [
                formaat
                for formaat in canvasformaten
                if None not in formaat
            ]
            if (
                len(geldige_canvasformaten) == len(wallpaper_ids)
                and len(geldige_canvasformaten)
                != len(set(geldige_canvasformaten))
            ):
                diagnostics.append(Diagnostic(
                    code="BP4397",
                    boodschap=(
                        f"Wallpaperfamilie '{familie.id}' vereist voor ieder "
                        "lid een uniek expliciet canvasformaat"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "wallpapers", familie.bronlocatie
                    ),
                ))

        for wallpaper in wallpapers.values():
            familie_id = wallpaper.eigenschappen.get("familie")
            variant = wallpaper.eigenschappen.get("variant")
            heeft_familie = "familie" in wallpaper.eigenschappen
            heeft_variant = "variant" in wallpaper.eigenschappen
            if (
                heeft_familie != heeft_variant
                or (
                    heeft_familie
                    and (
                        familie_id not in families
                        or not isinstance(variant, str)
                        or not variant.strip()
                    )
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4398",
                    boodschap=(
                        f"Wallpaper '{wallpaper.id}' vereist samen een "
                        "bekende familie en betekenisvolle variant"
                    ),
                    locatie=wallpaper.eigenschaplocaties.get(
                        "familie",
                        wallpaper.eigenschaplocaties.get(
                            "variant", wallpaper.bronlocatie
                        ),
                    ),
                ))

        return tuple(diagnostics)
