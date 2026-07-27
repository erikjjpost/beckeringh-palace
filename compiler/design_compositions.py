"""Native, backend-onafhankelijk compositiemodel voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


@dataclass(frozen=True)
class ResolvedComponentInstance:
    id: str
    naam: str
    doel: str
    composition_id: str
    component_id: str


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


def _instantie_uit_object(obj: Architectuurobject) -> ResolvedComponentInstance:
    return ResolvedComponentInstance(
        id=obj.id,
        naam=_tekst(obj, "naam"),
        doel=_tekst(obj, "doel"),
        composition_id=_tekst(obj, "compositie"),
        component_id=_tekst(obj, "component"),
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
                _instantie_uit_object(instanties[instance_id])
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
