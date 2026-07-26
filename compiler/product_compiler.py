"""Compileer productdefinities via een backendregistry."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from compiler.backend import BackendRegistry
from compiler.cir import Architectuurobject
from compiler.product_model import ProductDefinition, verzamel_producten


@dataclass(frozen=True)
class CompiledProduct:
    definitie: ProductDefinition
    inhoud: str


def compileer_producten(
    objecten: Iterable[Architectuurobject],
    registry: BackendRegistry,
) -> tuple[CompiledProduct, ...]:
    objecten = tuple(objecten)
    return tuple(
        CompiledProduct(
            definitie=product,
            inhoud=registry.resolveer(product.backend).render(objecten, product),
        )
        for product in verzamel_producten(objecten)
    )
