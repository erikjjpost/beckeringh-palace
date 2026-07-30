"""Backendcontract en registry voor Beckeringh Palace-producten."""
from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

from compiler.cir import Architectuurobject
from compiler.product_model import ProductDefinition

BackendPayload = str | bytes
BackendRenderer = Callable[
    [Iterable[Architectuurobject], ProductDefinition],
    BackendPayload,
]


@dataclass(frozen=True)
class Backend:
    naam: str
    render: BackendRenderer


class BackendRegistry:
    def __init__(self) -> None:
        self._backends: dict[str, Backend] = {}

    def registreer(self, backend: Backend) -> None:
        if backend.naam in self._backends:
            raise ValueError(f"Backend '{backend.naam}' is al geregistreerd")
        self._backends[backend.naam] = backend

    def resolveer(self, naam: str) -> Backend:
        try:
            return self._backends[naam]
        except KeyError as exc:
            raise KeyError(f"Onbekende backend '{naam}'") from exc

    @property
    def namen(self) -> frozenset[str]:
        return frozenset(self._backends)
