"""Backend-onafhankelijk contract voor native SVG assetcatalogi."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.svg_asset_families import (
    ResolvedSvgAssetFamily,
    resolveer_svg_assetfamilies,
)
from compiler.svg_assets import ResolvedSvgAsset, resolveer_svg_assets


SVG_ASSET_CATALOG_CONTENT = "asset-catalog"


@dataclass(frozen=True)
class ResolvedSvgAssetCatalogEntry:
    asset: ResolvedSvgAsset
    artifact_product_id: str
    artifact_path: str
    familie: ResolvedSvgAssetFamily | None


@dataclass(frozen=True)
class ResolvedSvgAssetCatalog:
    entries: tuple[ResolvedSvgAssetCatalogEntry, ...]


class SvgAssetCatalogResolutionError(ValueError):
    """Niet gevalideerde CIR kan niet tot een assetcatalogus worden opgelost."""


def resolveer_svg_assetcatalogus(
    objecten: Iterable[Architectuurobject],
    asset_ids: Iterable[str],
) -> ResolvedSvgAssetCatalog:
    objecten = tuple(objecten)
    assets = {
        asset.id: asset
        for asset in resolveer_svg_assets(objecten)
    }
    families = {
        asset.id: familie
        for familie in resolveer_svg_assetfamilies(objecten)
        for asset in familie.assets
    }
    artifact_producten: dict[str, list[Architectuurobject]] = {}
    for obj in objecten:
        if (
            obj.soort == "product"
            and obj.eigenschappen.get("inhoud") == "asset"
        ):
            asset_id = obj.eigenschappen.get("asset")
            if isinstance(asset_id, str):
                artifact_producten.setdefault(asset_id, []).append(obj)

    entries = []
    for asset_id in asset_ids:
        asset = assets.get(asset_id)
        producten = artifact_producten.get(asset_id, [])
        if asset is None or len(producten) != 1:
            raise SvgAssetCatalogResolutionError(
                f"Assetcatalogus kan asset '{asset_id}' niet eenduidig oplossen"
            )
        product = producten[0]
        artifact_path = product.eigenschappen.get("pad")
        if not isinstance(artifact_path, str) or not artifact_path.strip():
            raise SvgAssetCatalogResolutionError(
                f"SVG product '{product.id}' mist een artifactpad"
            )
        entries.append(ResolvedSvgAssetCatalogEntry(
            asset=asset,
            artifact_product_id=product.id,
            artifact_path=artifact_path,
            familie=families.get(asset_id),
        ))
    return ResolvedSvgAssetCatalog(entries=tuple(entries))


@dataclass(frozen=True)
class SvgAssetCatalogConstraint:
    """Valideer expliciete, volledige catalogusdekking vóór backendselectie."""

    sleutel: str = "world-model.svg-asset-catalog"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        assets = {
            obj.id: obj for obj in context.objecten if obj.soort == "asset"
        }
        composities = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "compositie"
        }
        artifact_producten: dict[str, list[Architectuurobject]] = {}
        for obj in context.objecten:
            if (
                obj.soort == "product"
                and obj.eigenschappen.get("inhoud") == "asset"
            ):
                asset_id = obj.eigenschappen.get("asset")
                if isinstance(asset_id, str):
                    artifact_producten.setdefault(asset_id, []).append(obj)

        for product in (
            obj for obj in context.objecten if obj.soort == "product"
        ):
            inhoud = product.eigenschappen.get("inhoud", "composition")
            asset_ids = product.eigenschappen.get("assets")
            if inhoud != SVG_ASSET_CATALOG_CONTENT:
                if "assets" in product.eigenschappen:
                    diagnostics.append(Diagnostic(
                        code="BP4321",
                        boodschap=(
                            f"Product '{product.id}' gebruikt 'assets' zonder "
                            f"inhoud '{SVG_ASSET_CATALOG_CONTENT}'"
                        ),
                        locatie=product.eigenschaplocaties.get(
                            "assets", product.bronlocatie
                        ),
                    ))
                continue

            geldig = (
                isinstance(asset_ids, list)
                and bool(asset_ids)
                and all(
                    isinstance(asset_id, str) and asset_id.strip()
                    for asset_id in asset_ids
                )
                and len(asset_ids) == len(set(asset_ids))
            )
            if not geldig:
                diagnostics.append(Diagnostic(
                    code="BP4322",
                    boodschap=(
                        f"SVG assetcatalogus '{product.id}' vereist een "
                        "niet-lege, unieke lijst 'assets'"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "assets", product.bronlocatie
                    ),
                ))
                continue

            onbekend = [
                asset_id for asset_id in asset_ids if asset_id not in assets
            ]
            if onbekend:
                diagnostics.append(Diagnostic(
                    code="BP4323",
                    boodschap=(
                        f"SVG assetcatalogus '{product.id}' verwijst naar "
                        f"onbekend asset '{onbekend[0]}'"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "assets", product.bronlocatie
                    ),
                ))
            elif set(asset_ids) != set(assets):
                diagnostics.append(Diagnostic(
                    code="BP4324",
                    boodschap=(
                        f"SVG assetcatalogus '{product.id}' vereist expliciete "
                        "dekking van alle native SVG assets"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "assets", product.bronlocatie
                    ),
                ))

            for asset_id in asset_ids:
                if asset_id in assets and len(
                    artifact_producten.get(asset_id, [])
                ) != 1:
                    diagnostics.append(Diagnostic(
                        code="BP4325",
                        boodschap=(
                            f"SVG assetcatalogus '{product.id}' vereist voor "
                            f"asset '{asset_id}' exact één statisch SVG product"
                        ),
                        locatie=product.eigenschaplocaties.get(
                            "assets", product.bronlocatie
                        ),
                    ))

            if product.eigenschappen.get("backend") != "html":
                diagnostics.append(Diagnostic(
                    code="BP4326",
                    boodschap=(
                        f"SVG assetcatalogus '{product.id}' vereist backend "
                        "'html'"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "backend", product.bronlocatie
                    ),
                ))
            if product.eigenschappen.get("mode", "interactive") != "static":
                diagnostics.append(Diagnostic(
                    code="BP4327",
                    boodschap=(
                        f"SVG assetcatalogus '{product.id}' moet een statische "
                        "architectuursnapshot zijn"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "mode", product.bronlocatie
                    ),
                ))
            pad = product.eigenschappen.get("pad")
            if (
                not isinstance(pad, str)
                or PurePosixPath(pad).suffix.lower() != ".html"
            ):
                diagnostics.append(Diagnostic(
                    code="BP4328",
                    boodschap=(
                        f"SVG assetcatalogus '{product.id}' vereist een .html "
                        "artifactpad"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "pad", product.bronlocatie
                    ),
                ))

            compositie_id = product.eigenschappen.get("compositie")
            compositie = composities.get(compositie_id)
            instanties = (
                compositie.eigenschappen.get("instanties")
                if compositie is not None
                else None
            )
            if not isinstance(instanties, list) or len(instanties) != 1:
                diagnostics.append(Diagnostic(
                    code="BP4329",
                    boodschap=(
                        f"SVG assetcatalogus '{product.id}' vereist exact één "
                        "inhoudsinstantie in zijn compositie"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "compositie", product.bronlocatie
                    ),
                ))

        return tuple(diagnostics)
