"""Semantische constraints voor backendgestuurde producten."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from compiler.backend_discovery import backend_namen
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class ProductDefinitionConstraint:
    sleutel: str = "world-model.products"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        layouts = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "layout"
        }
        composities = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "compositie"
        }
        regions = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "region"
        }
        werelden = {obj.id for obj in context.objecten if obj.soort == "wereld"}
        heeft_themalaag = any(obj.soort == "thema" for obj in context.objecten)
        toegestane_backends = backend_namen()
        toegestane_velden = {
            "naam",
            "doel",
            "backend",
            "compositie",
            "layout",
            "pad",
            "mode",
            "wereld",
            "inhoud",
            "referentiesecties",
        }
        for obj in context.objecten:
            if obj.soort != "product":
                continue
            for naam in obj.eigenschappen:
                if naam not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP3501",
                        boodschap=f"Product '{obj.id}' heeft onbekende eigenschap '{naam}'",
                        locatie=obj.eigenschaplocaties.get(naam, obj.bronlocatie),
                    ))
            backend = obj.eigenschappen.get("backend")
            if backend not in toegestane_backends:
                diagnostics.append(Diagnostic(
                    code="BP3502",
                    boodschap=f"Product '{obj.id}' heeft onbekende backend '{backend}'",
                    locatie=obj.eigenschaplocaties.get("backend", obj.bronlocatie),
                ))
            layout = obj.eigenschappen.get("layout")
            if layout not in layouts:
                diagnostics.append(Diagnostic(
                    code="BP3503",
                    boodschap=f"Product '{obj.id}' verwijst naar onbekende layout '{layout}'",
                    locatie=obj.eigenschaplocaties.get("layout", obj.bronlocatie),
                ))
            compositie = obj.eigenschappen.get("compositie")
            if compositie not in composities:
                diagnostics.append(Diagnostic(
                    code="BP3506",
                    boodschap=(
                        f"Product '{obj.id}' verwijst naar onbekende of ontbrekende "
                        f"compositie '{compositie}'"
                    ),
                    locatie=obj.eigenschaplocaties.get("compositie", obj.bronlocatie),
                ))
            if layout in layouts and compositie in composities:
                layout_obj = layouts[layout]
                compositie_obj = composities[compositie]
                region_ids = layout_obj.eigenschappen.get("regions")
                composition_instances = compositie_obj.eigenschappen.get("instanties")
                kan_vergelijken = (
                    isinstance(region_ids, list)
                    and all(
                        isinstance(region_id, str) and region_id in regions
                        for region_id in region_ids
                    )
                    and isinstance(composition_instances, list)
                    and all(
                        isinstance(instance_id, str)
                        for instance_id in composition_instances
                    )
                )
                layout_instances = (
                    [
                        regions[region_id].eigenschappen.get("instantie")
                        for region_id in region_ids
                    ]
                    if kan_vergelijken
                    else []
                )
                kan_vergelijken = kan_vergelijken and all(
                    isinstance(instance_id, str)
                    for instance_id in layout_instances
                )
                if kan_vergelijken and (
                    set(layout_instances) != set(composition_instances)
                    or len(layout_instances) != len(composition_instances)
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3507",
                        boodschap=(
                            f"Product '{obj.id}' vereist exact dezelfde "
                            "componentinstanties in compositie en layout"
                        ),
                        locatie=obj.bronlocatie,
                    ))
            pad = obj.eigenschappen.get("pad")
            geldig_pad = isinstance(pad, str) and bool(pad.strip()) and not PurePosixPath(pad).is_absolute() and ".." not in PurePosixPath(pad).parts
            if not geldig_pad:
                diagnostics.append(Diagnostic(
                    code="BP3504",
                    boodschap=f"Product '{obj.id}' vereist een veilig relatief uitvoerpad",
                    locatie=obj.eigenschaplocaties.get("pad", obj.bronlocatie),
                ))
            wereld = obj.eigenschappen.get("wereld")
            if heeft_themalaag and wereld not in werelden:
                diagnostics.append(Diagnostic(
                    code="BP3505",
                    boodschap=f"Product '{obj.id}' verwijst naar onbekende of ontbrekende wereld '{wereld}'",
                    locatie=obj.eigenschaplocaties.get("wereld", obj.bronlocatie),
                ))
            mode = obj.eigenschappen.get("mode", "interactive")
            if mode not in {"interactive", "static"}:
                diagnostics.append(Diagnostic(
                    code="BP3508",
                    boodschap=f"Product '{obj.id}' heeft onbekende modus '{mode}'",
                    locatie=obj.eigenschaplocaties.get("mode", obj.bronlocatie),
                ))
            inhoud = obj.eigenschappen.get("inhoud", "composition")
            if inhoud not in {
                "composition",
                "project-status",
                "design-system",
            }:
                diagnostics.append(Diagnostic(
                    code="BP3509",
                    boodschap=f"Product '{obj.id}' heeft onbekende inhoud '{inhoud}'",
                    locatie=obj.eigenschaplocaties.get("inhoud", obj.bronlocatie),
                ))
        return tuple(diagnostics)
