"""Getypeerd productmodel voor backendgestuurde artifacts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.design_compositions import ResolvedComposition
from compiler.layout_model import ResolvedLayout
from compiler.project_status import ProjectStatus
from compiler.theme_resolution import ResolvedTheme

SNAPSHOT_ID_LENGTH = 12


@dataclass(frozen=True)
class ProductDefinition:
    id: str
    naam: str
    doel: str
    backend: str
    compositie: str
    layout: str
    pad: str
    bron: Architectuurobject
    mode: str = "interactive"
    mode_label: str = ""
    has_time_context: bool = True
    snapshot_id: str = ""
    snapshot_ref: str = ""
    project_status: ProjectStatus | None = None
    wereld: str = ""
    thema: ResolvedTheme | None = None
    opgeloste_compositie: ResolvedComposition | None = None
    opgeloste_layout: ResolvedLayout | None = None


def product_uit_object(obj: Architectuurobject) -> ProductDefinition | None:
    if obj.soort != "product":
        return None
    return ProductDefinition(
        id=obj.id,
        naam=str(obj.eigenschappen.get("naam", "")),
        doel=str(obj.eigenschappen.get("doel", "")),
        backend=str(obj.eigenschappen.get("backend", "")),
        compositie=str(obj.eigenschappen.get("compositie", "")),
        layout=str(obj.eigenschappen.get("layout", "")),
        pad=str(obj.eigenschappen.get("pad", "")),
        bron=obj,
        mode=str(obj.eigenschappen.get("mode", "interactive")),
        wereld=str(obj.eigenschappen.get("wereld", "")),
    )


def verzamel_producten(objecten: Iterable[Architectuurobject]) -> tuple[ProductDefinition, ...]:
    producten = (product_uit_object(obj) for obj in objecten)
    return tuple(sorted(
        (product for product in producten if product is not None),
        key=lambda product: product.id,
    ))
