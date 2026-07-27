"""Semantische constraints voor native renderdoelen."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


def _veilig_relatief_pad(waarde: object) -> bool:
    if not isinstance(waarde, str) or not waarde.strip():
        return False
    pad = PurePosixPath(waarde)
    return not pad.is_absolute() and ".." not in pad.parts


@dataclass(frozen=True)
class RenderTargetConstraint:
    sleutel: str = "world-model.render-targets"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        renderdoelen = [
            obj for obj in context.objecten if obj.soort == "renderdoel"
        ]
        toegestane_velden = {"naam", "doel", "formaat", "pad"}
        paden: dict[str, str] = {}

        for renderdoel in renderdoelen:
            for naam in renderdoel.eigenschappen:
                if naam not in toegestane_velden:
                    diagnostics.append(Diagnostic(
                        code="BP3901",
                        boodschap=(
                            f"Renderdoel '{renderdoel.id}' heeft onbekende "
                            f"eigenschap '{naam}'"
                        ),
                        locatie=renderdoel.eigenschaplocaties.get(
                            naam, renderdoel.bronlocatie
                        ),
                    ))

            formaat = renderdoel.eigenschappen.get("formaat")
            if not isinstance(formaat, str) or not formaat.strip():
                diagnostics.append(Diagnostic(
                    code="BP3902",
                    boodschap=(
                        f"Renderdoel '{renderdoel.id}' vereist tekstveld 'formaat'"
                    ),
                    locatie=renderdoel.eigenschaplocaties.get(
                        "formaat", renderdoel.bronlocatie
                    ),
                ))

            pad = renderdoel.eigenschappen.get("pad")
            if not _veilig_relatief_pad(pad):
                diagnostics.append(Diagnostic(
                    code="BP3903",
                    boodschap=(
                        f"Renderdoel '{renderdoel.id}' vereist een veilig "
                        "relatief artifactpad"
                    ),
                    locatie=renderdoel.eigenschaplocaties.get(
                        "pad", renderdoel.bronlocatie
                    ),
                ))
            elif pad in paden:
                diagnostics.append(Diagnostic(
                    code="BP3904",
                    boodschap=(
                        f"Renderdoel '{renderdoel.id}' deelt artifactpad '{pad}' "
                        f"met renderdoel '{paden[pad]}'"
                    ),
                    locatie=renderdoel.eigenschaplocaties.get(
                        "pad", renderdoel.bronlocatie
                    ),
                ))
            else:
                paden[pad] = renderdoel.id

        return tuple(diagnostics)
