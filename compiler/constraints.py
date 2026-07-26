"""Deterministische constraint-evaluatie voor semantische BAT-modellen."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol

from compiler.cir import Architectuurobject
from compiler.diagnostics import Diagnostic
from compiler.graph import DependencyGraph


@dataclass(frozen=True)
class ConstraintContext:
    """Gevalideerde semantische gegevens waarop constraints mogen werken."""

    objecten: tuple[Architectuurobject, ...]
    symbolen: dict[str, Architectuurobject]
    dependency_graph: DependencyGraph


class Constraint(Protocol):
    """Uitbreidbare semantische regel met een stabiele evaluatievolgorde."""

    sleutel: str

    def evalueer(self, context: ConstraintContext) -> Iterable[Diagnostic]:
        """Geef nul of meer diagnostics voor deze regel terug."""
        ...


def evalueer_constraints(
    context: ConstraintContext,
    constraints: Iterable[Constraint],
) -> tuple[Diagnostic, ...]:
    """Evalueer constraints deterministisch en verzamel alle diagnostics."""

    diagnostics: list[Diagnostic] = []
    vaste_constraints = tuple(constraints)

    sleutels = [constraint.sleutel for constraint in vaste_constraints]
    if len(sleutels) != len(set(sleutels)):
        raise ValueError("Constraints moeten een unieke sleutel hebben")

    for constraint in sorted(vaste_constraints, key=lambda item: item.sleutel):
        diagnostics.extend(constraint.evalueer(context))

    return tuple(diagnostics)
