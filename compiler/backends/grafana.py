"""Grafana-backend voor reproduceerbare native gridproducten."""
from __future__ import annotations

import json
from collections.abc import Iterable

from compiler.backend import Backend
from compiler.cir import Architectuurobject
from compiler.layout_model import LayoutType, ResolvedLayout, ResolvedRegion
from compiler.product_model import ProductDefinition

GRAFANA_GRID_COLUMNS = 24
GRAFANA_ROW_HEIGHT = 8


def _gridpositie(layout: ResolvedLayout, region: ResolvedRegion) -> dict[str, int]:
    if None in (
        layout.columns,
        region.column,
        region.row,
        region.column_span,
        region.row_span,
    ):
        raise ValueError(
            f"Grafana-backend vereist volledige gridplaatsing voor region '{region.id}'"
        )

    assert layout.columns is not None
    assert region.column is not None
    assert region.row is not None
    assert region.column_span is not None
    assert region.row_span is not None

    start = ((region.column - 1) * GRAFANA_GRID_COLUMNS) // layout.columns
    einde = (
        (region.column - 1 + region.column_span) * GRAFANA_GRID_COLUMNS
    ) // layout.columns
    return {
        "h": region.row_span * GRAFANA_ROW_HEIGHT,
        "w": einde - start,
        "x": start,
        "y": (region.row - 1) * GRAFANA_ROW_HEIGHT,
    }


def _render(
    _objecten: Iterable[Architectuurobject],
    product: ProductDefinition,
) -> str:
    compositie = product.opgeloste_compositie
    layout = product.opgeloste_layout
    if compositie is None:
        raise ValueError(
            f"Product '{product.id}' vereist een opgeloste native compositie"
        )
    if layout is None:
        raise ValueError(
            f"Product '{product.id}' vereist een opgeloste native layout"
        )
    if layout.type is not LayoutType.GRID:
        raise ValueError(
            f"Grafana-backend ondersteunt alleen native grid-layouts, niet "
            f"'{layout.type.value}'"
        )

    regions_per_instantie = {
        region.instance_id: region
        for region in layout.regions
    }
    panels = []
    for panel_id, instantie in enumerate(compositie.instances, start=1):
        region = regions_per_instantie[instantie.id]
        panels.append(
            {
                "gridPos": _gridpositie(layout, region),
                "id": panel_id,
                "options": {
                    "content": f"### {instantie.naam}",
                    "mode": "markdown",
                },
                "title": instantie.naam,
                "transparent": False,
                "type": "text",
            }
        )

    dashboard = {
        "annotations": {"list": []},
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 0,
        "id": None,
        "links": [],
        "panels": panels,
        "refresh": "",
        "schemaVersion": 41,
        "tags": ["beckeringh-palace", "generated"],
        "templating": {"list": []},
        "time": {"from": "now-6h", "to": "now"},
        "timepicker": {},
        "timezone": "browser",
        "title": product.naam,
        "uid": product.id,
        "version": 1,
    }
    return json.dumps(dashboard, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


backend = Backend("grafana", _render)
