"""Semantische constraints voor gecontroleerde componentvarianten."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
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
                if naam not in {"naam", "doel", "component", "appearance"}:
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
