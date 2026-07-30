"""Getypeerde, backendonafhankelijke families voor native SVG assets."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.svg_assets import ResolvedSvgAsset, resolveer_svg_assets


SVG_ASSET_FAMILIETYPEN = frozenset({"iconen", "merk"})
SVG_ASSET_FAMILIEROLLEN = {
    "iconen": "icoon",
    "merk": "logo",
}
SVG_MERKFAMILIE_VARIANTEN = frozenset({"merkteken", "woordmerk"})


@dataclass(frozen=True)
class ResolvedSvgAssetFamily:
    """Volledig gevalideerde en geordende SVG assetfamilie."""

    id: str
    naam: str
    doel: str
    familietype: str
    merk: str
    assets: tuple[ResolvedSvgAsset, ...]


class SvgAssetFamilyResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot assetfamilies worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise SvgAssetFamilyResolutionError(
            f"SVG assetfamilie '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def resolveer_svg_assetfamilies(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedSvgAssetFamily, ...]:
    """Los families op zonder renderer- of artifactkennis."""

    objecten = tuple(objecten)
    assets = {
        asset.id: asset
        for asset in resolveer_svg_assets(objecten)
    }
    families = []
    for obj in objecten:
        if obj.soort != "assetfamilie":
            continue
        asset_ids = obj.eigenschappen.get("assets")
        if (
            not isinstance(asset_ids, list)
            or len(asset_ids) < 2
            or not all(isinstance(asset_id, str) for asset_id in asset_ids)
        ):
            raise SvgAssetFamilyResolutionError(
                f"SVG assetfamilie '{obj.id}' is niet semantisch gevalideerd"
            )
        try:
            familie_assets = tuple(assets[asset_id] for asset_id in asset_ids)
        except KeyError as fout:
            raise SvgAssetFamilyResolutionError(
                f"SVG assetfamilie '{obj.id}' bevat onbekend asset '{fout.args[0]}'"
            ) from fout
        families.append(ResolvedSvgAssetFamily(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            familietype=_tekst(obj, "type"),
            merk=_tekst(obj, "merk"),
            assets=familie_assets,
        ))
    return tuple(sorted(families, key=lambda familie: familie.id))


@dataclass(frozen=True)
class SvgAssetFamilyConstraint:
    """Valideer expliciete, wederkerige en getypeerde assetfamilies."""

    sleutel: str = "world-model.svg-asset-families"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        families = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "assetfamilie"
        }
        assets = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "asset"
        }
        merken = {
            obj.id
            for obj in context.objecten
            if obj.soort == "merk"
        }
        toegestane_velden = {
            "naam",
            "doel",
            "type",
            "merk",
            "assets",
        }

        for familie in families.values():
            for naam in familie.eigenschappen:
                if naam not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP4331",
                        boodschap=(
                            f"SVG assetfamilie '{familie.id}' heeft onbekende "
                            f"eigenschap '{naam}'"
                        ),
                        locatie=familie.eigenschaplocaties.get(
                            naam, familie.bronlocatie
                        ),
                    ))

            familietype = familie.eigenschappen.get("type")
            if familietype not in SVG_ASSET_FAMILIETYPEN:
                diagnostics.append(Diagnostic(
                    code="BP4332",
                    boodschap=(
                        f"SVG assetfamilie '{familie.id}' heeft onbekend type "
                        f"'{familietype}'"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "type", familie.bronlocatie
                    ),
                ))

            merk = familie.eigenschappen.get("merk")
            if merk not in merken:
                diagnostics.append(Diagnostic(
                    code="BP4333",
                    boodschap=(
                        f"SVG assetfamilie '{familie.id}' verwijst naar "
                        f"onbekend merk '{merk}'"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "merk", familie.bronlocatie
                    ),
                ))

            asset_ids = familie.eigenschappen.get("assets")
            geldige_lijst = (
                isinstance(asset_ids, list)
                and len(asset_ids) >= 2
                and all(
                    isinstance(asset_id, str) and asset_id.strip()
                    for asset_id in asset_ids
                )
                and len(asset_ids) == len(set(asset_ids))
            )
            if not geldige_lijst:
                diagnostics.append(Diagnostic(
                    code="BP4334",
                    boodschap=(
                        f"SVG assetfamilie '{familie.id}' vereist minstens "
                        "twee unieke geordende assets"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "assets", familie.bronlocatie
                    ),
                ))
                continue

            onbekend = [
                asset_id for asset_id in asset_ids if asset_id not in assets
            ]
            if onbekend:
                diagnostics.append(Diagnostic(
                    code="BP4335",
                    boodschap=(
                        f"SVG assetfamilie '{familie.id}' verwijst naar "
                        f"onbekend asset '{onbekend[0]}'"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "assets", familie.bronlocatie
                    ),
                ))

            bekende_leden = [
                assets[asset_id]
                for asset_id in asset_ids
                if asset_id in assets
            ]
            verwezen_leden = {
                asset.id
                for asset in assets.values()
                if asset.eigenschappen.get("familie") == familie.id
            }
            wederkerig = (
                not onbekend
                and all(
                    asset.eigenschappen.get("familie") == familie.id
                    for asset in bekende_leden
                )
                and verwezen_leden == set(asset_ids)
            )
            if not wederkerig:
                diagnostics.append(Diagnostic(
                    code="BP4337",
                    boodschap=(
                        f"SVG assetfamilie '{familie.id}' vereist een exact "
                        "wederkerige ledenlijst"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "assets", familie.bronlocatie
                    ),
                ))

            varianten = [
                asset.eigenschappen.get("variant")
                for asset in bekende_leden
            ]
            geldige_varianten = (
                len(varianten) == len(asset_ids)
                and all(
                    isinstance(variant, str) and variant.strip()
                    for variant in varianten
                )
                and len(varianten) == len(set(varianten))
            )
            if not geldige_varianten:
                diagnostics.append(Diagnostic(
                    code="BP4338",
                    boodschap=(
                        f"SVG assetfamilie '{familie.id}' vereist voor ieder "
                        "lid een unieke betekenisvolle variant"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "assets", familie.bronlocatie
                    ),
                ))

            verwachte_rol = SVG_ASSET_FAMILIEROLLEN.get(familietype)
            if (
                verwachte_rol is not None
                and any(
                    asset.eigenschappen.get("rol") != verwachte_rol
                    for asset in bekende_leden
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4339",
                    boodschap=(
                        f"SVG assetfamilie '{familie.id}' van type "
                        f"'{familietype}' vereist uitsluitend rol "
                        f"'{verwachte_rol}'"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "type", familie.bronlocatie
                    ),
                ))

            if (
                familietype == "merk"
                and geldige_varianten
                and set(varianten) != SVG_MERKFAMILIE_VARIANTEN
            ):
                diagnostics.append(Diagnostic(
                    code="BP4340",
                    boodschap=(
                        f"SVG merkfamilie '{familie.id}' vereist exact de "
                        "varianten 'merkteken' en 'woordmerk'"
                    ),
                    locatie=familie.eigenschaplocaties.get(
                        "assets", familie.bronlocatie
                    ),
                ))

        for asset in assets.values():
            familie_id = asset.eigenschappen.get("familie")
            variant = asset.eigenschappen.get("variant")
            heeft_familie = "familie" in asset.eigenschappen
            heeft_variant = "variant" in asset.eigenschappen
            if not heeft_familie and not heeft_variant:
                continue
            if (
                not heeft_familie
                or not heeft_variant
                or not isinstance(familie_id, str)
                or not familie_id.strip()
                or not isinstance(variant, str)
                or not variant.strip()
                or familie_id not in families
            ):
                diagnostics.append(Diagnostic(
                    code="BP4336",
                    boodschap=(
                        f"SVG asset '{asset.id}' vereist een bekende familie "
                        "en een betekenisvolle variant"
                    ),
                    locatie=asset.eigenschaplocaties.get(
                        "familie",
                        asset.eigenschaplocaties.get(
                            "variant", asset.bronlocatie
                        ),
                    ),
                ))

        return tuple(diagnostics)
