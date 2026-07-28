"""Semantische constraints voor gecontroleerde componentvarianten."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.design_variants import COMPONENT_STATE_FIELDS
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class ComponentVariantConstraint:
    sleutel: str = "world-model.component-variants"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        componenten = {obj.id for obj in context.objecten if obj.soort == "component"}
        appearances = {obj.id for obj in context.objecten if obj.soort == "appearance"}
        varianten = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "variant"
        }

        for variant in varianten.values():
            for naam in variant.eigenschappen:
                if naam not in {
                    "naam",
                    "doel",
                    "component",
                    "appearance",
                    *COMPONENT_STATE_FIELDS,
                }:
                    diagnostics.append(Diagnostic(
                        code="BP3801",
                        boodschap=(
                            f"Variant '{variant.id}' heeft onbekende eigenschap '{naam}'"
                        ),
                        locatie=variant.eigenschaplocaties.get(naam, variant.bronlocatie),
                    ))
            component_id = variant.eigenschappen.get("component")
            if component_id not in componenten:
                diagnostics.append(Diagnostic(
                    code="BP3802",
                    boodschap=(
                        f"Variant '{variant.id}' verwijst naar onbekend component "
                        f"'{component_id}'"
                    ),
                    locatie=variant.eigenschaplocaties.get(
                        "component",
                        variant.bronlocatie,
                    ),
                ))
            appearance_id = variant.eigenschappen.get("appearance")
            if appearance_id not in appearances:
                diagnostics.append(Diagnostic(
                    code="BP3803",
                    boodschap=(
                        f"Variant '{variant.id}' verwijst naar onbekende appearance "
                        f"'{appearance_id}'"
                    ),
                    locatie=variant.eigenschaplocaties.get(
                        "appearance",
                        variant.bronlocatie,
                    ),
                ))
            aanwezige_states = tuple(
                state
                for state in COMPONENT_STATE_FIELDS
                if state in variant.eigenschappen
            )
            if (
                aanwezige_states
                and len(aanwezige_states) != len(COMPONENT_STATE_FIELDS)
            ):
                ontbrekende_states = tuple(
                    state
                    for state in COMPONENT_STATE_FIELDS
                    if state not in aanwezige_states
                )
                diagnostics.append(Diagnostic(
                    code="BP3806",
                    boodschap=(
                        f"Variant '{variant.id}' vereist een volledig "
                        "statecontract; ontbrekend: "
                        f"{', '.join(ontbrekende_states)}"
                    ),
                    locatie=variant.bronlocatie,
                ))
            for state in aanwezige_states:
                state_appearance = variant.eigenschappen.get(state)
                if state_appearance not in appearances:
                    diagnostics.append(Diagnostic(
                        code="BP3807",
                        boodschap=(
                            f"Variant '{variant.id}' verwijst voor state "
                            f"'{state}' naar onbekende appearance "
                            f"'{state_appearance}'"
                        ),
                        locatie=variant.eigenschaplocaties.get(
                            state,
                            variant.bronlocatie,
                        ),
                    ))

        for instantie in (
            obj
            for obj in context.objecten
            if obj.soort == "componentinstantie" and "variant" in obj.eigenschappen
        ):
            variant_id = instantie.eigenschappen.get("variant")
            variant = varianten.get(variant_id)
            if variant is None:
                diagnostics.append(Diagnostic(
                    code="BP3804",
                    boodschap=(
                        f"Componentinstantie '{instantie.id}' verwijst naar onbekende "
                        f"variant '{variant_id}'"
                    ),
                    locatie=instantie.eigenschaplocaties.get(
                        "variant",
                        instantie.bronlocatie,
                    ),
                ))
            elif variant.eigenschappen.get("component") != instantie.eigenschappen.get(
                "component"
            ):
                diagnostics.append(Diagnostic(
                    code="BP3805",
                    boodschap=(
                        f"Variant '{variant_id}' hoort niet bij component "
                        f"'{instantie.eigenschappen.get('component')}' van "
                        f"componentinstantie '{instantie.id}'"
                    ),
                    locatie=instantie.eigenschaplocaties.get(
                        "variant",
                        instantie.bronlocatie,
                    ),
                ))

        return tuple(diagnostics)
