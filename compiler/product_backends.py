"""Registryopbouw voor automatisch ontdekte productbackends."""
from __future__ import annotations

from compiler.backend import BackendRegistry
from compiler.backend_discovery import ontdek_backends


def standaard_backend_registry() -> BackendRegistry:
    registry = BackendRegistry()
    for backend in ontdek_backends():
        registry.registreer(backend)
    return registry
