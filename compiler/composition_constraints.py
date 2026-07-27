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

        for obj in context.objecten:
            if obj.soort == "compositie":
                toegestane_velden = {"naam", "doel", "instanties"}
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
                else:
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
                if component_id not in componenten:
                    diagnostics.append(Diagnostic(
                        code="BP3713",
                        boodschap=(
                            f"Componentinstantie '{obj.id}' verwijst naar onbekend "
                            f"component '{component_id}'"
                        ),
                        locatie=obj.eigenschaplocaties.get("component", obj.bronlocatie),
                    ))
                metric_kind = obj.eigenschappen.get("metric-kind")
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
        return tuple(diagnostics)
