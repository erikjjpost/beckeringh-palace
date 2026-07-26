"""Expliciete dependency graph voor het semantische architectuurmodel."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Bronlocatie


@dataclass(frozen=True)
class Relatie:
    """Een gevalideerde, geresolveerde relatie tussen twee objecten."""

    bron_id: str
    relatietype: str
    doel_id: str
    locatie: Bronlocatie | None = None


@dataclass(frozen=True)
class DependencyGraph:
    """Deterministische graaf van architectuurobjecten en hun relaties."""

    knopen: tuple[str, ...]
    relaties: tuple[Relatie, ...]

    def uitgaand(self, bron_id: str, relatietype: str | None = None) -> tuple[Relatie, ...]:
        return tuple(
            relatie
            for relatie in self.relaties
            if relatie.bron_id == bron_id
            and (relatietype is None or relatie.relatietype == relatietype)
        )


def bouw_dependency_graph(knopen: Iterable[str], relaties: Iterable[Relatie]) -> DependencyGraph:
    """Bouw een canoniek geordende graaf uit gevalideerde semantische gegevens."""
    return DependencyGraph(
        knopen=tuple(sorted(set(knopen))),
        relaties=tuple(
            sorted(
                relaties,
                key=lambda relatie: (
                    relatie.bron_id,
                    relatie.relatietype,
                    relatie.doel_id,
                ),
            )
        ),
    )


def _canonieke_cyclus(cyclus: tuple[str, ...]) -> tuple[str, ...]:
    """Normaliseer een gesloten cyclus zodat detectie deterministisch is."""
    kern = cyclus[:-1]
    rotaties = [kern[index:] + kern[:index] for index in range(len(kern))]
    canoniek = min(rotaties)
    return canoniek + (canoniek[0],)


def vind_cycli(graaf: DependencyGraph, relatietype: str) -> tuple[tuple[str, ...], ...]:
    """Vind DFS-terugkoppelingen voor één relatietype, deterministisch genormaliseerd."""
    buren = {
        knoop: tuple(
            sorted(relatie.doel_id for relatie in graaf.uitgaand(knoop, relatietype))
        )
        for knoop in graaf.knopen
    }
    status: dict[str, int] = {knoop: 0 for knoop in graaf.knopen}
    stapel: list[str] = []
    cycli: set[tuple[str, ...]] = set()

    def bezoek(knoop: str) -> None:
        status[knoop] = 1
        stapel.append(knoop)
        for buur in buren[knoop]:
            if status[buur] == 0:
                bezoek(buur)
            elif status[buur] == 1:
                begin = stapel.index(buur)
                cycli.add(_canonieke_cyclus(tuple(stapel[begin:] + [buur])))
        stapel.pop()
        status[knoop] = 2

    for knoop in graaf.knopen:
        if status[knoop] == 0:
            bezoek(knoop)

    return tuple(sorted(cycli))
