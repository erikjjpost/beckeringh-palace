"""Semantische regels voor expliciete ontwerpwerelden en theme-primitieven."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


PRIMITIEF_SOORTEN = ("materiaal", "border", "radius", "shadow", "motion", "spacing")


@dataclass(frozen=True)
class ThemeFoundationConstraint:
    """Valideer alle objecten en expliciete referenties van een thema."""

    sleutel: str = "world-model.theme-foundation"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        soorten = (
            "kleur", "palet", "typografie", *PRIMITIEF_SOORTEN, "thema", "wereld",
        )
        objecten_per_soort = {
            soort: {obj.id: obj for obj in context.objecten if obj.soort == soort}
            for soort in soorten
        }
        toegestane_velden = {
            "kleur": {"naam", "doel", "waarde"},
            "palet": {"naam", "doel", "primary", "secondary", "background", "surface", "foreground", "accent", "success", "warning", "error"},
            "typografie": {"naam", "doel", "heading", "body", "mono"},
            "materiaal": {"naam", "doel", "canvas", "surface", "raised", "foreground", "accent"},
            "border": {"naam", "doel", "hairline", "regular", "strong", "style"},
            "radius": {"naam", "doel", "small", "medium", "large", "pill"},
            "shadow": {"naam", "doel", "low", "medium", "high"},
            "motion": {"naam", "doel", "fast", "normal", "slow", "easing"},
            "spacing": {"naam", "doel", "none", "xs", "small", "medium", "large", "xl"},
            "thema": {"naam", "doel", "palet", "typografie", *PRIMITIEF_SOORTEN},
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

        kleuren = objecten_per_soort["kleur"]
        for kleur in kleuren.values():
            waarde = kleur.eigenschappen.get("waarde")
            if not isinstance(waarde, str) or not waarde.startswith("#") or len(waarde) not in {4, 7, 9}:
                diagnostics.append(Diagnostic(
                    code="BP3602",
                    boodschap=f"Kleur '{kleur.id}' vereist een expliciete hexwaarde",
                    locatie=kleur.eigenschaplocaties.get("waarde", kleur.bronlocatie),
                ))

        paletten = objecten_per_soort["palet"]
        for palet in paletten.values():
            for rol in toegestane_velden["palet"] - {"naam", "doel"}:
                referentie = palet.eigenschappen.get(rol)
                if referentie is not None and referentie not in kleuren:
                    diagnostics.append(Diagnostic(
                        code="BP3603",
                        boodschap=f"Palet '{palet.id}' verwijst voor '{rol}' naar onbekende kleur '{referentie}'",
                        locatie=palet.eigenschaplocaties.get(rol, palet.bronlocatie),
                    ))

        for materiaal in objecten_per_soort["materiaal"].values():
            for rol in toegestane_velden["materiaal"] - {"naam", "doel"}:
                referentie = materiaal.eigenschappen.get(rol)
                if referentie is not None and referentie not in kleuren:
                    diagnostics.append(Diagnostic(
                        code="BP3607",
                        boodschap=f"Materiaal '{materiaal.id}' verwijst voor '{rol}' naar onbekende kleur '{referentie}'",
                        locatie=materiaal.eigenschaplocaties.get(rol, materiaal.bronlocatie),
                    ))

        themas = objecten_per_soort["thema"]
        thema_referenties = {
            "palet": ("palet", "BP3604", True),
            "typografie": ("typografie", "BP3605", True),
            "materiaal": ("materiaal", "BP3608", False),
            "border": ("border", "BP3609", False),
            "radius": ("radius", "BP3610", False),
            "shadow": ("shadow", "BP3611", False),
            "motion": ("motion", "BP3612", False),
            "spacing": ("spacing", "BP3613", False),
        }
        for thema in themas.values():
            for veld, (soort, code, vereist) in thema_referenties.items():
                referentie = thema.eigenschappen.get(veld)
                if (vereist or referentie is not None) and referentie not in objecten_per_soort[soort]:
                    diagnostics.append(Diagnostic(
                        code=code,
                        boodschap=f"Thema '{thema.id}' verwijst naar onbekende {soort} '{referentie}'",
                        locatie=thema.eigenschaplocaties.get(veld, thema.bronlocatie),
                    ))

        foundation_actief = any(objecten_per_soort[soort] for soort in soorten[:-1])
        if foundation_actief:
            for wereld in objecten_per_soort["wereld"].values():
                thema = wereld.eigenschappen.get("thema")
                if thema not in themas:
                    diagnostics.append(Diagnostic(
                        code="BP3606",
                        boodschap=f"Wereld '{wereld.id}' verwijst naar onbekend thema '{thema}'",
                        locatie=wereld.eigenschaplocaties.get("thema", wereld.bronlocatie),
                    ))

        return tuple(diagnostics)
