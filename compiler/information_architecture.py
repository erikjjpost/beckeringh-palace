"""Native informatiearchitectuur voor Beckeringh Palace-producten."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.world_model import Domeinstatus, objectsoortdefinitie


@dataclass(frozen=True)
class ResolvedNavigationTarget:
    id: str
    naam: str
    target_kind: str
    artifact_path: str


@dataclass(frozen=True)
class ResolvedContentAnchor:
    id: str
    naam: str
    object_kind: str
    doel: str


@dataclass(frozen=True)
class ResolvedInformationArea:
    id: str
    naam: str
    doel: str
    accessibility_label: str
    reading_order: int
    object_kinds: tuple[str, ...]
    content_anchors: tuple[ResolvedContentAnchor, ...]
    navigation_targets: tuple[ResolvedNavigationTarget, ...]


@dataclass(frozen=True)
class InformationArchitectureConstraint:
    sleutel: str = "world-model.information-architecture"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        gebieden = tuple(
            obj for obj in context.objecten if obj.soort == "informatiegebied"
        )
        eigenaren: dict[str, str] = {}
        inhoud_eigenaren: dict[str, str] = {}
        navigatie_eigenaren: dict[str, str] = {}
        leesvolgorde_eigenaren: dict[int, str] = {}
        geldige_leesvolgordes: list[int] = []

        for gebied in gebieden:
            for veld in gebied.eigenschappen:
                if veld not in {
                    "naam",
                    "doel",
                    "toegankelijkheidslabel",
                    "leesvolgorde",
                    "soorten",
                    "inhoud",
                    "navigatie",
                }:
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
            toegankelijkheidslabel = gebied.eigenschappen.get(
                "toegankelijkheidslabel"
            )
            if (
                not isinstance(toegankelijkheidslabel, str)
                or not toegankelijkheidslabel.strip()
            ):
                diagnostics.append(Diagnostic(
                    code="BP4013",
                    boodschap=(
                        f"Informatiegebied '{gebied.id}' vereist een betekenisvol "
                        "tekstveld 'toegankelijkheidslabel'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "toegankelijkheidslabel", gebied.bronlocatie
                    ),
                ))
            leesvolgorde = gebied.eigenschappen.get("leesvolgorde")
            try:
                leespositie = int(leesvolgorde)
            except (TypeError, ValueError):
                leespositie = 0
            if (
                isinstance(leesvolgorde, bool)
                or leespositie < 1
                or str(leespositie) != str(leesvolgorde)
            ):
                diagnostics.append(Diagnostic(
                    code="BP4014",
                    boodschap=(
                        f"Informatiegebied '{gebied.id}' vereist een positieve "
                        "gehele 'leesvolgorde'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "leesvolgorde", gebied.bronlocatie
                    ),
                ))
            else:
                eigenaar = leesvolgorde_eigenaren.get(leespositie)
                if eigenaar is not None:
                    diagnostics.append(Diagnostic(
                        code="BP4015",
                        boodschap=(
                            f"Leesvolgorde '{leespositie}' komt voor in zowel "
                            f"informatiegebied '{eigenaar}' als '{gebied.id}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "leesvolgorde", gebied.bronlocatie
                        ),
                    ))
                else:
                    leesvolgorde_eigenaren[leespositie] = gebied.id
                    geldige_leesvolgordes.append(leespositie)
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
            inhoud = gebied.eigenschappen.get("inhoud")
            geldig = (
                isinstance(inhoud, list)
                and bool(inhoud)
                and all(
                    isinstance(anker, str) and bool(anker.strip())
                    for anker in inhoud
                )
                and len(inhoud) == len(set(inhoud))
            )
            if not geldig:
                diagnostics.append(Diagnostic(
                    code="BP4009",
                    boodschap=(
                        f"Informatiegebied '{gebied.id}' vereist een niet-lege, "
                        "unieke lijst 'inhoud'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "inhoud", gebied.bronlocatie
                    ),
                ))
            else:
                for anker_id in inhoud:
                    anker = context.symbolen.get(anker_id)
                    if anker is None:
                        diagnostics.append(Diagnostic(
                            code="BP4010",
                            boodschap=(
                                f"Informatiegebied '{gebied.id}' verwijst naar "
                                f"onbekend inhoudsanker '{anker_id}'"
                            ),
                            locatie=gebied.eigenschaplocaties.get(
                                "inhoud", gebied.bronlocatie
                            ),
                        ))
                    elif anker.soort not in soorten:
                        diagnostics.append(Diagnostic(
                            code="BP4011",
                            boodschap=(
                                f"Inhoudsanker '{anker_id}' van informatiegebied "
                                f"'{gebied.id}' valt buiten de gebiedssoorten"
                            ),
                            locatie=gebied.eigenschaplocaties.get(
                                "inhoud", gebied.bronlocatie
                            ),
                        ))
                    eigenaar = inhoud_eigenaren.get(anker_id)
                    if eigenaar is not None:
                        diagnostics.append(Diagnostic(
                            code="BP4012",
                            boodschap=(
                                f"Inhoudsanker '{anker_id}' komt voor in zowel "
                                f"informatiegebied '{eigenaar}' als '{gebied.id}'"
                            ),
                            locatie=gebied.eigenschaplocaties.get(
                                "inhoud", gebied.bronlocatie
                            ),
                        ))
                    else:
                        inhoud_eigenaren[anker_id] = gebied.id
            navigatie = gebied.eigenschappen.get("navigatie")
            geldig = (
                isinstance(navigatie, list)
                and bool(navigatie)
                and all(
                    isinstance(doel, str) and bool(doel.strip())
                    for doel in navigatie
                )
                and len(navigatie) == len(set(navigatie))
            )
            if not geldig:
                diagnostics.append(Diagnostic(
                    code="BP4005",
                    boodschap=(
                        f"Informatiegebied '{gebied.id}' vereist een niet-lege, "
                        "unieke lijst 'navigatie'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "navigatie", gebied.bronlocatie
                    ),
                ))
                continue
            for doel_id in navigatie:
                doel = context.symbolen.get(doel_id)
                if doel is None:
                    diagnostics.append(Diagnostic(
                        code="BP4006",
                        boodschap=(
                            f"Informatiegebied '{gebied.id}' verwijst naar "
                            f"onbekend navigatiedoel '{doel_id}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "navigatie", gebied.bronlocatie
                        ),
                    ))
                elif doel.soort not in {"product", "renderdoel"}:
                    diagnostics.append(Diagnostic(
                        code="BP4007",
                        boodschap=(
                            f"Navigatiedoel '{doel_id}' van informatiegebied "
                            f"'{gebied.id}' is geen product of renderdoel"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "navigatie", gebied.bronlocatie
                        ),
                    ))
                eigenaar = navigatie_eigenaren.get(doel_id)
                if eigenaar is not None:
                    diagnostics.append(Diagnostic(
                        code="BP4008",
                        boodschap=(
                            f"Navigatiedoel '{doel_id}' komt voor in zowel "
                            f"informatiegebied '{eigenaar}' als '{gebied.id}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "navigatie", gebied.bronlocatie
                        ),
                    ))
                else:
                    navigatie_eigenaren[doel_id] = gebied.id
        if (
            geldige_leesvolgordes
            and sorted(geldige_leesvolgordes)
            != list(range(1, len(gebieden) + 1))
        ):
            diagnostics.append(Diagnostic(
                code="BP4016",
                boodschap=(
                    "Informatiegebieden vereisen een aaneengesloten leesvolgorde "
                    f"van 1 tot en met {len(gebieden)}"
                ),
                locatie=gebieden[0].bronlocatie,
            ))
        return tuple(diagnostics)


def resolveer_informatiegebieden(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedInformationArea, ...]:
    objecten = tuple(objecten)
    symbolen = {obj.id: obj for obj in objecten}
    gebieden = []
    for obj in objecten:
        if obj.soort != "informatiegebied":
            continue
        soorten = obj.eigenschappen["soorten"]
        inhoud = obj.eigenschappen["inhoud"]
        navigatie = obj.eigenschappen["navigatie"]
        assert isinstance(soorten, list)
        assert isinstance(inhoud, list)
        assert isinstance(navigatie, list)
        gebieden.append(ResolvedInformationArea(
            id=obj.id,
            naam=str(obj.eigenschappen["naam"]),
            doel=str(obj.eigenschappen["doel"]),
            accessibility_label=str(
                obj.eigenschappen["toegankelijkheidslabel"]
            ),
            reading_order=int(obj.eigenschappen["leesvolgorde"]),
            object_kinds=tuple(sorted(str(soort) for soort in soorten)),
            content_anchors=tuple(
                ResolvedContentAnchor(
                    id=anker_id,
                    naam=str(symbolen[anker_id].eigenschappen["naam"]),
                    object_kind=symbolen[anker_id].soort,
                    doel=str(symbolen[anker_id].eigenschappen["doel"]),
                )
                for anker_id in inhoud
            ),
            navigation_targets=tuple(
                ResolvedNavigationTarget(
                    id=doel_id,
                    naam=str(symbolen[doel_id].eigenschappen["naam"]),
                    target_kind=symbolen[doel_id].soort,
                    artifact_path=str(symbolen[doel_id].eigenschappen["pad"]),
                )
                for doel_id in navigatie
            ),
        ))
    return tuple(sorted(gebieden, key=lambda gebied: gebied.id))
