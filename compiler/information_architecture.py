"""Native informatiearchitectuur voor Beckeringh Palace-producten."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.world_model import Domeinstatus, objectsoortdefinitie


@dataclass(frozen=True)
class ResolvedInformationArea:
    id: str
    naam: str
    doel: str
    object_kinds: tuple[str, ...]


@dataclass(frozen=True)
class InformationArchitectureConstraint:
    sleutel: str = "world-model.information-architecture"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        gebieden = tuple(
            obj for obj in context.objecten if obj.soort == "informatiegebied"
        )
        eigenaren: dict[str, str] = {}

        for gebied in gebieden:
            for veld in gebied.eigenschappen:
                if veld not in {"naam", "doel", "soorten"}:
                    diagnostics.append(Diagnostic(
                        code="BP4001",
                        boodschap=(
                            f"Informatiegebied '{gebied.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            veld, gebied.bronlocatie
                        ),
                    ))
            soorten = gebied.eigenschappen.get("soorten")
            geldig = (
                isinstance(soorten, list)
                and bool(soorten)
                and all(
                    isinstance(soort, str) and bool(soort.strip())
                    for soort in soorten
                )
                and len(soorten) == len(set(soorten))
            )
            if not geldig:
                diagnostics.append(Diagnostic(
                    code="BP4002",
                    boodschap=(
                        f"Informatiegebied '{gebied.id}' vereist een niet-lege, "
                        "unieke lijst 'soorten'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "soorten", gebied.bronlocatie
                    ),
                ))
                continue
            for soort in soorten:
                definitie = objectsoortdefinitie(soort)
                if (
                    soort == "informatiegebied"
                    or definitie is None
                    or definitie.status is not Domeinstatus.NATIVE
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4003",
                        boodschap=(
                            f"Informatiegebied '{gebied.id}' bevat onbekende of "
                            f"recursieve objectsoort '{soort}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "soorten", gebied.bronlocatie
                        ),
                    ))
                    continue
                eigenaar = eigenaren.get(soort)
                if eigenaar is not None:
                    diagnostics.append(Diagnostic(
                        code="BP4004",
                        boodschap=(
                            f"Objectsoort '{soort}' komt voor in zowel "
                            f"informatiegebied '{eigenaar}' als '{gebied.id}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "soorten", gebied.bronlocatie
                        ),
                    ))
                else:
                    eigenaren[soort] = gebied.id
        return tuple(diagnostics)


def resolveer_informatiegebieden(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedInformationArea, ...]:
    gebieden = []
    for obj in objecten:
        if obj.soort != "informatiegebied":
            continue
        soorten = obj.eigenschappen["soorten"]
        assert isinstance(soorten, list)
        gebieden.append(ResolvedInformationArea(
            id=obj.id,
            naam=str(obj.eigenschappen["naam"]),
            doel=str(obj.eigenschappen["doel"]),
            object_kinds=tuple(sorted(str(soort) for soort in soorten)),
        ))
    return tuple(sorted(gebieden, key=lambda gebied: gebied.id))
