from __future__ import annotations

import unittest
from pathlib import Path

from compiler.parser import parseer_bestand
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.terminal_theme_renderer import naar_dircolors, naar_ps1


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


class TerminalThemeRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.objecten = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        ).objecten

    def test_dircolors_gebruikt_opgeloste_materiaalkleuren(self) -> None:
        inhoud = naar_dircolors(self.objecten)

        self.assertIn("TERM *", inhoud)
        self.assertIn("DIR 38;2;125;211;252;01", inhoud)
        self.assertIn("LINK 38;2;165;222;251;01", inhoud)
        self.assertIn("ORPHAN 38;2;248;113;113;01", inhoud)
        self.assertIn("EXEC 38;2;74;222;128;01", inhoud)
        self.assertIn(".tar 38;2;201;137;91;01", inhoud)
        self.assertIn(".png 38;2;226;169;130", inhoud)
        self.assertIn(".mp3 38;2;184;197;214", inhoud)
        self.assertNotIn("COLORTERM", inhoud)

    def test_dircolors_is_deterministisch(self) -> None:
        self.assertEqual(
            naar_dircolors(self.objecten),
            naar_dircolors(self.objecten),
        )

    def test_ps1_gebruikt_opgeloste_materiaalkleuren(self) -> None:
        inhoud = naar_ps1(self.objecten)

        self.assertIn(r"PS1+='\[\033[38;2;201;137;91;1m\]\u@\h", inhoud)
        self.assertIn(r"PS1+='\[\033[38;2;184;197;214m\]:", inhoud)
        self.assertIn(r"PS1+='\[\033[38;2;125;211;252;1m\]\w", inhoud)
        self.assertIn(r"PS1+='\[\033[38;2;74;222;128m\]\$", inhoud)
        self.assertIn("export PS1", inhoud)
        self.assertIn("__venv_ps1", inhoud)


if __name__ == "__main__":
    unittest.main()
