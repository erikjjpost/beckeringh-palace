"""Native, backend-onafhankelijk compositiemodel voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.design_variants import ResolvedComponentVariant, resolveer_varianten
from compiler.information_architecture import (
    ResolvedInformationArea,
    resolveer_informatiegebieden,
)


@dataclass(frozen=True)
class ResolvedMetricDetail:
    label: str
    value: int | None


@dataclass(frozen=True)
class ResolvedComponentInstance:
    id: str
    naam: str
    doel: str
    composition_id: str
    component_id: str
    variant_id: str | None
    appearance_id: str | None
    information_area_id: str | None
    metric_kind: str | None
    metric_value: int | None
    metric_details: tuple[ResolvedMetricDetail, ...]


@dataclass(frozen=True)
class ResolvedComposition:
    id: str
    naam: str
    doel: str
    instances: tuple[ResolvedComponentInstance, ...]


class CompositionResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot een compositie worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise CompositionResolutionError(
            f"{obj.soort.capitalize()} '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _instantie_uit_object(
    obj: Architectuurobject,
    componenten: dict[str, Architectuurobject],
    varianten: dict[str, ResolvedComponentVariant],
    informatiegebieden: dict[str, ResolvedInformationArea],
    objecten_per_soort: dict[str, int],
    aantal_objecten: int,
    objecten: tuple[Architectuurobject, ...],
) -> ResolvedComponentInstance:
    component_id = _tekst(obj, "component")
    variant_waarde = obj.eigenschappen.get("variant")
    variant_id = variant_waarde if isinstance(variant_waarde, str) else None
    variant = varianten.get(variant_id) if variant_id is not None else None
    metric_waarde = obj.eigenschappen.get("metric-kind")
    metric_detail = obj.eigenschappen.get("metric-detail")
    informatiegebied_waarde = obj.eigenschappen.get("informatiegebied")
    informatiegebied = (
        informatiegebieden.get(informatiegebied_waarde)
        if isinstance(informatiegebied_waarde, str)
        else None
    )
    component = componenten[component_id]
    basisappearance = component.eigenschappen.get("appearance")
    matching_objects = tuple(
        item
        for item in objecten
        if (
            informatiegebied is not None
            and item.soort in informatiegebied.object_kinds
        )
        or metric_waarde == "*"
        or item.soort == metric_waarde
    )
    metric_details: tuple[ResolvedMetricDetail, ...] = ()
    if informatiegebied is not None or metric_detail == "kinds":
        aantallen: dict[str, int] = {}
        for item in matching_objects:
            aantallen[item.soort] = aantallen.get(item.soort, 0) + 1
        metric_details = tuple(
            ResolvedMetricDetail(label=soort, value=aantal)
            for soort, aantal in sorted(aantallen.items())
        )
    elif metric_detail == "items":
        metric_details = tuple(
            ResolvedMetricDetail(
                label=(
                    str(item.eigenschappen.get("naam"))
                    if isinstance(item.eigenschappen.get("naam"), str)
                    else item.id
                ),
                value=None,
            )
            for item in sorted(matching_objects, key=lambda item: item.id)
        )
    return ResolvedComponentInstance(
        id=obj.id,
        naam=informatiegebied.naam if informatiegebied is not None else _tekst(obj, "naam"),
        doel=informatiegebied.doel if informatiegebied is not None else _tekst(obj, "doel"),
        composition_id=_tekst(obj, "compositie"),
        component_id=component_id,
        variant_id=variant_id,
        appearance_id=(
            variant.appearance_id
            if variant is not None
            else basisappearance if isinstance(basisappearance, str) else None
        ),
        information_area_id=(
            informatiegebied.id if informatiegebied is not None else None
        ),
        metric_kind=(
            f"informatiegebied:{informatiegebied.id}"
            if informatiegebied is not None
            else metric_waarde if isinstance(metric_waarde, str) else None
        ),
        metric_value=(
            len(matching_objects)
            if informatiegebied is not None
            else aantal_objecten
            if metric_waarde == "*"
            else objecten_per_soort[metric_waarde]
            if isinstance(metric_waarde, str)
            else None
        ),
        metric_details=metric_details,
    )


def resolveer_composities(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedComposition, ...]:
    """Los gevalideerde composities deterministisch op vanuit de CIR."""

    objecten = tuple(objecten)
    instanties = {
        obj.id: obj
        for obj in objecten
        if obj.soort == "componentinstantie"
    }
    componenten = {
        obj.id: obj
        for obj in objecten
        if obj.soort == "component"
    }
    varianten = {
        variant.id: variant
        for variant in resolveer_varianten(objecten)
    }
    informatiegebieden = {
        gebied.id: gebied
        for gebied in resolveer_informatiegebieden(objecten)
    }
    objecten_per_soort: dict[str, int] = {}
    for obj in objecten:
        objecten_per_soort[obj.soort] = objecten_per_soort.get(obj.soort, 0) + 1
    composities = []
    for obj in objecten:
        if obj.soort != "compositie":
            continue
        instance_ids = obj.eigenschappen.get("instanties")
        if not isinstance(instance_ids, list):
            raise CompositionResolutionError(
                f"Compositie '{obj.id}' vereist lijstveld 'instanties'"
            )
        try:
            resolved_instances = tuple(
                _instantie_uit_object(
                    instanties[instance_id],
                    componenten,
                    varianten,
                    informatiegebieden,
                    objecten_per_soort,
                    len(objecten),
                    objecten,
                )
                for instance_id in instance_ids
            )
        except KeyError as exc:
            raise CompositionResolutionError(
                f"Compositie '{obj.id}' bevat een onbekende componentinstantie"
            ) from exc
        composities.append(ResolvedComposition(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            instances=resolved_instances,
        ))
    return tuple(sorted(composities, key=lambda compositie: compositie.id))
