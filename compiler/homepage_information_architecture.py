"""Native informatiearchitectuur voor de Beckeringh Palace-homepage."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.information_architecture import ResolvedNavigationTarget


@dataclass(frozen=True)
class ResolvedHomepageArea:
    id: str
    naam: str
    doel: str
    role: str
    component_role: str
    component_id: str
    variant_id: str | None
    appearance_id: str
    reading_order: int
    core_message: str
    navigation_targets: tuple[ResolvedNavigationTarget, ...]


@dataclass(frozen=True)
class HomepageInformationArchitectureConstraint:
    sleutel: str = "world-model.homepage-information-architecture"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        gebieden = tuple(
            obj for obj in context.objecten if obj.soort == "homepagegebied"
        )
        leesvolgordes: dict[int, str] = {}
        navigatiedoelen: dict[str, str] = {}
        componenten = {
            obj.id: obj for obj in context.objecten if obj.soort == "component"
        }
        varianten = {
            obj.id: obj for obj in context.objecten if obj.soort == "variant"
        }

        for gebied in gebieden:
            for veld in gebied.eigenschappen:
                if veld not in {
                    "naam",
                    "doel",
                    "rol",
                    "componentrol",
                    "component",
                    "variant",
                    "leesvolgorde",
                    "kernboodschap",
                    "navigatie",
                }:
                    diagnostics.append(Diagnostic(
                        code="BP4101",
                        boodschap=(
                            f"Homepagegebied '{gebied.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            veld, gebied.bronlocatie
                        ),
                    ))

            rol = gebied.eigenschappen.get("rol")
            if rol not in {"entree", "route"}:
                diagnostics.append(Diagnostic(
                    code="BP4102",
                    boodschap=(
                        f"Homepagegebied '{gebied.id}' vereist rol "
                        "'entree' of 'route'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "rol", gebied.bronlocatie
                    ),
                ))

            componentrol = gebied.eigenschappen.get("componentrol")
            verwachte_componentrol = (
                "hero"
                if rol == "entree"
                else "routekaart"
                if rol == "route"
                else None
            )
            if componentrol != verwachte_componentrol:
                diagnostics.append(Diagnostic(
                    code="BP4111",
                    boodschap=(
                        f"Homepagegebied '{gebied.id}' met rol '{rol}' vereist "
                        f"componentrol '{verwachte_componentrol}'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "componentrol", gebied.bronlocatie
                    ),
                ))

            component_id = gebied.eigenschappen.get("component")
            component = (
                componenten.get(component_id)
                if isinstance(component_id, str)
                else None
            )
            if component is None:
                diagnostics.append(Diagnostic(
                    code="BP4112",
                    boodschap=(
                        f"Homepagegebied '{gebied.id}' verwijst naar een "
                        "onbekend component"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "component", gebied.bronlocatie
                    ),
                ))

            variant_id = gebied.eigenschappen.get("variant")
            variant = (
                varianten.get(variant_id)
                if isinstance(variant_id, str)
                else None
            )
            if variant is None:
                diagnostics.append(Diagnostic(
                    code="BP4113",
                    boodschap=(
                        f"Homepagegebied '{gebied.id}' verwijst naar een "
                        "onbekende variant"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "variant", gebied.bronlocatie
                    ),
                ))
            elif variant.eigenschappen.get("component") != component_id:
                diagnostics.append(Diagnostic(
                    code="BP4114",
                    boodschap=(
                        f"Variant '{variant_id}' hoort niet bij component "
                        f"'{component_id}' van homepagegebied '{gebied.id}'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "variant", gebied.bronlocatie
                    ),
                ))

            kernboodschap = gebied.eigenschappen.get("kernboodschap")
            if (
                not isinstance(kernboodschap, str)
                or not kernboodschap.strip()
            ):
                diagnostics.append(Diagnostic(
                    code="BP4103",
                    boodschap=(
                        f"Homepagegebied '{gebied.id}' vereist een "
                        "betekenisvolle 'kernboodschap'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "kernboodschap", gebied.bronlocatie
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
                    code="BP4104",
                    boodschap=(
                        f"Homepagegebied '{gebied.id}' vereist een positieve "
                        "gehele 'leesvolgorde'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "leesvolgorde", gebied.bronlocatie
                    ),
                ))
            elif leespositie in leesvolgordes:
                diagnostics.append(Diagnostic(
                    code="BP4105",
                    boodschap=(
                        f"Leesvolgorde '{leespositie}' komt voor in zowel "
                        f"homepagegebied '{leesvolgordes[leespositie]}' "
                        f"als '{gebied.id}'"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "leesvolgorde", gebied.bronlocatie
                    ),
                ))
            else:
                leesvolgordes[leespositie] = gebied.id

            navigatie = gebied.eigenschappen.get("navigatie")
            if rol == "entree" and "navigatie" in gebied.eigenschappen:
                diagnostics.append(Diagnostic(
                    code="BP4106",
                    boodschap=(
                        f"Entreegebied '{gebied.id}' mag geen navigatiedoel "
                        "bevatten"
                    ),
                    locatie=gebied.eigenschaplocaties.get(
                        "navigatie", gebied.bronlocatie
                    ),
                ))
            if rol == "route":
                doel = (
                    context.symbolen.get(navigatie)
                    if isinstance(navigatie, str)
                    else None
                )
                if (
                    not isinstance(navigatie, str)
                    or not navigatie.strip()
                    or doel is None
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4107",
                        boodschap=(
                            f"Routegebied '{gebied.id}' verwijst naar een "
                            "onbekend navigatiedoel"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "navigatie", gebied.bronlocatie
                        ),
                    ))
                elif doel.soort not in {"product", "renderdoel"}:
                    diagnostics.append(Diagnostic(
                        code="BP4108",
                        boodschap=(
                            f"Navigatiedoel '{navigatie}' van homepagegebied "
                            f"'{gebied.id}' is geen product of renderdoel"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "navigatie", gebied.bronlocatie
                        ),
                    ))
                elif navigatie in navigatiedoelen:
                    diagnostics.append(Diagnostic(
                        code="BP4109",
                        boodschap=(
                            f"Navigatiedoel '{navigatie}' komt voor in zowel "
                            f"homepagegebied '{navigatiedoelen[navigatie]}' "
                            f"als '{gebied.id}'"
                        ),
                        locatie=gebied.eigenschaplocaties.get(
                            "navigatie", gebied.bronlocatie
                        ),
                    ))
                else:
                    navigatiedoelen[navigatie] = gebied.id

        if (
            gebieden
            and sorted(leesvolgordes)
            != list(range(1, len(gebieden) + 1))
        ):
            diagnostics.append(Diagnostic(
                code="BP4110",
                boodschap=(
                    "Homepagegebieden vereisen een aaneengesloten "
                    f"leesvolgorde van 1 tot en met {len(gebieden)}"
                ),
                locatie=gebieden[0].bronlocatie,
            ))
        return tuple(diagnostics)


def resolveer_homepagegebieden(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedHomepageArea, ...]:
    objecten = tuple(objecten)
    symbolen = {obj.id: obj for obj in objecten}
    gebieden = []
    for obj in objecten:
        if obj.soort != "homepagegebied":
            continue
        navigatie = obj.eigenschappen.get("navigatie")
        component_id = str(obj.eigenschappen["component"])
        variant_id = str(obj.eigenschappen["variant"])
        variant = symbolen[variant_id]
        navigatiedoelen = ()
        if isinstance(navigatie, str):
            doel = symbolen[navigatie]
            navigatiedoelen = (ResolvedNavigationTarget(
                id=doel.id,
                naam=str(doel.eigenschappen["naam"]),
                target_kind=doel.soort,
                artifact_path=str(doel.eigenschappen["pad"]),
            ),)
        gebieden.append(ResolvedHomepageArea(
            id=obj.id,
            naam=str(obj.eigenschappen["naam"]),
            doel=str(obj.eigenschappen["doel"]),
            role=str(obj.eigenschappen["rol"]),
            component_role=str(obj.eigenschappen["componentrol"]),
            component_id=component_id,
            variant_id=variant_id,
            appearance_id=str(variant.eigenschappen["appearance"]),
            reading_order=int(obj.eigenschappen["leesvolgorde"]),
            core_message=str(obj.eigenschappen["kernboodschap"]),
            navigation_targets=navigatiedoelen,
        ))
    return tuple(sorted(gebieden, key=lambda gebied: gebied.reading_order))
