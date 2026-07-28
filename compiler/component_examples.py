"""Getypeerde, backend-onafhankelijke voorbeelden voor componentcatalogi."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.design_components import COMPONENT_ROLLEN
from compiler.diagnostics import Diagnostic


COMPONENTVOORBEELD_VELDEN = frozenset({
    "naam",
    "doel",
    "component",
    "variant",
    "label",
    "waarde",
    "beschrijving",
    "melding",
    "status",
})
COMPONENTVOORBEELD_INHOUD = frozenset({
    "label",
    "waarde",
    "beschrijving",
    "melding",
    "status",
})
VERPLICHTE_INHOUD_PER_ROL = {
    "actie": frozenset({"label"}),
    "invoer": frozenset({"label", "waarde"}),
    "status": frozenset({"label", "waarde"}),
    "app-tegel": frozenset({"label", "beschrijving", "status"}),
    "statistiek": frozenset({"label", "waarde"}),
}
TOEGESTANE_INHOUD_PER_ROL = {
    "actie": frozenset({"label"}),
    "invoer": frozenset({"label", "waarde", "melding"}),
    "status": frozenset({"label", "waarde"}),
    "app-tegel": frozenset({"label", "beschrijving", "status"}),
    "statistiek": frozenset({"label", "waarde", "beschrijving"}),
}
APP_STATUSSEN = frozenset({"running", "pending", "failed"})


@dataclass(frozen=True)
class ResolvedComponentExample:
    id: str
    naam: str
    doel: str
    component_id: str
    component_role: str
    component_anatomy: tuple[str, ...]
    variant_id: str
    label: str
    waarde: str | None
    beschrijving: str | None
    melding: str | None
    status: str | None


class ComponentExampleResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot componentvoorbeelden worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise ComponentExampleResolutionError(
            f"Componentvoorbeeld '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _optionele_tekst(
    obj: Architectuurobject,
    veld: str,
) -> str | None:
    if veld not in obj.eigenschappen:
        return None
    return _tekst(obj, veld)


def resolveer_componentvoorbeelden(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedComponentExample, ...]:
    objecten = tuple(objecten)
    componenten = {
        obj.id: obj for obj in objecten if obj.soort == "component"
    }
    voorbeelden = []
    for obj in objecten:
        if obj.soort != "componentvoorbeeld":
            continue
        component = componenten[_tekst(obj, "component")]
        rol = component.eigenschappen["rol"]
        anatomie = component.eigenschappen["anatomie"]
        assert isinstance(rol, str)
        assert isinstance(anatomie, list)
        voorbeelden.append(ResolvedComponentExample(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            component_id=component.id,
            component_role=rol,
            component_anatomy=tuple(str(item) for item in anatomie),
            variant_id=_tekst(obj, "variant"),
            label=_tekst(obj, "label"),
            waarde=_optionele_tekst(obj, "waarde"),
            beschrijving=_optionele_tekst(obj, "beschrijving"),
            melding=_optionele_tekst(obj, "melding"),
            status=_optionele_tekst(obj, "status"),
        ))
    return tuple(sorted(voorbeelden, key=lambda item: item.id))


@dataclass(frozen=True)
class ComponentExampleConstraint:
    """Valideer voorbeelden tegen componentrol, anatomie en variant."""

    sleutel: str = "world-model.component-examples"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        componenten = {
            obj.id: obj for obj in context.objecten if obj.soort == "component"
        }
        varianten = {
            obj.id: obj for obj in context.objecten if obj.soort == "variant"
        }
        for voorbeeld in (
            obj
            for obj in context.objecten
            if obj.soort == "componentvoorbeeld"
        ):
            for veld in voorbeeld.eigenschappen:
                if veld not in COMPONENTVOORBEELD_VELDEN:
                    diagnostics.append(Diagnostic(
                        code="BP3820",
                        boodschap=(
                            f"Componentvoorbeeld '{voorbeeld.id}' heeft "
                            f"onbekende eigenschap '{veld}'"
                        ),
                        locatie=voorbeeld.eigenschaplocaties.get(
                            veld, voorbeeld.bronlocatie
                        ),
                    ))
            component_id = voorbeeld.eigenschappen.get("component")
            component = componenten.get(component_id)
            if component is None:
                diagnostics.append(Diagnostic(
                    code="BP3821",
                    boodschap=(
                        f"Componentvoorbeeld '{voorbeeld.id}' verwijst naar "
                        f"onbekend component '{component_id}'"
                    ),
                    locatie=voorbeeld.eigenschaplocaties.get(
                        "component", voorbeeld.bronlocatie
                    ),
                ))
                continue
            rol = component.eigenschappen.get("rol")
            if rol not in COMPONENT_ROLLEN:
                diagnostics.append(Diagnostic(
                    code="BP3824",
                    boodschap=(
                        f"Componentvoorbeeld '{voorbeeld.id}' vereist een "
                        f"component met expliciete rol"
                    ),
                    locatie=voorbeeld.eigenschaplocaties.get(
                        "component", voorbeeld.bronlocatie
                    ),
                ))
                continue
            variant_id = voorbeeld.eigenschappen.get("variant")
            variant = varianten.get(variant_id)
            if variant is None:
                diagnostics.append(Diagnostic(
                    code="BP3822",
                    boodschap=(
                        f"Componentvoorbeeld '{voorbeeld.id}' verwijst naar "
                        f"onbekende variant '{variant_id}'"
                    ),
                    locatie=voorbeeld.eigenschaplocaties.get(
                        "variant", voorbeeld.bronlocatie
                    ),
                ))
            elif variant.eigenschappen.get("component") != component_id:
                diagnostics.append(Diagnostic(
                    code="BP3823",
                    boodschap=(
                        f"Variant '{variant_id}' hoort niet bij component "
                        f"'{component_id}' van componentvoorbeeld "
                        f"'{voorbeeld.id}'"
                    ),
                    locatie=voorbeeld.eigenschaplocaties.get(
                        "variant", voorbeeld.bronlocatie
                    ),
                ))
            aanwezige_inhoud = {
                veld
                for veld in COMPONENTVOORBEELD_INHOUD
                if veld in voorbeeld.eigenschappen
            }
            toegestaan = TOEGESTANE_INHOUD_PER_ROL.get(str(rol), frozenset())
            onverwacht = aanwezige_inhoud - toegestaan
            if onverwacht:
                diagnostics.append(Diagnostic(
                    code="BP3825",
                    boodschap=(
                        f"Componentvoorbeeld '{voorbeeld.id}' bevat voor rol "
                        f"'{rol}' onverwachte inhoud: "
                        f"{', '.join(sorted(onverwacht))}"
                    ),
                    locatie=voorbeeld.bronlocatie,
                ))
            verplicht = VERPLICHTE_INHOUD_PER_ROL.get(str(rol), frozenset())
            for veld in sorted(verplicht):
                waarde = voorbeeld.eigenschappen.get(veld)
                if not isinstance(waarde, str) or not waarde.strip():
                    diagnostics.append(Diagnostic(
                        code="BP3824",
                        boodschap=(
                            f"Componentvoorbeeld '{voorbeeld.id}' vereist voor "
                            f"rol '{rol}' tekstveld '{veld}'"
                        ),
                        locatie=voorbeeld.eigenschaplocaties.get(
                            veld, voorbeeld.bronlocatie
                        ),
                    ))
            status = voorbeeld.eigenschappen.get("status")
            if rol == "app-tegel" and status not in APP_STATUSSEN:
                diagnostics.append(Diagnostic(
                    code="BP3826",
                    boodschap=(
                        f"Componentvoorbeeld '{voorbeeld.id}' heeft onbekende "
                        f"appstatus '{status}'"
                    ),
                    locatie=voorbeeld.eigenschaplocaties.get(
                        "status", voorbeeld.bronlocatie
                    ),
                ))
        return tuple(diagnostics)
