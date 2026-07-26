from __future__ import annotations

import importlib
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

from compiler.backend_discovery import backend_namen, ontdek_backends


class BackendDiscoveryTests(unittest.TestCase):
    def _package(self, bestanden: dict[str, str]):
        tijdelijk = tempfile.TemporaryDirectory()
        root = Path(tijdelijk.name)
        package = root / "test_backends"
        package.mkdir()
        (package / "__init__.py").write_text("", encoding="utf-8")
        for naam, inhoud in bestanden.items():
            (package / f"{naam}.py").write_text(textwrap.dedent(inhoud), encoding="utf-8")
        sys.path.insert(0, str(root))
        importlib.invalidate_caches()
        return tijdelijk

    def _cleanup(self, tijdelijk) -> None:
        sys.path.remove(tijdelijk.name)
        for naam in tuple(sys.modules):
            if naam == "test_backends" or naam.startswith("test_backends."):
                del sys.modules[naam]
        tijdelijk.cleanup()
        importlib.invalidate_caches()

    def test_ontdekt_plugins_deterministisch(self):
        tijdelijk = self._package({
            "zeta": '''
                from compiler.backend import Backend
                backend = Backend("zeta", lambda objecten, product: "z")
            ''',
            "alpha": '''
                from compiler.backend import Backend
                backend = Backend("alpha", lambda objecten, product: "a")
            ''',
        })
        try:
            self.assertEqual(["alpha", "zeta"], [item.naam for item in ontdek_backends("test_backends")])
            self.assertEqual(frozenset({"alpha", "zeta"}), backend_namen("test_backends"))
        finally:
            self._cleanup(tijdelijk)

    def test_weigert_module_zonder_backendcontract(self):
        tijdelijk = self._package({"ongeldig": "backend = object()"})
        try:
            with self.assertRaisesRegex(ValueError, "moet exact één Backend exporteren"):
                ontdek_backends("test_backends")
        finally:
            self._cleanup(tijdelijk)

    def test_weigert_dubbele_backendnaam(self):
        module = '''
            from compiler.backend import Backend
            backend = Backend("dubbel", lambda objecten, product: "")
        '''
        tijdelijk = self._package({"een": module, "twee": module})
        try:
            with self.assertRaisesRegex(ValueError, "Dubbele backendnaam"):
                ontdek_backends("test_backends")
        finally:
            self._cleanup(tijdelijk)


if __name__ == "__main__":
    unittest.main()
