"""Grafana-backend voor reproduceerbare native gridproducten."""
from __future__ import annotations

import json
import re
from collections.abc import Iterable

from compiler.backend import Backend
from compiler.cir import Architectuurobject
from compiler.design_components import ComponentAppearance, verzamel_appearances
from compiler.design_compositions import ResolvedComponentInstance
from compiler.layout_model import LayoutType, ResolvedLayout, ResolvedRegion
from compiler.product_model import ProductDefinition
from compiler.theme_resolution import ResolvedTheme

GRAFANA_GRID_COLUMNS = 24
GRAFANA_ROW_HEIGHT = 16
GRAFANA_HEADER_HEIGHT = 4
PIXELWAARDE = re.compile(r"^(?P<waarde>\d+(?:\.\d+)?)px$")


def _grafana_stijl(product: ProductDefinition) -> str:
    thema = product.thema
    if thema is None:
        raise ValueError(
            f"Grafana-product '{product.id}' vereist een opgelost native thema"
        )
    achtergrond = thema.palet.kleur("background")
    if achtergrond is None:
        raise ValueError(
            f"Grafana-product '{product.id}' vereist de themarol 'background'"
        )
    waarde = achtergrond.waarde
    if len(waarde) != 7 or not waarde.startswith("#"):
        raise ValueError(
            f"Grafana-product '{product.id}' vereist een hex backgroundkleur"
        )
    try:
        rood, groen, blauw = (
            int(waarde[index:index + 2], 16)
            for index in (1, 3, 5)
        )
    except ValueError as exc:
        raise ValueError(
            f"Grafana-product '{product.id}' vereist een hex backgroundkleur"
        ) from exc
    luminantie = (299 * rood + 587 * groen + 114 * blauw) / 1000
    return "dark" if luminantie < 128 else "light"


def _paneelbeschrijving(instantie: ResolvedComponentInstance) -> str:
    identiteit = [
        f"BAT component: {instantie.component_id}",
        f"BAT appearance: {instantie.appearance_id or 'none'}",
    ]
    if instantie.variant_id is not None:
        identiteit.insert(1, f"BAT variant: {instantie.variant_id}")
    return f"{instantie.doel}\n\n" + "\n".join(identiteit)


def _pixels(waarde: str, context: str) -> float:
    match = PIXELWAARDE.fullmatch(waarde)
    if match is None:
        raise ValueError(f"Grafana Canvas vereist een px-waarde voor {context}")
    getal = float(match.group("waarde"))
    return int(getal) if getal.is_integer() else getal


def _appearance_waarde(
    appearance: ComponentAppearance,
    rol: str,
    context: str,
) -> str:
    waarde = appearance.rol(rol)
    if waarde is None:
        raise ValueError(
            f"Grafana Canvas vereist appearance-rol '{rol}' voor {context}"
        )
    return waarde


def _themakleur(thema: ResolvedTheme, groep: str, rol: str) -> str:
    bron = thema.materiaal if groep == "materiaal" else thema.palet
    kleur = None if bron is None else bron.kleur(rol)
    if kleur is None:
        raise ValueError(
            f"Grafana Canvas vereist themakleur '{groep}.{rol}'"
        )
    return kleur.waarde


