"""Canonieke tussenrepresentatie voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Bronlocatie:
    """Exacte locatie in een BAT-bronbestand."""

    bron: str
    regel: int
    kolom: int = 1

    def __str__(self) -> str:
        return f"{self.bron}:{self.regel}:{self.kolom}"


@dataclass(frozen=True)
class Architectuurobject:
    soort: str
    id: str
    eigenschappen: dict[str, Any]
    bronlocatie: Bronlocatie | None = field(default=None, compare=False, repr=False)
    eigenschaplocaties: dict[str, Bronlocatie] = field(
        default_factory=dict,
        compare=False,
        repr=False,
    )

    def als_dict(self) -> dict[str, Any]:
        """Geef een deterministische, serialiseerbare representatie terug."""
        return {
            "soort": self.soort,
            "id": self.id,
            "eigenschappen": self.eigenschappen,
        }
