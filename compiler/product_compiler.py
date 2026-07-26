"""Compileer productdefinities via een backendregistry."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace

from compiler.backend import BackendRegistry
from compiler.cir import Architectuurobject
from compiler.layout_model import ResolvedLayout, resolveer_layouts
from compiler.product_model import ProductDefinition, verzamel_producten
from compiler.theme_resolution import resolveer_thema


@dataclass(frozen=True)
class CompiledProduct:
    definitie: ProductDefinition
    inhoud: str


def _los_productcontext_op(
    objecten: tuple[Architectuurobject, ...],
    product: ProductDefinition,
    layouts: dict[str, ResolvedLayout],
) -> ProductDefinition:
    thema = resolveer_thema(objecten, product.wereld) if product.wereld else None
    return replace(
        product,
        thema=thema,
        opgeloste_layout=layouts.get(product.layout),
    )


def compileer_producten(
    objecten: Iterable[Architectuurobject],
    registry: BackendRegistry,
) -> tuple[CompiledProduct, ...]:
    objecten = tuple(objecten)
    layouts = {layout.id: layout for layout in resolveer_layouts(objecten)}
    return tuple(
        CompiledProduct(
            definitie=opgelost,
            inhoud=registry.resolveer(opgelost.backend).render(objecten, opgelost),
        )
        for product in verzamel_producten(objecten)
        for opgelost in (_los_productcontext_op(objecten, product, layouts),)
    )
