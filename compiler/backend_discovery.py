"""Deterministische discovery van Beckeringh Palace-backendplugins."""
from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterable

from compiler.backend import Backend


def ontdek_backends(package_naam: str = "compiler.backends") -> tuple[Backend, ...]:
    package = importlib.import_module(package_naam)
    package_paden = getattr(package, "__path__", None)
    if package_paden is None:
        raise ValueError(f"Backendpackage '{package_naam}' is geen package")

    module_namen = sorted(
        info.name
        for info in pkgutil.iter_modules(package_paden, package.__name__ + ".")
        if not info.name.rsplit(".", 1)[-1].startswith("_")
    )
    backends = []
    for module_naam in module_namen:
        module = importlib.import_module(module_naam)
        backend = getattr(module, "backend", None)
        if not isinstance(backend, Backend):
            raise ValueError(
                f"Backendmodule '{module_naam}' moet exact één Backend exporteren als 'backend'"
            )
        backends.append(backend)

    namen = [backend.naam for backend in backends]
    dubbele_namen = sorted({naam for naam in namen if namen.count(naam) > 1})
    if dubbele_namen:
        raise ValueError(f"Dubbele backendnaam/namen: {', '.join(dubbele_namen)}")

    return tuple(backends)


def backend_namen(package_naam: str = "compiler.backends") -> frozenset[str]:
    return frozenset(backend.naam for backend in ontdek_backends(package_naam))
