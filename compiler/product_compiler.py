"""Compileer productdefinities via een backendregistry."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, replace

from compiler.backend import BackendRegistry
from compiler.cir import Architectuurobject
from compiler.product_model import ProductDefinition, verzamel_producten
from compiler.theme_resolution import resolveer_thema


@dataclass(frozen=True)
class CompiledProduct:
    definitie: ProductDefinition
    inhoud: str


def _met_opgelost_thema(
    objecten: tuple[Architectuurobject, ...],
    product: ProductDefinition,
) -> ProductDefinition:
    if not product.wereld:
        return product
    return replace(product, thema=resolveer_thema(objecten, product.wereld))


def compileer_producten(
    objecten: Iterable[Architectuurobject],
    registry: BackendRegistry,
) -> tuple[CompiledProduct, ...]:
    objecten = tuple(objecten)
    return tuple(
        CompiledProduct(
            definitie=opgelost,
            inhoud=registry.resolveer(opgelost.backend).render(objecten, opgelost),
        )
        for product in verzamel_producten(objecten)
        for opgelost in (_met_opgelost_thema(objecten, product),)
    )