"""Compileer productdefinities via een backendregistry."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace
import hashlib
import json

from compiler.backend import BackendRegistry
from compiler.cir import Architectuurobject
from compiler.design_compositions import ResolvedComposition, resolveer_composities
from compiler.design_system_reference import resolveer_designsystemreferentie
from compiler.layout_model import ResolvedLayout, resolveer_layouts
from compiler.product_model import ProductDefinition, verzamel_producten
from compiler.project_status import ProjectStatus
from compiler.svg_assets import ResolvedSvgAsset, resolveer_svg_assets
from compiler.theme_resolution import resolveer_thema


PRODUCT_MODE_LABELS = {
    "interactive": "Interactief product",
    "static": "Statische architectuursnapshot",
}

PRODUCT_MODE_TIME_CONTEXT = {
    "interactive": True,
    "static": False,
}

SNAPSHOT_ALGORITHM = "sha256"


@dataclass(frozen=True)
class CompiledProduct:
    definitie: ProductDefinition
    inhoud: str


def _los_productcontext_op(
    objecten: tuple[Architectuurobject, ...],
    product: ProductDefinition,
    composities: dict[str, ResolvedComposition],
    layouts: dict[str, ResolvedLayout],
    assets: dict[str, ResolvedSvgAsset],
    project_status: ProjectStatus | None,
) -> ProductDefinition:
    thema = resolveer_thema(objecten, product.wereld) if product.wereld else None
    snapshot_id = _snapshot_id(objecten) if product.mode == "static" else ""
    return replace(
        product,
        mode_label=PRODUCT_MODE_LABELS[product.mode],
        has_time_context=PRODUCT_MODE_TIME_CONTEXT[product.mode],
        snapshot_id=snapshot_id,
        snapshot_ref=(
            f"{SNAPSHOT_ALGORITHM}:{snapshot_id}"
            if snapshot_id
            else ""
        ),
        project_status=project_status,
        thema=thema,
        opgeloste_compositie=composities.get(product.compositie),
        opgeloste_layout=layouts.get(product.layout),
        opgelost_asset=assets.get(product.asset),
        design_system_reference=(
            resolveer_designsystemreferentie(
                objecten,
                product.reference_section_ids,
            )
            if product.inhoud == "design-system"
            else None
        ),
    )


def _snapshot_id(objecten: tuple[Architectuurobject, ...]) -> str:
    canoniek = json.dumps(
        [
            obj.als_dict()
            for obj in sorted(objecten, key=lambda obj: (obj.soort, obj.id))
        ],
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canoniek).hexdigest()


def compileer_producten(
    objecten: Iterable[Architectuurobject],
    registry: BackendRegistry,
    project_status: ProjectStatus | None = None,
) -> tuple[CompiledProduct, ...]:
    objecten = tuple(objecten)
    composities = {
        compositie.id: compositie
        for compositie in resolveer_composities(objecten)
    }
    layouts = {layout.id: layout for layout in resolveer_layouts(objecten)}
    assets = {asset.id: asset for asset in resolveer_svg_assets(objecten)}
    return tuple(
        CompiledProduct(
            definitie=opgelost,
            inhoud=registry.resolveer(opgelost.backend).render(objecten, opgelost),
        )
        for product in verzamel_producten(objecten)
        if product.inhoud != "project-status" or project_status is not None
        for opgelost in (
            _los_productcontext_op(
                objecten,
                product,
                composities,
                layouts,
                assets,
                project_status,
            ),
        )
    )
