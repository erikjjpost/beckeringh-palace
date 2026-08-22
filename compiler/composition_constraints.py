"""Semantische constraints voor Beckeringh Palace-composities."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class DesignCompositionConstraint:
    sleutel: str = "world-model.design-compositions"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        objectsoorten = {obj.soort for obj in context.objecten}
        componenten = {obj.id for obj in context.objecten if obj.soort == "component"}
        composities = {obj.id: obj for obj in context.objecten if obj.soort == "compositie"}
        instanties = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "componentinstantie"
        }
        informatiegebieden = {
            obj.id for obj in context.objecten if obj.soort == "informatiegebied"
        }
        homepagegebieden = {
            obj.id for obj in context.objecten if obj.soort == "homepagegebied"
        }
        voorbeelden = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "componentvoorbeeld"
        }
        databronnen = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "databron"
        }

        for obj in context.objecten:
            if obj.soort == "compositie":
                toegestane_velden = {"naam", "doel", "rol", "instanties"}
                for naam in obj.eigenschappen:
                    if naam not in toegestane_velden:
                        diagnostics.append(Diagnostic(
                            code="BP3701",
                            boodschap=f"Compositie '{obj.id}' heeft onbekende eigenschap '{naam}'",
                            locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                        ))
                waarden = obj.eigenschappen.get("instanties")
                geldig = (
                    isinstance(waarden, list)
                    and bool(waarden)
                    and all(
                        isinstance(item, str) and bool(item.strip())
                        for item in waarden
                    )
                    and len(waarden) == len(set(waarden))
                )
                if not geldig:
                    diagnostics.append(Diagnostic(
                        code="BP3702",
                        boodschap=(
                            f"Compositie '{obj.id}' vereist een niet-lege, "
                            "unieke lijst 'instanties'"
                        ),
                        locatie=obj.eigenschaplocaties.get("instanties", obj.bronlocatie),
                    ))
                rol = obj.eigenschappen.get("rol")
                if rol is not None and rol not in {
                    "login-formulier",
                    "terminal-sessie",
                }:
                    diagnostics.append(Diagnostic(
                        code="BP3705",
                        boodschap=(
                            f"Compositie '{obj.id}' heeft onbekende rol '{rol}'"
                        ),
                        locatie=obj.eigenschaplocaties.get("rol", obj.bronlocatie),
                    ))
                if geldig:
                    for instance_id in waarden:
                        instantie = instanties.get(instance_id)
                        if instantie is None:
                            diagnostics.append(Diagnostic(
                                code="BP3703",
                                boodschap=(
                                    f"Compositie '{obj.id}' verwijst naar onbekende "
                                    f"componentinstantie '{instance_id}'"
                                ),
                                locatie=obj.eigenschaplocaties.get(
                                    "instanties",
                                    obj.bronlocatie,
                                ),
                            ))
                        elif instantie.eigenschappen.get("compositie") != obj.id:
                            diagnostics.append(Diagnostic(
                                code="BP3704",
                                boodschap=(
                                    f"Componentinstantie '{instance_id}' verwijst niet "
                                    f"terug naar compositie '{obj.id}'"
                                ),
                                locatie=instantie.eigenschaplocaties.get(
                                    "compositie",
                                    instantie.bronlocatie,
                                ),
                            ))

            if obj.soort == "componentinstantie":
                toegestane_velden = {
                    "naam",
                    "doel",
                    "compositie",
                    "component",
                    "variant",
                    "metric-kind",
                    "metric-detail",
                    "informatiegebied",
                    "homepagegebied",
                    "navigatie",
                    "voorbeeld",
                    "databron",
                }
                for naam in obj.eigenschappen:
                    if naam not in toegestane_velden:
                        diagnostics.append(Diagnostic(
                            code="BP3710",
                            boodschap=(
                                f"Componentinstantie '{obj.id}' heeft onbekende "
                                f"eigenschap '{naam}'"
                            ),
                            locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                        ))
                composition_id = obj.eigenschappen.get("compositie")
                compositie = (
                    composities.get(composition_id)
                    if isinstance(composition_id, str)
                    else None
                )
                if compositie is None:
                    diagnostics.append(Diagnostic(
                        code="BP3711",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' verwijst naar onbekende "
                            f"compositie '{composition_id}'"
                        ),
                        locatie=obj.eigenschaplocaties.get("compositie", obj.bronlocatie),
                    ))
                else:
                    composition_instances = compositie.eigenschappen.get("instanties")
                    if (
                        not isinstance(composition_instances, list)
                        or obj.id not in composition_instances
                    ):
                        diagnostics.append(Diagnostic(
                            code="BP3712",
                            boodschap=(
                                f"Compositie '{composition_id}' noemt "
                                f"componentinstantie '{obj.id}' niet"
                            ),
                            locatie=compositie.eigenschaplocaties.get(
                                "instanties",
                                compositie.bronlocatie,
                            ),
                        ))
                component_id = obj.eigenschappen.get("component")
                homepagegebied = obj.eigenschappen.get("homepagegebied")
                voorbeeld_id = obj.eigenschappen.get("voorbeeld")
                voorbeeld = (
                    voorbeelden.get(voorbeeld_id)
                    if isinstance(voorbeeld_id, str)
                    else None
                )
                if (
                    "homepagegebied" not in obj.eigenschappen
                    and "voorbeeld" not in obj.eigenschappen
                    and component_id not in componenten
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3713",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' verwijst naar onbekend "
                            f"component '{component_id}'"
                        ),
                        locatie=obj.eigenschaplocaties.get("component", obj.bronlocatie),
                    ))
                if "voorbeeld" in obj.eigenschappen and voorbeeld is None:
                    diagnostics.append(Diagnostic(
                        code="BP3719",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' verwijst naar onbekend "
                            f"componentvoorbeeld '{voorbeeld_id}'"
                        ),
                        locatie=obj.eigenschaplocaties.get("voorbeeld", obj.bronlocatie),
                    ))
                if voorbeeld is not None:
                    conflicten = {
                        "component",
                        "variant",
                        "informatiegebied",
                        "homepagegebied",
                        "metric-kind",
                        "metric-detail",
                        "navigatie",
                    }.intersection(obj.eigenschappen)
                    if conflicten:
                        diagnostics.append(Diagnostic(
                            code="BP3720",
                            boodschap=(
                                f"Componentinstantie '{obj.id}' combineert "
                                f"'voorbeeld' met {', '.join(sorted(conflicten))}"
                            ),
                            locatie=obj.eigenschaplocaties.get(
                                "voorbeeld", obj.bronlocatie
                            ),
                        ))
                databron_id = obj.eigenschappen.get("databron")
                if (
                    "databron" in obj.eigenschappen
                    and databron_id not in databronnen
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3721",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' verwijst naar "
                            f"onbekende databron '{databron_id}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "databron", obj.bronlocatie
                        ),
                    ))
                metric_kind = obj.eigenschappen.get("metric-kind")
                informatiegebied = obj.eigenschappen.get("informatiegebied")
                if (
                    "informatiegebied" in obj.eigenschappen
                    and informatiegebied not in informatiegebieden
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3717",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' verwijst naar "
                            f"onbekend informatiegebied '{informatiegebied}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "informatiegebied", obj.bronlocatie
                        ),
                    ))
                if (
                    "informatiegebied" in obj.eigenschappen
                    and (
                        "metric-kind" in obj.eigenschappen
                        or "metric-detail" in obj.eigenschappen
                    )
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3718",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' combineert "
                            "'informatiegebied' met legacy metriekvelden"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "informatiegebied", obj.bronlocatie
                        ),
                    ))
                if (
                    "metric-kind" in obj.eigenschappen
                    and (
                        not isinstance(metric_kind, str)
                        or not metric_kind.strip()
                    )
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3714",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' vereist een niet-lege "
                            "tekst voor 'metric-kind'"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "metric-kind",
                            obj.bronlocatie,
                        ),
                    ))
                elif (
                    isinstance(metric_kind, str)
                    and metric_kind != "*"
                    and metric_kind not in objectsoorten
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3715",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' telt onbekende "
                            f"objectsoort '{metric_kind}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "metric-kind",
                            obj.bronlocatie,
                        ),
                    ))
                metric_detail = obj.eigenschappen.get("metric-detail")
                if (
                    "metric-detail" in obj.eigenschappen
                    and (
                        metric_kind is None
                        or metric_detail not in {"kinds", "items"}
                    )
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3716",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' vereist voor "
                            "'metric-detail' de waarde 'kinds' of 'items' "
                            "naast 'metric-kind'"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "metric-detail",
                            obj.bronlocatie,
                        ),
                    ))
                navigatie = obj.eigenschappen.get("navigatie")
                if "homepagegebied" in obj.eigenschappen:
                    if homepagegebied not in homepagegebieden:
                        diagnostics.append(Diagnostic(
                            code="BP3722",
                            boodschap=(
                                f"Componentinstantie '{obj.id}' verwijst naar "
                                f"onbekend homepagegebied '{homepagegebied}'"
                            ),
                            locatie=obj.eigenschaplocaties.get(
                                "homepagegebied", obj.bronlocatie
                            ),
                        ))
                    if any(
                        veld in obj.eigenschappen
                        for veld in (
                            "naam",
                            "doel",
                            "metric-kind",
                            "metric-detail",
                            "informatiegebied",
                            "navigatie",
                        )
                    ):
                        diagnostics.append(Diagnostic(
                            code="BP3723",
                            boodschap=(
                                f"Componentinstantie '{obj.id}' combineert "
                                "'homepagegebied' met afgeleide inhoudsvelden"
                            ),
                            locatie=obj.eigenschaplocaties.get(
                                "homepagegebied", obj.bronlocatie
                            ),
                        ))
                if "navigatie" in obj.eigenschappen:
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
                            code="BP3719",
                            boodschap=(
                                f"Componentinstantie '{obj.id}' vereist een "
                                "niet-lege, unieke lijst 'navigatie'"
                            ),
                            locatie=obj.eigenschaplocaties.get(
                                "navigatie", obj.bronlocatie
                            ),
                        ))
                    else:
                        for doel_id in navigatie:
                            doel = context.symbolen.get(doel_id)
                            if doel is None:
                                diagnostics.append(Diagnostic(
                                    code="BP3720",
                                    boodschap=(
                                        f"Componentinstantie '{obj.id}' verwijst "
                                        f"naar onbekend navigatiedoel '{doel_id}'"
                                    ),
                                    locatie=obj.eigenschaplocaties.get(
                                        "navigatie", obj.bronlocatie
                                    ),
                                ))
                            elif doel.soort not in {"product", "renderdoel"}:
                                diagnostics.append(Diagnostic(
                                    code="BP3721",
                                    boodschap=(
                                        f"Navigatiedoel '{doel_id}' van "
                                        f"componentinstantie '{obj.id}' is geen "
                                        "product of renderdoel"
                                    ),
                                    locatie=obj.eigenschaplocaties.get(
                                        "navigatie", obj.bronlocatie
                                    ),
                                ))
        return tuple(diagnostics)
