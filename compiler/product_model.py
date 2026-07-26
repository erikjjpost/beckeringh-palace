"""Getypeerd productmodel voor backendgestuurde artifacts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


@dataclass(frozen=True)
class ProductDefinition:
    id: str
    naam: str
    doel: str
    backend: str
    layout: str
    pad: str
    bron: Architectuurobject


def product_uit_object(obj: Architectuurobject) -> ProductDefinition | None:
    if obj.soort != "product":
        return None
    return ProductDefinition(
        id=obj.id,
        naam=str(obj.eigenschappen.get("naam", "")),
        doel=str(obj.eigenschappen.get("doel", "")),
        backend=str(obj.eigenschappen.get("backend", "")),
        layout=str(obj.eigenschappen.get("layout", "")),
        pad=str(obj.eigenschappen.get("pad", "")),
        bron=obj,
    )


def verzamel_producten(objecten: Iterable[Architectuurobject]) -> tuple[ProductDefinition, ...]:
    producten = (product_uit_object(obj) for obj in objecten)
    return tuple(sorted(
        (product for product in producten if product is not None),
        key=lambda product: product.id,
    ))
