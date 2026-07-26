"""Typesysteem voor relaties in Beckeringh Architectuurtaal."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RelatieSignatuur:
    """Toegestane bron- en doelsoorten voor één relatietype."""

    relatietype: str
    bronsoorten: frozenset[str] | None = None
    doelsoorten: frozenset[str] | None = None

    def accepteert_bron(self, soort: str) -> bool:
        return self.bronsoorten is None or soort in self.bronsoorten

    def accepteert_doel(self, soort: str) -> bool:
        return self.doelsoorten is None or soort in self.doelsoorten


RELATIESIGNATUREN = {
    signatuur.relatietype: signatuur
    for signatuur in (
        RelatieSignatuur(
            relatietype="ondersteunt",
            bronsoorten=frozenset({"dienst"}),
            doelsoorten=frozenset({"capability"}),
        ),
        RelatieSignatuur(
            relatietype="eigenaar",
            bronsoorten=frozenset({"capability"}),
            doelsoorten=frozenset({"agent"}),
        ),
    )
}
