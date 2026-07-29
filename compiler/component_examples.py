"""Getypeerde, backend-onafhankelijke voorbeelden voor componentcatalogi."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.component_accessibility import (
    ResolvedComponentAccessibility,
    resolveer_componenttoegankelijkheid,
)
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
    "invoertype",
    "actietype",
    "venstertitel",
    "vensterknoppen",
    "tabs",
    "actieve-tab",
    "markering",
    "gebruiker",
    "host",
    "sleutels",
    "waarden",
    "pad",
    "prompt",
    "cursor",
})
COMPONENTVOORBEELD_INHOUD = frozenset({
    "label",
    "waarde",
    "beschrijving",
    "melding",
    "status",
    "venstertitel",
    "vensterknoppen",
    "tabs",
    "actieve-tab",
    "markering",
    "gebruiker",
    "host",
    "sleutels",
    "waarden",
    "pad",
    "prompt",
    "cursor",
})
VERPLICHTE_INHOUD_PER_ROL = {
    "actie": frozenset({"label"}),
    "invoer": frozenset({"label", "waarde"}),
    "status": frozenset({"label", "waarde"}),
    "app-tegel": frozenset({"label", "beschrijving", "status"}),
    "statistiek": frozenset({"label", "waarde"}),
    "terminal": frozenset({"label"}),
}
TOEGESTANE_INHOUD_PER_ROL = {
    "actie": frozenset({"label"}),
    "invoer": frozenset({"label", "waarde", "melding"}),
    "status": frozenset({"label", "waarde"}),
    "app-tegel": frozenset({"label", "beschrijving", "status"}),
    "statistiek": frozenset({"label", "waarde", "beschrijving"}),
    "terminal": frozenset({
        "label",
        "venstertitel",
        "vensterknoppen",
        "tabs",
        "actieve-tab",
        "markering",
        "gebruiker",
        "host",
        "sleutels",
        "waarden",
        "pad",
        "prompt",
        "cursor",
    }),
}
APP_STATUSSEN = frozenset({"running", "pending", "failed"})
TERMINALVENSTERKNOPPEN = ("sluiten", "minimaliseren", "maximaliseren")
TERMINAL_TEKSTVELDEN = (
    "venstertitel",
    "actieve-tab",
    "markering",
    "gebruiker",
    "host",
    "pad",
    "prompt",
    "cursor",
)
TERMINAL_LIJSTVELDEN = ("vensterknoppen", "tabs", "sleutels", "waarden")


@dataclass(frozen=True)
class ResolvedTerminalContent:
    venstertitel: str
    vensterknoppen: tuple[str, ...]
    tabs: tuple[str, ...]
    actieve_tab: str
    markering: str
    gebruiker: str
    host: str
    systeemvelden: tuple[tuple[str, str], ...]
    pad: str
    prompt: str
    cursor: str


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
    invoertype: str | None
    actietype: str | None
    terminal: ResolvedTerminalContent | None
    accessibility: ResolvedComponentAccessibility | None


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


def _tekstreeks(
    obj: Architectuurobject,
    veld: str,
) -> tuple[str, ...]:
    waarde = obj.eigenschappen.get(veld)
    if (
        not isinstance(waarde, list)
        or not waarde
        or any(
            not isinstance(item, str) or not item.strip()
            for item in waarde
        )
    ):
        raise ComponentExampleResolutionError(
            f"Componentvoorbeeld '{obj.id}' vereist tekstreeks '{veld}'"
        )
    return tuple(waarde)


def _terminalinhoud(
    obj: Architectuurobject,
    rol: str,
) -> ResolvedTerminalContent | None:
    if rol != "terminal":
        return None
    sleutels = _tekstreeks(obj, "sleutels")
    waarden = _tekstreeks(obj, "waarden")
    return ResolvedTerminalContent(
        venstertitel=_tekst(obj, "venstertitel"),
        vensterknoppen=_tekstreeks(obj, "vensterknoppen"),
        tabs=_tekstreeks(obj, "tabs"),
        actieve_tab=_tekst(obj, "actieve-tab"),
        markering=_tekst(obj, "markering"),
        gebruiker=_tekst(obj, "gebruiker"),
        host=_tekst(obj, "host"),
        systeemvelden=tuple(zip(sleutels, waarden, strict=True)),
        pad=_tekst(obj, "pad"),
        prompt=_tekst(obj, "prompt"),
        cursor=_tekst(obj, "cursor"),
    )


def resolveer_componentvoorbeelden(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedComponentExample, ...]:
    objecten = tuple(objecten)
    componenten = {
        obj.id: obj for obj in objecten if obj.soort == "component"
    }
    toegankelijkheid = {
        contract.component_id: contract
        for contract in resolveer_componenttoegankelijkheid(objecten)
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
            invoertype=_optionele_tekst(obj, "invoertype"),
            actietype=_optionele_tekst(obj, "actietype"),
            terminal=_terminalinhoud(obj, str(rol)),
            accessibility=toegankelijkheid.get(component.id),
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
            invoertype = voorbeeld.eigenschappen.get("invoertype")
            if invoertype is not None and (
                rol != "invoer" or invoertype not in {"text", "email", "password"}
            ):
                diagnostics.append(Diagnostic(
                    code="BP3827",
                    boodschap=(
                        f"Componentvoorbeeld '{voorbeeld.id}' heeft voor rol "
                        f"'{rol}' onbekend invoertype '{invoertype}'"
                    ),
                    locatie=voorbeeld.eigenschaplocaties.get(
                        "invoertype", voorbeeld.bronlocatie
                    ),
                ))
            actietype = voorbeeld.eigenschappen.get("actietype")
            if actietype is not None and (
                rol != "actie" or actietype not in {"button", "submit"}
            ):
                diagnostics.append(Diagnostic(
                    code="BP3828",
                    boodschap=(
                        f"Componentvoorbeeld '{voorbeeld.id}' heeft voor rol "
                        f"'{rol}' onbekend actietype '{actietype}'"
                    ),
                    locatie=voorbeeld.eigenschaplocaties.get(
                        "actietype", voorbeeld.bronlocatie
                    ),
                ))
            if rol == "terminal":
                for veld in TERMINAL_TEKSTVELDEN:
                    waarde = voorbeeld.eigenschappen.get(veld)
                    if not isinstance(waarde, str) or not waarde.strip():
                        diagnostics.append(Diagnostic(
                            code="BP3829",
                            boodschap=(
                                f"Terminalvoorbeeld '{voorbeeld.id}' vereist "
                                f"tekstveld '{veld}'"
                            ),
                            locatie=voorbeeld.eigenschaplocaties.get(
                                veld, voorbeeld.bronlocatie
                            ),
                        ))
                lijsten: dict[str, list[str]] = {}
                for veld in TERMINAL_LIJSTVELDEN:
                    waarde = voorbeeld.eigenschappen.get(veld)
                    geldig = (
                        isinstance(waarde, list)
                        and bool(waarde)
                        and all(
                            isinstance(item, str) and bool(item.strip())
                            for item in waarde
                        )
                    )
                    if not geldig:
                        diagnostics.append(Diagnostic(
                            code="BP3829",
                            boodschap=(
                                f"Terminalvoorbeeld '{voorbeeld.id}' vereist "
                                f"niet-lege tekstreeks '{veld}'"
                            ),
                            locatie=voorbeeld.eigenschaplocaties.get(
                                veld, voorbeeld.bronlocatie
                            ),
                        ))
                    else:
                        lijsten[veld] = waarde
                vensterknoppen = lijsten.get("vensterknoppen")
                if (
                    vensterknoppen is not None
                    and tuple(vensterknoppen) != TERMINALVENSTERKNOPPEN
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3829",
                        boodschap=(
                            f"Terminalvoorbeeld '{voorbeeld.id}' vereist "
                            "sluiten, minimaliseren en maximaliseren als "
                            "geordende vensterknoppen"
                        ),
                        locatie=voorbeeld.eigenschaplocaties.get(
                            "vensterknoppen", voorbeeld.bronlocatie
                        ),
                    ))
                tabs = lijsten.get("tabs")
                actieve_tab = voorbeeld.eigenschappen.get("actieve-tab")
                if (
                    tabs is not None
                    and (
                        len(tabs) != len(set(tabs))
                        or actieve_tab not in tabs
                    )
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3829",
                        boodschap=(
                            f"Terminalvoorbeeld '{voorbeeld.id}' vereist "
                            "unieke tabs en één bestaande actieve tab"
                        ),
                        locatie=voorbeeld.eigenschaplocaties.get(
                            "tabs", voorbeeld.bronlocatie
                        ),
                    ))
                sleutels = lijsten.get("sleutels")
                waarden = lijsten.get("waarden")
                if (
                    sleutels is not None
                    and waarden is not None
                    and (
                        len(sleutels) != len(waarden)
                        or len(sleutels) != len(set(sleutels))
                    )
                ):
                    diagnostics.append(Diagnostic(
                        code="BP3829",
                        boodschap=(
                            f"Terminalvoorbeeld '{voorbeeld.id}' vereist "
                            "evenveel unieke sleutels als waarden"
                        ),
                        locatie=voorbeeld.eigenschaplocaties.get(
                            "sleutels", voorbeeld.bronlocatie
                        ),
                    ))
        return tuple(diagnostics)
