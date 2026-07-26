"""Semantische regels voor expliciete ontwerpwerelden en themafundamenten."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class ThemeFoundationConstraint:
    """Valideer kleur-, palet-, typografie-, thema- en wereldreferenties."""

    sleutel: str = "world-model.theme-foundation"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        objecten_per_soort = {
            soort: {obj.id: obj for obj in context.objecten if obj.soort == soort}
            for soort in ("kleur", "palet", "typografie", "thema", "wereld")
        }

        toegestane_velden = {
            "kleur": {"naam", "doel", "waarde"},
            "palet": {"naam", "doel", "primary", "secondary", "background", "surface", "foreground", "accent", "success", "warning", "error"},
            "typografie": {"naam", "doel", "heading", "body", "mono"},
            "thema": {"naam", "doel", "palet", "typografie"},
            "wereld": {"naam", "doel", "thema"},
        }

        for soort, objecten in objecten_per_soort.items():
            for obj in objecten.values():
                for veld in obj.eigenschappen:
                    if veld not in toegestane_velden[soort]:
                        diagnostics.append(Diagnostic(
                            code="BP3601",
                            boodschap=f"{soort.capitalize()} '{obj.id}' heeft onbekende eigenschap '{veld}'",
                            locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                        ))

        for kleur in objecten_per_soort["kleur"].values():
            waarde = kleur.eigenschappen.get("waarde")
            if not isinstance(waarde, str) or not waarde.startswith("#") or len(waarde) not in {4, 7, 9}:
                diagnostics.append(Diagnostic(
                    code="BP3602",
                    boodschap=f"Kleur '{kleur.id}' vereist een expliciete hexwaarde",
                    locatie=kleur.eigenschaplocaties.get("waarde", kleur.bronlocatie),
                ))

        kleuren = objecten_per_soort["kleur"]
        for palet in objecten_per_soort["palet"].values():
            rollen = toegestane_velden["palet"] - {"naam", "doel"}
            for rol in rollen:
                referentie = palet.eigenschappen.get(rol)
                if referentie is not None and referentie not in kleuren:
                    diagnostics.append(Diagnostic(
                        code="BP3603",
                        boodschap=f"Palet '{palet.id}' verwijst voor '{rol}' naar onbekende kleur '{referentie}'",
                        locatie=palet.eigenschaplocaties.get(rol, palet.bronlocatie),
                    ))

        paletten = objecten_per_soort["palet"]
        typografieen = objecten_per_soort["typografie"]
        for thema in objecten_per_soort["thema"].values():
            palet = thema.eigenschappen.get("palet")
            typografie = thema.eigenschappen.get("typografie")
            if palet not in paletten:
                diagnostics.append(Diagnostic(
                    code="BP3604",
                    boodschap=f"Thema '{thema.id}' verwijst naar onbekend palet '{palet}'",
                    locatie=thema.eigenschaplocaties.get("palet", thema.bronlocatie),
                ))
            if typografie not in typografieen:
                diagnostics.append(Diagnostic(
                    code="BP3605",
                    boodschap=f"Thema '{thema.id}' verwijst naar onbekende typografie '{typografie}'",
                    locatie=thema.eigenschaplocaties.get("typografie", thema.bronlocatie),
                ))

        themas = objecten_per_soort["thema"]
        for wereld in objecten_per_soort["wereld"].values():
            thema = wereld.eigenschappen.get("thema")
            if thema not in themas:
                diagnostics.append(Diagnostic(
                    code="BP3606",
                    boodschap=f"Wereld '{wereld.id}' verwijst naar onbekend thema '{thema}'",
                    locatie=wereld.eigenschaplocaties.get("thema", wereld.bronlocatie),
                ))

        return tuple(diagnostics)
