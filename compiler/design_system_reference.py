"""Backend-onafhankelijk model voor native designsystem referentieproducten."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.component_accessibility import (
    ResolvedComponentAccessibility,
    resolveer_componenttoegankelijkheid,
)
from compiler.component_examples import (
    ResolvedComponentExample,
    resolveer_componentvoorbeelden,
)
from compiler.constraints import ConstraintContext
from compiler.design_components import (
    ComponentAppearance,
    DesignComponent,
    verzamel_appearances,
    verzamel_componenten,
)
from compiler.design_tokens import DesignToken, verzamel_tokens
from compiler.design_variants import (
    ResolvedComponentVariant,
    resolveer_varianten,
)
from compiler.diagnostics import Diagnostic


REFERENCE_SECTION_ROLES = (
    "primitieven",
    "tokens",
    "toestanden",
    "voorbeelden",
    "toegankelijkheid",
)
REFERENCE_SECTION_FIELDS = frozenset({"naam", "doel", "rol"})


@dataclass(frozen=True)
class ResolvedReferenceSection:
    id: str
    naam: str
    doel: str
    role: str


@dataclass(frozen=True)
class ResolvedDesignSystemReference:
    sections: tuple[ResolvedReferenceSection, ...]
    tokens: tuple[DesignToken, ...]
    appearances: tuple[ComponentAppearance, ...]
    components: tuple[DesignComponent, ...]
    variants: tuple[ResolvedComponentVariant, ...]
    examples: tuple[ResolvedComponentExample, ...]
    accessibility: tuple[ResolvedComponentAccessibility, ...]


class DesignSystemReferenceResolutionError(ValueError):
    """Niet gevalideerde CIR kan niet veilig tot referentie worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise DesignSystemReferenceResolutionError(
            f"Referentiesectie '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def resolveer_referentiesecties(
    objecten: Iterable[Architectuurobject],
    section_ids: Iterable[str],
) -> tuple[ResolvedReferenceSection, ...]:
    secties = {
        obj.id: obj for obj in objecten if obj.soort == "referentiesectie"
    }
    try:
        return tuple(
            ResolvedReferenceSection(
                id=secties[section_id].id,
                naam=_tekst(secties[section_id], "naam"),
                doel=_tekst(secties[section_id], "doel"),
                role=_tekst(secties[section_id], "rol"),
            )
            for section_id in section_ids
        )
    except KeyError as exc:
        raise DesignSystemReferenceResolutionError(
            f"Onbekende referentiesectie '{exc.args[0]}'"
        ) from exc


def resolveer_designsystemreferentie(
    objecten: Iterable[Architectuurobject],
    section_ids: Iterable[str],
) -> ResolvedDesignSystemReference:
    objecten = tuple(objecten)
    return ResolvedDesignSystemReference(
        sections=resolveer_referentiesecties(objecten, section_ids),
        tokens=verzamel_tokens(objecten),
        appearances=verzamel_appearances(objecten),
        components=verzamel_componenten(objecten),
        variants=resolveer_varianten(objecten),
        examples=resolveer_componentvoorbeelden(objecten),
        accessibility=resolveer_componenttoegankelijkheid(objecten),
    )


@dataclass(frozen=True)
class DesignSystemReferenceConstraint:
    """Valideer secties en volledige productdekking vóór backendselectie."""

    sleutel: str = "world-model.design-system-reference"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        secties = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "referentiesectie"
        }
        composities = {
            obj.id: obj for obj in context.objecten if obj.soort == "compositie"
        }

        for sectie in secties.values():
            for veld in sectie.eigenschappen:
                if veld not in REFERENCE_SECTION_FIELDS:
                    diagnostics.append(Diagnostic(
                        code="BP3840",
                        boodschap=(
                            f"Referentiesectie '{sectie.id}' heeft onbekende "
                            f"eigenschap '{veld}'"
                        ),
                        locatie=sectie.eigenschaplocaties.get(
                            veld, sectie.bronlocatie
                        ),
                    ))
            rol = sectie.eigenschappen.get("rol")
            if rol not in REFERENCE_SECTION_ROLES:
                diagnostics.append(Diagnostic(
                    code="BP3841",
                    boodschap=(
                        f"Referentiesectie '{sectie.id}' heeft onbekende rol "
                        f"'{rol}'"
                    ),
                    locatie=sectie.eigenschaplocaties.get(
                        "rol", sectie.bronlocatie
                    ),
                ))

        for product in (
            obj for obj in context.objecten if obj.soort == "product"
        ):
            inhoud = product.eigenschappen.get("inhoud", "composition")
            section_ids = product.eigenschappen.get("referentiesecties")
            if inhoud != "design-system":
                if section_ids is not None:
                    diagnostics.append(Diagnostic(
                        code="BP3845",
                        boodschap=(
                            f"Product '{product.id}' gebruikt "
                            "'referentiesecties' zonder inhoud 'design-system'"
                        ),
                        locatie=product.eigenschaplocaties.get(
                            "referentiesecties", product.bronlocatie
                        ),
                    ))
                continue

            geldig = (
                isinstance(section_ids, list)
                and bool(section_ids)
                and all(
                    isinstance(section_id, str) and section_id.strip()
                    for section_id in section_ids
                )
                and len(section_ids) == len(set(section_ids))
            )
            if not geldig:
                diagnostics.append(Diagnostic(
                    code="BP3842",
                    boodschap=(
                        f"Designsystemproduct '{product.id}' vereist een "
                        "niet lege, unieke lijst 'referentiesecties'"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "referentiesecties", product.bronlocatie
                    ),
                ))
                continue

            onbekend = [
                section_id
                for section_id in section_ids
                if section_id not in secties
            ]
            if onbekend:
                diagnostics.append(Diagnostic(
                    code="BP3842",
                    boodschap=(
                        f"Designsystemproduct '{product.id}' verwijst naar "
                        f"onbekende referentiesectie '{onbekend[0]}'"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "referentiesecties", product.bronlocatie
                    ),
                ))
                continue

            rollen = tuple(
                secties[section_id].eigenschappen.get("rol")
                for section_id in section_ids
            )
            if rollen != REFERENCE_SECTION_ROLES:
                diagnostics.append(Diagnostic(
                    code="BP3843",
                    boodschap=(
                        f"Designsystemproduct '{product.id}' vereist exact de "
                        "geordende rollen "
                        f"{', '.join(REFERENCE_SECTION_ROLES)}"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "referentiesecties", product.bronlocatie
                    ),
                ))

            if product.eigenschappen.get("mode", "interactive") != "static":
                diagnostics.append(Diagnostic(
                    code="BP3844",
                    boodschap=(
                        f"Designsystemproduct '{product.id}' moet een statische "
                        "architectuursnapshot zijn"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "mode", product.bronlocatie
                    ),
                ))

            compositie_id = product.eigenschappen.get("compositie")
            compositie = composities.get(compositie_id)
            instanties = (
                compositie.eigenschappen.get("instanties")
                if compositie is not None
                else None
            )
            if not isinstance(instanties, list) or len(instanties) != 1:
                diagnostics.append(Diagnostic(
                    code="BP3846",
                    boodschap=(
                        f"Designsystemproduct '{product.id}' vereist exact één "
                        "inhoudsinstantie in zijn compositie"
                    ),
                    locatie=product.eigenschaplocaties.get(
                        "compositie", product.bronlocatie
                    ),
                ))

        return tuple(diagnostics)
