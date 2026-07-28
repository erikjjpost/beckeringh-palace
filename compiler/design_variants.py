"""Getypeerd, backend-onafhankelijk model voor componentvarianten."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject


COMPONENT_STATE_FIELDS = ("hover", "focus", "pressed", "disabled")
COMPONENT_STATES = ("rest", *COMPONENT_STATE_FIELDS)


@dataclass(frozen=True)
class ResolvedComponentVariant:
    id: str
    naam: str
    doel: str
    component_id: str
    appearance_id: str
    state_appearances: tuple[tuple[str, str], ...]

    def appearance_for_state(self, state: str) -> str | None:
        return next(
            (
                appearance_id
                for state_name, appearance_id in self.state_appearances
                if state_name == state
            ),
            None,
        )


class VariantResolutionError(ValueError):
    """Niet-gevalideerde CIR kan niet tot componentvarianten worden opgelost."""


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise VariantResolutionError(
            f"Variant '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def resolveer_varianten(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedComponentVariant, ...]:
    varianten = []
    for obj in objecten:
        if obj.soort != "variant":
            continue
        appearance_id = _tekst(obj, "appearance")
        varianten.append(
            ResolvedComponentVariant(
                id=obj.id,
                naam=_tekst(obj, "naam"),
                doel=_tekst(obj, "doel"),
                component_id=_tekst(obj, "component"),
                appearance_id=appearance_id,
                state_appearances=(
                    ("rest", appearance_id),
                    *(
                        (state, _tekst(obj, state))
                        for state in COMPONENT_STATE_FIELDS
                        if state in obj.eigenschappen
                    ),
                ),
            )
        )
    return tuple(sorted(varianten, key=lambda variant: variant.id))
