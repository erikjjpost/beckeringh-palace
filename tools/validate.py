#!/usr/bin/env python3
"""Validate the Beckeringh Palace design-input contracts using only the Python stdlib."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from compiler.design_input import load_design_input

DESIGN_INPUTS_DIR = ROOT / "project" / "design-inputs"


def main() -> int:
    errors: list[str] = []
    checked = 0

    for path in sorted(DESIGN_INPUTS_DIR.glob("*.json")):
        checked += 1
        try:
            load_design_input(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    print("Beckeringh Palace validator")
    print(f"Ontwerpbroncontracten gecontroleerd: {checked}")
    if errors:
        print("\nFouten:")
        for error in errors:
            print(f"  - {error}")
        print(f"\nRESULTAAT: MISLUKT ({len(errors)} fout(en))")
        return 1

    print("\nRESULTAAT: GELDIG")
    return 0


if __name__ == "__main__":
    sys.exit(main())
