"""Semantische regels voor expliciete ontwerpwerelden en theme-primitieven."""
from __future__ import annotations

from dataclasses import dataclass

from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.theme_resolution import (
    MATERIAAL_ROLLEN,
    RADIUS_ROLLEN,
    SHADOW_ROLLEN,
)


PRIMITIEF_SOORTEN = (
    "materiaal", "border", "radius", "shadow", "motion", "spacing",
    "typeschaal", "artdirection",
)
TYPOGRAFIE_ROLLEN = ("heading", "body", "mono")
TYPOGRAFIE_FALLBACKS = {
    "heading": "sans-serif",
    "body": "sans-serif",
    "mono": "monospace",
}
VERBODEN_FONTBRONDELEN = ("@import", "url(", "://")


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
            "typografie": {
                "naam", "doel", *TYPOGRAFIE_ROLLEN, "levering",
            },
            "typeschaal": {"naam", "doel", "display", "title", "heading", "body", "label", "caption"},
            "materiaal": {
                "naam", "doel", *MATERIAAL_ROLLEN,
            },
            "border": {"naam", "doel", "hairline", "regular", "strong", "style"},
            "radius": {"naam", "doel", *RADIUS_ROLLEN},
            "shadow": {
                "naam", "doel", *SHADOW_ROLLEN,
            },
            "motion": {
                "naam", "doel", "fast", "normal", "slow", "easing",
                "rest-offset", "hover-offset",
            },
            "spacing": {"naam", "doel", "none", "xs", "small", "medium", "large", "xl"},
            "artdirection": {
                "naam", "doel", "canvas", "interaction", "warm-accent",
                "warm-accent-limit", "glow", "ornament", "density", "imagery",
            },
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

        for typografie in objecten_per_soort["typografie"].values():
            levering = typografie.eigenschappen.get("levering")
            if levering != "local-only":
                diagnostics.append(Diagnostic(
                    code="BP3640",
                    boodschap=(
                        f"Typografie '{typografie.id}' vereist expliciete "
                        "levering 'local-only'"
                    ),
                    locatie=typografie.eigenschaplocaties.get(
                        "levering", typografie.bronlocatie
                    ),
                ))
            for rol in TYPOGRAFIE_ROLLEN:
                stack = typografie.eigenschappen.get(rol)
                if (
                    not isinstance(stack, list)
                    or not stack
                    or any(
                        not isinstance(familie, str) or not familie.strip()
                        for familie in stack
                    )
                    or len(stack) != len(set(stack))
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3641",
                        boodschap=(
                            f"Typografie '{typografie.id}' vereist voor '{rol}' "
                            "een niet-lege, unieke fontstack"
                        ),
                        locatie=typografie.eigenschaplocaties.get(
                            rol, typografie.bronlocatie
                        ),
                    ))
                    continue
                if any(
                    verboden in familie.lower()
                    for familie in stack
                    for verboden in VERBODEN_FONTBRONDELEN
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3642",
                        boodschap=(
                            f"Typografie '{typografie.id}' mag voor '{rol}' "
                            "geen externe fontbron bevatten"
                        ),
                        locatie=typografie.eigenschaplocaties.get(
                            rol, typografie.bronlocatie
                        ),
                    ))
                if stack[-1] != TYPOGRAFIE_FALLBACKS[rol]:
                    diagnostics.append(Diagnostic(
                        code="BP3643",
                        boodschap=(
                            f"Typografie '{typografie.id}' vereist voor '{rol}' "
                            f"generieke fallback '{TYPOGRAFIE_FALLBACKS[rol]}'"
                        ),
                        locatie=typografie.eigenschaplocaties.get(
                            rol, typografie.bronlocatie
                        ),
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

        artdirection_modes = {
            "glow": {"controlled", "none"},
            "ornament": {"technical-linework", "none"},
            "density": {"spacious", "compact"},
            "imagery": {"isometric-line-art", "none"},
        }
        for artdirection in objecten_per_soort["artdirection"].values():
            for veld, bronsoort, rollen in (
                ("canvas", "materiaal", {"canvas", "surface", "raised"}),
                ("interaction", "palet", {"primary", "secondary"}),
                ("warm-accent", "palet", {"accent"}),
            ):
                waarde = artdirection.eigenschappen.get(veld)
                if waarde not in rollen:
                    diagnostics.append(Diagnostic(
                        code="BP3630",
                        boodschap=(
                            f"Artdirection '{artdirection.id}' heeft voor '{veld}' "
                            f"onbekende {bronsoort}rol '{waarde}'"
                        ),
                        locatie=artdirection.eigenschaplocaties.get(
                            veld, artdirection.bronlocatie
                        ),
                    ))
            limiet = artdirection.eigenschappen.get("warm-accent-limit")
            if limiet not in {"1", "2"}:
                diagnostics.append(Diagnostic(
                    code="BP3631",
                    boodschap=(
                        f"Artdirection '{artdirection.id}' vereist een "
                        "warm-accent-limit van 1 of 2"
                    ),
                    locatie=artdirection.eigenschaplocaties.get(
                        "warm-accent-limit", artdirection.bronlocatie
                    ),
                ))
            for veld, toegestane_waarden in artdirection_modes.items():
                waarde = artdirection.eigenschappen.get(veld)
                if waarde not in toegestane_waarden:
                    diagnostics.append(Diagnostic(
                        code="BP3632",
                        boodschap=(
                            f"Artdirection '{artdirection.id}' heeft onbekende "
                            f"{veld}waarde '{waarde}'"
                        ),
                        locatie=artdirection.eigenschaplocaties.get(
                            veld, artdirection.bronlocatie
                        ),
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
            "typeschaal": ("typeschaal", "BP3614", False),
            "artdirection": ("artdirection", "BP3633", False),
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
            if (
                thema.eigenschappen.get("artdirection") is not None
                and thema.eigenschappen.get("materiaal") is None
            ):
                diagnostics.append(Diagnostic(
                    code="BP3634",
                    boodschap=(
                        f"Thema '{thema.id}' vereist materiaal wanneer "
                        "artdirection actief is"
                    ),
                    locatie=thema.eigenschaplocaties.get(
                        "artdirection", thema.bronlocatie
                    ),
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
