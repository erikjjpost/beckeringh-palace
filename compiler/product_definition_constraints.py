"""Semantische constraints voor backendgestuurde producten."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic

TOEGESTANE_BACKENDS = frozenset({"html"})


@dataclass(frozen=True)
class ProductDefinitionConstraint:
    sleutel: str = "world-model.products"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        layouts = {obj.id for obj in context.objecten if obj.soort == "layout"}
        toegestane_velden = {"naam", "doel", "backend", "layout", "pad"}
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
            if backend not in TOEGESTANE_BACKENDS:
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
        return tuple(diagnostics)