def _canvasopties(
    instantie: ResolvedComponentInstance,
    appearance: ComponentAppearance,
    thema: ResolvedTheme,
    metric_value: int | None,
) -> dict[str, object]:
    if None in (thema.border, thema.spacing, thema.typeschaal):
        raise ValueError(
            f"Grafana Canvas vereist border, spacing en typeschaal voor "
            f"appearance '{appearance.id}'"
        )
    assert thema.border is not None
    assert thema.spacing is not None
    assert thema.typeschaal is not None

    materiaalrol = _appearance_waarde(
        appearance, "material", f"appearance '{appearance.id}'"
    )
    voorgrondrol = _appearance_waarde(
        appearance, "foreground", f"appearance '{appearance.id}'"
    )
    accentrol = _appearance_waarde(
        appearance, "accent", f"appearance '{appearance.id}'"
    )
    borderrol = _appearance_waarde(
        appearance, "border", f"appearance '{appearance.id}'"
    )
    spacingrol = _appearance_waarde(
        appearance, "spacing", f"appearance '{appearance.id}'"
    )
    headingrol = _appearance_waarde(
        appearance, "heading-style", f"appearance '{appearance.id}'"
    )
    bodyrol = _appearance_waarde(
        appearance, "body-style", f"appearance '{appearance.id}'"
    )
    captionrol = _appearance_waarde(
        appearance, "caption-style", f"appearance '{appearance.id}'"
    )

    padding = _pixels(getattr(thema.spacing, spacingrol), f"spacing.{spacingrol}")
    borderbreedte = _pixels(
        getattr(thema.border, borderrol), f"border.{borderrol}"
    )
    headinggrootte = _pixels(
        getattr(thema.typeschaal, headingrol), f"typeschaal.{headingrol}"
    )
    bodygrootte = _pixels(
        getattr(thema.typeschaal, bodyrol), f"typeschaal.{bodyrol}"
    )
    captiongrootte = _pixels(
        getattr(thema.typeschaal, captionrol), f"typeschaal.{captionrol}"
    )
    achtergrond = _themakleur(thema, "materiaal", materiaalrol)
    voorgrond = _themakleur(thema, "materiaal", voorgrondrol)
    accent = _themakleur(thema, "materiaal", accentrol)
    tekstlinks = padding + 12

    elementen = [
        {
            "background": {"color": {"fixed": accent}},
            "border": {"color": {"fixed": accent}, "width": 0},
            "constraint": {"horizontal": "left", "vertical": "top"},
            "name": f"{instantie.id}-accent",
            "placement": {
                "height": headinggrootte + bodygrootte + 12,
                "left": padding,
                "top": padding,
                "width": 4,
            },
            "type": "rectangle",
        },
        {
            "config": {
                "align": "left",
                "color": {"fixed": voorgrond},
                "size": headinggrootte,
                "text": {"fixed": instantie.naam, "mode": "fixed"},
                "valign": "top",
            },
            "constraint": {"horizontal": "left", "vertical": "top"},
            "name": f"{instantie.id}-heading",
            "placement": {
                "height": headinggrootte + 8,
                "left": tekstlinks,
                "top": padding,
                "width": 360,
            },
            "type": "text",
        },
    ]
    body_top = padding + headinggrootte + 12
    if metric_value is not None:
        metric_size = headinggrootte * 2
        elementen.append(
            {
                "config": {
                    "align": "left",
                    "color": {"fixed": accent},
                    "size": metric_size,
                    "text": {"fixed": str(metric_value), "mode": "fixed"},
                    "valign": "top",
                },
                "constraint": {"horizontal": "left", "vertical": "top"},
                "name": f"{instantie.id}-metric",
                "placement": {
                    "height": metric_size + 8,
                    "left": tekstlinks,
                    "top": body_top,
                    "width": 360,
                },
                "type": "text",
            }
        )
        body_top += metric_size + 12
    if instantie.metric_details:
        detailregels = tuple(
            (
                f"{detail.label}  {detail.value}"
                if detail.value is not None
                else detail.label
            )
            for detail in instantie.metric_details
        )
        detailhoogte = captiongrootte * (len(detailregels) + 1)
        elementen.append(
            {
                "config": {
                    "align": "left",
                    "color": {"fixed": voorgrond},
                    "size": captiongrootte,
                    "text": {"fixed": "\n".join(detailregels), "mode": "fixed"},
                    "valign": "top",
                },
                "constraint": {"horizontal": "left", "vertical": "top"},
                "name": f"{instantie.id}-metric-details",
                "placement": {
                    "height": detailhoogte,
                    "left": tekstlinks,
                    "top": body_top,
                    "width": 360,
                },
                "type": "text",
            }
        )
        body_top += detailhoogte + 12
    elementen.append(
        {
            "config": {
                "align": "left",
                "color": {"fixed": voorgrond},
                "size": bodygrootte,
                "text": {"fixed": instantie.doel, "mode": "fixed"},
                "valign": "top",
            },
            "constraint": {"horizontal": "left", "vertical": "top"},
            "name": f"{instantie.id}-body",
            "placement": {
                "height": bodygrootte * 3,
                "left": tekstlinks,
                "top": body_top,
                "width": 360,
            },
            "type": "text",
        }
    )
    elementen[0]["placement"]["height"] = body_top + bodygrootte * 3 - padding

    return {
        "infinitePan": False,
        "inlineEditing": False,
        "panZoom": False,
        "root": {
            "background": {"color": {"fixed": achtergrond}},
            "border": {
                "color": {"fixed": accent},
                "width": borderbreedte,
            },
            "elements": elementen,
            "name": "Root",
            "type": "frame",
        },
        "showAdvancedTypes": False,
    }


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
        "y": GRAFANA_HEADER_HEIGHT + (region.row - 1) * GRAFANA_ROW_HEIGHT,
    }


