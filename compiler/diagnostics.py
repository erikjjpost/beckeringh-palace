"""Gestructureerde compilerdiagnostics voor Beckeringh Palace."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from compiler.cir import Bronlocatie


class Ernst(str, Enum):
    FOUT = "fout"
    WAARSCHUWING = "waarschuwing"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    boodschap: str
    ernst: Ernst = Ernst.FOUT
    locatie: Bronlocatie | None = None

    def __str__(self) -> str:
        prefix = f"{self.locatie}: " if self.locatie else ""
        return f"{prefix}{self.code}: {self.boodschap}"
