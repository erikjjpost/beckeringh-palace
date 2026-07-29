"""Backend-onafhankelijke toegankelijkheidscontracten voor componenten."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic


TOEGANKELIJKHEIDSVELDEN = frozenset({
    "naam",
    "doel",
    "rol",
    "naambron",
    "waardebron",
    "foutbron",
    "disabled",
    "focus",
    "toetsenbord",
})
TOEGANKELIJKHEIDSROLLEN = frozenset({
    "actie",
    "groep",
    "status",
    "tekstinvoer",
})
DISABLED_GEDRAGINGEN = frozenset({
    "native",
    "niet-van-toepassing",
})
FOCUSGEDRAGINGEN = frozenset({
    "geen",
    "tabvolgorde",
})
TOETSENBORDGEDRAGINGEN = frozenset({
    "activeren",
    "geen",
    "tekstinvoer",
})
TOETSEN_PER_GEDRAG = {
    "activeren": ("Enter", "Space"),
    "geen": (),
    "tekstinvoer": (),
}

# Exact één contractvorm per native componentrol voorkomt rendererafleiding.
VERWACHT_CONTRACT_PER_COMPONENTROL = {
    "paneel": {
        "rol": "groep",
        "naambron": "titel",
        "waardebron": None,
        "foutbron": None,
        "disabled": "niet-van-toepassing",
        "focus": "geen",
        "toetsenbord": "geen",
    },
    "actie": {
        "rol": "actie",
        "naambron": "label",
        "waardebron": None,
        "foutbron": None,
        "disabled": "native",
        "focus": "tabvolgorde",
        "toetsenbord": "activeren",
    },
    "invoer": {
        "rol": "tekstinvoer",
        "naambron": "label",
        "waardebron": "waarde",
        "foutbron": "melding",
        "disabled": "native",
        "focus": "tabvolgorde",
        "toetsenbord": "tekstinvoer",
    },
    "status": {
        "rol": "status",
        "naambron": "label",
        "waardebron": "waarde",
        "foutbron": None,
        "disabled": "niet-van-toepassing",
        "focus": "geen",
        "toetsenbord": "geen",
    },
    "app-tegel": {
        "rol": "actie",
        "naambron": "label",
        "waardebron": "status",
        "foutbron": None,
        "disabled": "native",
        "focus": "tabvolgorde",
        "toetsenbord": "activeren",
    },
    "statistiek": {
        "rol": "groep",
        "naambron": "label",
        "waardebron": "waarde",
        "foutbron": None,
        "disabled": "niet-van-toepassing",
        "focus": "geen",
        "toetsenbord": "geen",
    },
}


@dataclass(frozen=True)
class ResolvedComponentAccessibility:
    component_id: str
    contract_id: str
    naam: str
    doel: str
    rol: str
    naambron: str
    waardebron: str | None
    foutbron: str | None
    disabled_gedrag: str
    focusgedrag: str
    toetsenbordgedrag: str
    toetsen: tuple[str, ...]
    bron: Architectuurobject


class ComponentAccessibilityResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet veilig worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise ComponentAccessibilityResolutionError(
            f"Toegankelijkheid '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _optionele_tekst(
    obj: Architectuurobject,
    veld: str,
) -> str | None:
    if veld not in obj.eigenschappen:
        return None
    return _tekst(obj, veld)


def resolveer_componenttoegankelijkheid(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedComponentAccessibility, ...]:
    """Los gevalideerde componentreferenties op naar getypeerde contracten."""

    objecten = tuple(objecten)
    contracten = {
        obj.id: obj for obj in objecten if obj.soort == "toegankelijkheid"
    }
    opgelost = []
    for component in objecten:
        if component.soort != "component":
            continue
        contract_id = component.eigenschappen.get("toegankelijkheid")
        if not isinstance(contract_id, str):
            continue
        try:
            contract = contracten[contract_id]
        except KeyError as exc:
            raise ComponentAccessibilityResolutionError(
                f"Component '{component.id}' verwijst naar onbekende "
                f"toegankelijkheid '{contract_id}'"
            ) from exc
        toetsenbordgedrag = _tekst(contract, "toetsenbord")
        opgelost.append(ResolvedComponentAccessibility(
            component_id=component.id,
            contract_id=contract.id,
            naam=_tekst(contract, "naam"),
            doel=_tekst(contract, "doel"),
            rol=_tekst(contract, "rol"),
            naambron=_tekst(contract, "naambron"),
            waardebron=_optionele_tekst(contract, "waardebron"),
            foutbron=_optionele_tekst(contract, "foutbron"),
            disabled_gedrag=_tekst(contract, "disabled"),
            focusgedrag=_tekst(contract, "focus"),
            toetsenbordgedrag=toetsenbordgedrag,
            toetsen=TOETSEN_PER_GEDRAG[toetsenbordgedrag],
            bron=contract,
        ))
    return tuple(sorted(opgelost, key=lambda item: item.component_id))


@dataclass(frozen=True)
class ComponentAccessibilityConstraint:
    """Valideer toegankelijkheid tegen componentrol en anatomie."""

    sleutel: str = "world-model.component-accessibility"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        contracten = {
            obj.id: obj
            for obj in context.objecten
            if obj.soort == "toegankelijkheid"
        }
        for contract in contracten.values():
            for veld in contract.eigenschappen:
                if veld not in TOEGANKELIJKHEIDSVELDEN:
                    diagnostics.append(Diagnostic(
                        code="BP3830",
                        boodschap=(
                            f"Toegankelijkheid '{contract.id}' heeft "
                            f"onbekende eigenschap '{veld}'"
                        ),
                        locatie=contract.eigenschaplocaties.get(
                            veld, contract.bronlocatie
                        ),
                    ))
            waarden = {
                "rol": TOEGANKELIJKHEIDSROLLEN,
                "disabled": DISABLED_GEDRAGINGEN,
                "focus": FOCUSGEDRAGINGEN,
                "toetsenbord": TOETSENBORDGEDRAGINGEN,
            }
            for veld, toegestaan in waarden.items():
                waarde = contract.eigenschappen.get(veld)
                if waarde not in toegestaan:
                    diagnostics.append(Diagnostic(
                        code="BP3831",
                        boodschap=(
                            f"Toegankelijkheid '{contract.id}.{veld}' heeft "
                            f"onbekende waarde '{waarde}'"
                        ),
                        locatie=contract.eigenschaplocaties.get(
                            veld, contract.bronlocatie
                        ),
                    ))
            for veld in ("naambron", "waardebron", "foutbron"):
                if veld not in contract.eigenschappen:
                    continue
                waarde = contract.eigenschappen[veld]
                if not isinstance(waarde, str) or not waarde.strip():
                    diagnostics.append(Diagnostic(
                        code="BP3831",
                        boodschap=(
                            f"Toegankelijkheid '{contract.id}' vereist voor "
                            f"'{veld}' een betekenisvolle bron"
                        ),
                        locatie=contract.eigenschaplocaties.get(
                            veld, contract.bronlocatie
                        ),
                    ))

        for component in (
            obj for obj in context.objecten if obj.soort == "component"
        ):
            componentrol = component.eigenschappen.get("rol")
            anatomie = component.eigenschappen.get("anatomie")
            contract_id = component.eigenschappen.get("toegankelijkheid")
            contract = (
                contracten.get(contract_id)
                if isinstance(contract_id, str)
                else None
            )
            if contract_id is not None and contract is None:
                diagnostics.append(Diagnostic(
                    code="BP3832",
                    boodschap=(
                        f"Component '{component.id}' verwijst niet naar een "
                        "bestaand toegankelijkheidscontract"
                    ),
                    locatie=component.eigenschaplocaties.get(
                        "toegankelijkheid", component.bronlocatie
                    ),
                ))
                continue
            if componentrol not in VERWACHT_CONTRACT_PER_COMPONENTROL:
                continue
            if contract is None:
                diagnostics.append(Diagnostic(
                    code="BP3832",
                    boodschap=(
                        f"Component '{component.id}' vereist een bestaand "
                        "toegankelijkheidscontract"
                    ),
                    locatie=component.eigenschaplocaties.get(
                        "toegankelijkheid", component.bronlocatie
                    ),
                ))
                continue
            verwacht = VERWACHT_CONTRACT_PER_COMPONENTROL[componentrol]
            if contract.eigenschappen.get("rol") != verwacht["rol"]:
                diagnostics.append(Diagnostic(
                    code="BP3833",
                    boodschap=(
                        f"Toegankelijkheid '{contract.id}' past qua rol niet "
                        f"bij componentrol '{componentrol}'"
                    ),
                    locatie=contract.eigenschaplocaties.get(
                        "rol", contract.bronlocatie
                    ),
                ))
            bronnen = {
                veld: contract.eigenschappen.get(veld)
                for veld in ("naambron", "waardebron", "foutbron")
            }
            verwachte_bronnen = {
                veld: verwacht[veld]
                for veld in ("naambron", "waardebron", "foutbron")
            }
            anatomieset = (
                set(anatomie) if isinstance(anatomie, list) else set()
            )
            if (
                bronnen != verwachte_bronnen
                or any(
                    bron is not None and bron not in anatomieset
                    for bron in bronnen.values()
                )
            ):
                diagnostics.append(Diagnostic(
                    code="BP3834",
                    boodschap=(
                        f"Toegankelijkheid '{contract.id}' gebruikt niet de "
                        f"rolgebonden anatomie van component '{component.id}'"
                    ),
                    locatie=contract.bronlocatie,
                ))
            gedragingen = (
                ("disabled", "BP3835"),
                ("focus", "BP3836"),
                ("toetsenbord", "BP3837"),
            )
            for veld, code in gedragingen:
                if contract.eigenschappen.get(veld) != verwacht[veld]:
                    diagnostics.append(Diagnostic(
                        code=code,
                        boodschap=(
                            f"Toegankelijkheid '{contract.id}.{veld}' past "
                            f"niet bij componentrol '{componentrol}'"
                        ),
                        locatie=contract.eigenschaplocaties.get(
                            veld, contract.bronlocatie
                        ),
                    ))
        return tuple(diagnostics)
