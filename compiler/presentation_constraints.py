"""Semantische constraints voor native Beckeringh Palace-presentaties."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.presentations import DiaFormaat
from compiler.product_definition_constraints import _instanties_komen_niet_overeen


PRESENTATION_FIELDS = frozenset({"naam", "doel", "dias"})
DIA_FIELDS = frozenset({
    "naam", "doel", "presentatie", "compositie", "layout", "formaat",
})


def _geldige_geordende_lijst(waarde: object) -> bool:
    return (
        isinstance(waarde, list)
        and bool(waarde)
        and all(isinstance(item, str) and bool(item.strip()) for item in waarde)
        and len(waarde) == len(set(waarde))
    )


@dataclass(frozen=True)
class PresentationConstraint:
    """Valideer presentatie/dia-wederkerigheid en gedeeld compositie/layoutgebruik."""

    sleutel: str = "world-model.presentations"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        presentaties = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "presentatie"
        }
        dias = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "dia"
        }
        composities = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "compositie"
        }
        layouts = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "layout"
        }
        regions = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "region"
        }

        for presentatie in presentaties.values():
            for veld in presentatie.eigenschappen:
                if veld not in PRESENTATION_FIELDS:
                    diagnostics.append(Diagnostic(
                        code="BP4420",
                        boodschap=(
                            f"Presentatie '{presentatie.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=presentatie.eigenschaplocaties.get(
                            veld, presentatie.bronlocatie
                        ),
                    ))

            dia_ids = presentatie.eigenschappen.get("dias")
            if not _geldige_geordende_lijst(dia_ids):
                diagnostics.append(Diagnostic(
                    code="BP4421",
                    boodschap=(
                        f"Presentatie '{presentatie.id}' vereist een "
                        "niet-lege, unieke en geordende lijst 'dias'"
                    ),
                    locatie=presentatie.eigenschaplocaties.get(
                        "dias", presentatie.bronlocatie
                    ),
                ))
                continue

            onbekende_dias = [
                dia_id for dia_id in dia_ids if dia_id not in dias
            ]
            if onbekende_dias:
                diagnostics.append(Diagnostic(
                    code="BP4422",
                    boodschap=(
                        f"Presentatie '{presentatie.id}' verwijst naar "
                        f"onbekende dia '{onbekende_dias[0]}'"
                    ),
                    locatie=presentatie.eigenschaplocaties.get(
                        "dias", presentatie.bronlocatie
                    ),
                ))

            verwezen_dias = {
                dia.id
                for dia in dias.values()
                if dia.eigenschappen.get("presentatie") == presentatie.id
            }
            if (
                onbekende_dias
                or verwezen_dias != set(dia_ids)
                or any(
                    dias[dia_id].eigenschappen.get("presentatie")
                    != presentatie.id
                    for dia_id in dia_ids
                    if dia_id in dias
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP4423",
                    boodschap=(
                        f"Presentatie '{presentatie.id}' vereist een exact "
                        "wederkerige dialijst"
                    ),
                    locatie=presentatie.eigenschaplocaties.get(
                        "dias", presentatie.bronlocatie
                    ),
                ))

        for dia in dias.values():
            for veld in dia.eigenschappen:
                if veld not in DIA_FIELDS:
                    diagnostics.append(Diagnostic(
                        code="BP4430",
                        boodschap=(
                            f"Dia '{dia.id}' heeft onbekende eigenschap "
                            f"'{veld}'"
                        ),
                        locatie=dia.eigenschaplocaties.get(
                            veld, dia.bronlocatie
                        ),
                    ))

            presentatie_id = dia.eigenschappen.get("presentatie")
            if presentatie_id not in presentaties:
                diagnostics.append(Diagnostic(
                    code="BP4431",
                    boodschap=(
                        f"Dia '{dia.id}' verwijst naar onbekende presentatie "
                        f"'{presentatie_id}'"
                    ),
                    locatie=dia.eigenschaplocaties.get(
                        "presentatie", dia.bronlocatie
                    ),
                ))

            compositie_id = dia.eigenschappen.get("compositie")
            compositie = composities.get(compositie_id)
            if compositie is None:
                diagnostics.append(Diagnostic(
                    code="BP4432",
                    boodschap=(
                        f"Dia '{dia.id}' verwijst naar onbekende compositie "
                        f"'{compositie_id}'"
                    ),
                    locatie=dia.eigenschaplocaties.get(
                        "compositie", dia.bronlocatie
                    ),
                ))

            layout_id = dia.eigenschappen.get("layout")
            layout = layouts.get(layout_id)
            if layout is None:
                diagnostics.append(Diagnostic(
                    code="BP4433",
                    boodschap=(
                        f"Dia '{dia.id}' verwijst naar onbekende layout "
                        f"'{layout_id}'"
                    ),
                    locatie=dia.eigenschaplocaties.get(
                        "layout", dia.bronlocatie
                    ),
                ))

            if (
                compositie is not None
                and layout is not None
                and _instanties_komen_niet_overeen(compositie, layout, regions)
            ):
                diagnostics.append(Diagnostic(
                    code="BP4434",
                    boodschap=(
                        f"Dia '{dia.id}' vereist exact dezelfde "
                        "componentinstanties in compositie en layout"
                    ),
                    locatie=dia.bronlocatie,
                ))

            formaat_waarde = dia.eigenschappen.get("formaat")
            try:
                DiaFormaat(str(formaat_waarde))
            except ValueError:
                diagnostics.append(Diagnostic(
                    code="BP4435",
                    boodschap=(
                        f"Dia '{dia.id}' heeft onbekend formaat "
                        f"'{formaat_waarde}'"
                    ),
                    locatie=dia.eigenschaplocaties.get(
                        "formaat", dia.bronlocatie
                    ),
                ))

        return tuple(diagnostics)
