"""Ingebouwde productbackends."""
from __future__ import annotations

from collections.abc import Iterable

from compiler.backend import Backend, BackendRegistry
from compiler.cir import Architectuurobject
from compiler.product_model import ProductDefinition
from compiler.spatial_html_renderer import naar_spatial_html


def _render_html(
    objecten: Iterable[Architectuurobject],
    product: ProductDefinition,
) -> str:
    return naar_spatial_html(objecten, layout_id=product.layout, titel=product.naam)


def standaard_backend_registry() -> BackendRegistry:
    registry = BackendRegistry()
    registry.registreer(Backend("html", _render_html))
    return registry
