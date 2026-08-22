"""Getypeerde, backend-onafhankelijke databronnen voor live telemetrie."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic

DATABRON_VELDEN = frozenset({"naam", "doel", "expr", "eenheid", "mapping"})
DATABRON_EENHEDEN = frozenset({"aantal", "percentage", "tekst"})


@dataclass(frozen=True)
class ResolvedDataSourceMapping:
    waarde: str
    label: str


@dataclass(frozen=True)
class ResolvedDataSource:
    id: str
    naam: str
    doel: str
    expr: str
    eenheid: str
    mapping: tuple[ResolvedDataSourceMapping, ...]


class DataSourceResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot databronnen worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise DataSourceResolutionError(
            f"Databron '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _mapping(obj: Architectuurobject) -> tuple[ResolvedDataSourceMapping, ...]:
    waarde = obj.eigenschappen.get("mapping")
    if waarde is None:
        return ()
    if not isinstance(waarde, list) or not waarde:
        raise DataSourceResolutionError(
            f"Databron '{obj.id}' vereist een niet-lege lijst 'mapping'"
        )
    resultaat = []
    for item in waarde:
        if not isinstance(item, str) or ":" not in item:
            raise DataSourceResolutionError(
                f"Databron '{obj.id}' heeft ongeldige mapping-invoer '{item}'"
            )
        sleutel, _, label = item.partition(":")
        resultaat.append(ResolvedDataSourceMapping(waarde=sleutel, label=label))
    return tuple(resultaat)


def resolveer_databronnen(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedDataSource, ...]:
    databronnen = []
    for obj in objecten:
        if obj.soort != "databron":
            continue
        databronnen.append(ResolvedDataSource(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            expr=_tekst(obj, "expr"),
            eenheid=_tekst(obj, "eenheid"),
            mapping=_mapping(obj),
        ))
    return tuple(sorted(databronnen, key=lambda item: item.id))


@dataclass(frozen=True)
class DataSourceConstraint:
    """Valideer databronnen op verplichte velden, eenheid en mapping."""

    sleutel: str = "world-model.data-sources"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        for obj in context.objecten:
            if obj.soort != "databron":
                continue
            for veld in obj.eigenschappen:
                if veld not in DATABRON_VELDEN:
                    diagnostics.append(Diagnostic(
                        code="BP4410",
                        boodschap=(
                            f"Databron '{obj.id}' heeft onbekende eigenschap "
                            f"'{veld}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                    ))
            for veld in ("naam", "doel", "expr", "eenheid"):
                waarde = obj.eigenschappen.get(veld)
                if not isinstance(waarde, str) or not waarde.strip():
                    diagnostics.append(Diagnostic(
                        code="BP4411",
                        boodschap=(
                            f"Databron '{obj.id}' vereist tekstveld '{veld}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                    ))
            eenheid = obj.eigenschappen.get("eenheid")
            if (
                isinstance(eenheid, str)
                and eenheid
                and eenheid not in DATABRON_EENHEDEN
            ):
                diagnostics.append(Diagnostic(
                    code="BP4412",
                    boodschap=(
                        f"Databron '{obj.id}' heeft onbekende eenheid "
                        f"'{eenheid}'"
                    ),
                    locatie=obj.eigenschaplocaties.get("eenheid", obj.bronlocatie),
                ))
            mapping = obj.eigenschappen.get("mapping")
            if mapping is not None:
                if eenheid != "tekst":
                    diagnostics.append(Diagnostic(
                        code="BP4413",
                        boodschap=(
                            f"Databron '{obj.id}' staat 'mapping' alleen toe "
                            "bij eenheid 'tekst'"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "mapping", obj.bronlocatie
                        ),
                    ))
                geldig = (
                    isinstance(mapping, list)
                    and bool(mapping)
                    and all(
                        isinstance(item, str) and ":" in item
                        for item in mapping
                    )
                )
                if not geldig:
                    diagnostics.append(Diagnostic(
                        code="BP4414",
                        boodschap=(
                            f"Databron '{obj.id}' vereist een niet-lege lijst "
                            "'mapping' met 'waarde:label'-items"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "mapping", obj.bronlocatie
                        ),
                    ))
            elif eenheid == "tekst":
                diagnostics.append(Diagnostic(
                    code="BP4415",
                    boodschap=(
                        f"Databron '{obj.id}' vereist 'mapping' bij eenheid "
                        "'tekst'"
                    ),
                    locatie=obj.bronlocatie,
                ))
        return tuple(diagnostics)