def _dashboard_header(
    product: ProductDefinition,
    compositie_naam: str,
    compositie_doel: str,
) -> dict[str, object]:
    assert product.thema is not None
    thema = product.thema
    if thema.typeschaal is None or thema.spacing is None:
        raise ValueError(
            f"Grafana dashboardheader vereist typeschaal en spacing voor "
            f"product '{product.id}'"
        )
    voorgrond = _themakleur(thema, "materiaal", "foreground")
    accent = _themakleur(thema, "materiaal", "accent")
    achtergrond = _themakleur(thema, "materiaal", "canvas")
    padding = _pixels(thema.spacing.medium, "spacing.medium")
    titelgrootte = _pixels(thema.typeschaal.title, "typeschaal.title")
    labelgrootte = _pixels(thema.typeschaal.label, "typeschaal.label")
    bodygrootte = _pixels(thema.typeschaal.body, "typeschaal.body")
    return {
        "description": compositie_doel,
        "gridPos": {"h": GRAFANA_HEADER_HEIGHT, "w": 24, "x": 0, "y": 0},
        "id": 1,
        "options": {
            "infinitePan": False,
            "inlineEditing": False,
            "panZoom": False,
            "root": {
                "background": {"color": {"fixed": achtergrond}},
                "border": {"color": {"fixed": accent}, "width": 0},
                "elements": [
                    {
                        "config": {
                            "align": "left",
                            "color": {"fixed": accent},
                            "size": labelgrootte,
                            "text": {
                                "fixed": (
                                    f"{thema.wereld_naam} · {thema.thema_naam} "
                                    "· Gegenereerd uit BAT"
                                ),
                                "mode": "fixed",
                            },
                            "valign": "top",
                        },
                        "constraint": {"horizontal": "left", "vertical": "top"},
                        "name": f"{product.id}-identity",
                        "placement": {
                            "height": labelgrootte + 8,
                            "left": padding,
                            "top": padding,
                            "width": 720,
                        },
                        "type": "text",
                    },
                    {
                        "config": {
                            "align": "left",
                            "color": {"fixed": voorgrond},
                            "size": titelgrootte,
                            "text": {"fixed": compositie_naam, "mode": "fixed"},
                            "valign": "top",
                        },
                        "constraint": {"horizontal": "left", "vertical": "top"},
                        "name": f"{product.id}-title",
                        "placement": {
                            "height": titelgrootte + 8,
                            "left": padding,
                            "top": padding + labelgrootte + 8,
                            "width": 720,
                        },
                        "type": "text",
                    },
                    {
                        "config": {
                            "align": "left",
                            "color": {"fixed": voorgrond},
                            "size": bodygrootte,
                            "text": {"fixed": compositie_doel, "mode": "fixed"},
                            "valign": "top",
                        },
                        "constraint": {"horizontal": "left", "vertical": "top"},
                        "name": f"{product.id}-purpose",
                        "placement": {
                            "height": bodygrootte + 8,
                            "left": padding + 760,
                            "top": padding + labelgrootte + 16,
                            "width": 720,
                        },
                        "type": "text",
                    },
                ],
                "name": "Root",
                "type": "frame",
            },
            "showAdvancedTypes": False,
        },
        "title": compositie_naam,
        "transparent": True,
        "type": "canvas",
    }


def _render(
    objecten: Iterable[Architectuurobject],
    product: ProductDefinition,
) -> str:
    objecten = tuple(objecten)
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
    stijl = _grafana_stijl(product)
    assert product.thema is not None
    appearances = {
        appearance.id: appearance
        for appearance in verzamel_appearances(objecten)
    }
    regions_per_instantie = {
        region.instance_id: region
        for region in layout.regions
    }
    panels = [_dashboard_header(product, compositie.naam, compositie.doel)]
    for panel_id, instantie in enumerate(compositie.instances, start=2):
        region = regions_per_instantie[instantie.id]
        appearance = appearances.get(instantie.appearance_id or "")
        if appearance is None:
            raise ValueError(
                f"Grafana Canvas vereist een opgeloste appearance voor "
                f"componentinstantie '{instantie.id}'"
            )
        panels.append(
            {
                "description": _paneelbeschrijving(instantie),
                "gridPos": _gridpositie(layout, region),
                "id": panel_id,
                "options": _canvasopties(
                    instantie,
                    appearance,
                    product.thema,
                    instantie.metric_value,
                ),
                "title": instantie.naam,
                "transparent": True,
                "type": "canvas",
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
        "style": stijl,
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
