"""Native merkidentiteit voor Beckeringh Palace-producten."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


@dataclass(frozen=True)
class ResolvedBrandIdentity:
    id: str
    naam: str
    doel: str
    tagline: str
    promise: str
    principles: tuple[str, ...]
    products: tuple[str, ...]
    language: str
    voice: str


@dataclass(frozen=True)
class BrandIdentityConstraint:
    sleutel: str = "world-model.brand-identity"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        toegestane_velden = {
            "naam",
            "doel",
            "tagline",
            "belofte",
            "principes",
            "producten",
            "taal",
            "stem",
        }
        for merk in (obj for obj in context.objecten if obj.soort == "merk"):
            onbekend = set(merk.eigenschappen) - toegestane_velden
            for veld in sorted(onbekend):
                diagnostics.append(Diagnostic(
                    code="BP4201",
                    boodschap=(
                        f"Merk '{merk.id}' heeft onbekende eigenschap '{veld}'"
                    ),
                    locatie=merk.eigenschaplocaties.get(veld, merk.bronlocatie),
                ))

            for veld in ("tagline", "belofte", "taal", "stem"):
                waarde = merk.eigenschappen.get(veld)
                if not isinstance(waarde, str) or not waarde.strip():
                    diagnostics.append(Diagnostic(
                        code="BP4202",
                        boodschap=(
                            f"Merk '{merk.id}' vereist betekenisvol tekstveld "
                            f"'{veld}'"
                        ),
                        locatie=merk.eigenschaplocaties.get(
                            veld, merk.bronlocatie
                        ),
                    ))

            principes = merk.eigenschappen.get("principes")
            if (
                not isinstance(principes, list)
                or len(principes) != 3
                or any(
                    not isinstance(principe, str) or not principe.strip()
                    for principe in principes
                )
                or len(set(principes)) != len(principes)
            ):
                diagnostics.append(Diagnostic(
                    code="BP4203",
                    boodschap=(
                        f"Merk '{merk.id}' vereist precies drie unieke, "
                        "betekenisvolle principes"
                    ),
                    locatie=merk.eigenschaplocaties.get(
                        "principes", merk.bronlocatie
                    ),
                ))
            producten = merk.eigenschappen.get("producten")
            if (
                not isinstance(producten, list)
                or not producten
                or any(
                    not isinstance(product, str) or not product.strip()
                    for product in producten
                )
                or len(set(producten)) != len(producten)
            ):
                diagnostics.append(Diagnostic(
                    code="BP4204",
                    boodschap=(
                        f"Merk '{merk.id}' vereist een unieke, betekenisvolle "
                        "productfamilie"
                    ),
                    locatie=merk.eigenschaplocaties.get(
                        "producten", merk.bronlocatie
                    ),
                ))
        return tuple(diagnostics)


def resolveer_merkidentiteiten(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedBrandIdentity, ...]:
    merken = []
    for obj in objecten:
        if obj.soort != "merk":
            continue
        merken.append(ResolvedBrandIdentity(
            id=obj.id,
            naam=str(obj.eigenschappen["naam"]),
            doel=str(obj.eigenschappen["doel"]),
            tagline=str(obj.eigenschappen["tagline"]),
            promise=str(obj.eigenschappen["belofte"]),
            principles=tuple(str(item) for item in obj.eigenschappen["principes"]),
            products=tuple(str(item) for item in obj.eigenschappen["producten"]),
            language=str(obj.eigenschappen["taal"]),
            voice=str(obj.eigenschappen["stem"]),
        ))
    return tuple(sorted(merken, key=lambda merk: merk.id))
