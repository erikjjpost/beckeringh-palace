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
        layouts = {obj.id for obj in context.objecten if obj.soort == "layout"}
        werelden = {obj.id for obj in context.objecten if obj.soort == "wereld"}
        heeft_themalaag = any(obj.soort == "thema" for obj in context.objecten)
        toegestane_backends = backend_namen()
        toegestane_velden = {"naam", "doel", "backend", "layout", "pad", "wereld"}
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
        return tuple(diagnostics)