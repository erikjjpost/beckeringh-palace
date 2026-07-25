"""Canonieke tussenrepresentatie voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Architectuurobject:
    soort: str
    id: str
    eigenschappen: dict[str, Any]

    def als_dict(self) -> dict[str, Any]:
        """Geef een deterministische, serialiseerbare representatie terug."""
        return asdict(self)
