"""Semantische analyse voor Beckeringh Architectuurtaal."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import Constraint, ConstraintContext, evalueer_constraints
from compiler.diagnostics import Diagnostic
from compiler.graph import DependencyGraph, Relatie, bouw_dependency_graph, vind_cycli
from compiler.type_system import RELATIESIGNATUREN


class RelatieVorm(str, Enum):
    ENKELVOUDIG_OF_LIJST = "enkelvoudig_of_lijst"


@dataclass(frozen=True)
class RelatieType:
    naam: str
    vorm: RelatieVorm = RelatieVorm.ENKELVOUDIG_OF_LIJST
    acyclisch: bool = False


RELATIETYPEN = {
    relatietype.naam: relatietype
    for relatietype in (
        RelatieType("afhankelijk_van", acyclisch=True),
        RelatieType("eigenaar"),
        RelatieType("gebruikt"),
        RelatieType("realiseert"),
        RelatieType("ondersteunt"),
    )
}


class SemantischeFout(ValueError):
    """BAT is syntactisch geldig, maar semantisch inconsistent."""

    def __init__(self, diagnostics: Iterable[Diagnostic]):
        self.diagnostics = tuple(diagnostics)
        if not self.diagnostics:
            raise ValueError("SemantischeFout vereist ten minste één diagnostic")
        super().__init__("\n".join(str(diagnostic) for diagnostic in self.diagnostics))


@dataclass(frozen=True)
class SemantischModel:
    """Gevalideerde objecten, symbolen en hun dependency graph."""

    objecten: tuple[Architectuurobject, ...]
    symbolen: dict[str, Architectuurobject]
    dependency_graph: DependencyGraph


def _referenties(waarde: object) -> tuple[str, ...] | None:
    if isinstance(waarde, str):
        return (waarde,)
    if isinstance(waarde, list) and all(isinstance(item, str) for item in waarde):
        return tuple(waarde)
    return None


def _verwachte_soorten(soorten: frozenset[str] | None) -> str:
    if soorten is None:
        return "elk objecttype"
    return " of ".join(sorted(soorten))


def _cycluslocatie(
    cyclus: tuple[str, ...],
    relatietype: str,
    relaties: tuple[Relatie, ...],
):
    bron_id = cyclus[-2]
    doel_id = cyclus[-1]
    return next(
        (
            relatie.locatie
            for relatie in relaties
            if relatie.bron_id == bron_id
            and relatie.doel_id == doel_id
            and relatie.relatietype == relatietype
        ),
        None,
    )


def analyseer(
    objecten: Iterable[Architectuurobject],
    constraints: Iterable[Constraint] = (),
) -> SemantischModel:
    """Compileer objecten naar een gevalideerd semantisch model."""
    vaste_objecten = tuple(objecten)
    vaste_constraints = tuple(constraints)
    symbolen: dict[str, Architectuurobject] = {}
    diagnostics: list[Diagnostic] = []
    relaties: list[Relatie] = []

    for obj in vaste_objecten:
        if obj.id in symbolen:
            diagnostics.append(
                Diagnostic(
                    code="BP2001",
                    boodschap=f"Dubbele object-id: {obj.id}",
                    locatie=obj.bronlocatie,
                )
            )
            continue
        symbolen[obj.id] = obj

    for obj in vaste_objecten:
        for eigenschap, waarde in obj.eigenschappen.items():
            relatietype = RELATIETYPEN.get(eigenschap)
            if relatietype is None:
                continue
            locatie = obj.eigenschaplocaties.get(eigenschap, obj.bronlocatie)
            referenties = _referenties(waarde)
            if referenties is None:
                diagnostics.append(
                    Diagnostic(
                        code="BP2101",
                        boodschap=(
                            "Een relatie moet een object-id of een lijst met "
                            "object-id's bevatten"
                        ),
                        locatie=locatie,
                    )
                )
                continue

            signatuur = RELATIESIGNATUREN.get(relatietype.naam)
            if signatuur is not None and not signatuur.accepteert_bron(obj.soort):
                diagnostics.append(
                    Diagnostic(
                        code="BP2301",
                        boodschap=(
                            f"Relatie '{relatietype.naam}' verwacht als bron "
                            f"{_verwachte_soorten(signatuur.bronsoorten)}, "
                            f"maar '{obj.id}' is {obj.soort}"
                        ),
                        locatie=locatie,
                    )
                )
                continue

            for doel_id in referenties:
                doel = symbolen.get(doel_id)
                if doel is None:
                    diagnostics.append(
                        Diagnostic(
                            code="BP2102",
                            boodschap=(
                                f"Onbekende referentie '{doel_id}' in "
                                f"{obj.id}.{eigenschap}"
                            ),
                            locatie=locatie,
                        )
                    )
                    continue
                if signatuur is not None and not signatuur.accepteert_doel(doel.soort):
                    diagnostics.append(
                        Diagnostic(
                            code="BP2302",
                            boodschap=(
                                f"Relatie '{relatietype.naam}' verwacht als doel "
                                f"{_verwachte_soorten(signatuur.doelsoorten)}, "
                                f"maar '{doel.id}' is {doel.soort}"
                            ),
                            locatie=locatie,
                        )
                    )
                    continue
                relaties.append(
                    Relatie(
                        bron_id=obj.id,
                        relatietype=relatietype.naam,
                        doel_id=doel_id,
                        locatie=locatie,
                    )
                )

    dependency_graph = bouw_dependency_graph(symbolen, relaties)

    if not diagnostics:
        for relatietype in RELATIETYPEN.values():
            if not relatietype.acyclisch:
                continue
            for cyclus in vind_cycli(dependency_graph, relatietype.naam):
                diagnostics.append(
                    Diagnostic(
                        code="BP2201",
                        boodschap=(
                            f"Cyclische relatie '{relatietype.naam}': "
                            + " -> ".join(cyclus)
                        ),
                        locatie=_cycluslocatie(
                            cyclus, relatietype.naam, dependency_graph.relaties
                        ),
                    )
                )

    if not diagnostics:
        diagnostics.extend(
            evalueer_constraints(
                ConstraintContext(
                    objecten=vaste_objecten,
                    symbolen=symbolen,
                    dependency_graph=dependency_graph,
                ),
                vaste_constraints,
            )
        )

    if diagnostics:
        raise SemantischeFout(diagnostics)

    return SemantischModel(
        objecten=vaste_objecten,
        symbolen=symbolen,
        dependency_graph=dependency_graph,
    )
