#!/usr/bin/env python3
"""Beckeringh Palace developer command line entrypoint."""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]


def run(command: Sequence[str]) -> None:
    """Run a project command from the repository root without bytecode side effects."""
    print(f"\n$ {' '.join(command)}", flush=True)
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run(command, cwd=ROOT, check=True, env=environment)


def repository_status() -> list[str]:
    """Return tracked and untracked working-tree changes."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def check(require_clean_tree: bool = True) -> int:
    """Validate, compile, generate, test and, by default, verify reproducibility.

    De keten (validate, compile, generate, render_status, tests) is identiek in
    beide fasen. Met ``require_clean_tree=False`` (precommit) wordt de
    werkboomcontrole overgeslagen, omdat een agent op dat moment nog
    ongecommitte BAT-broncode heeft die de generatie bewust wijzigt. Met
    ``require_clean_tree=True`` (postcommit, de standaard) moet een tweede
    generatie op een schone boom géén wijziging meer opleveren.
    """
    run([sys.executable, "tools/validate.py"])
    run([sys.executable, "tools/compile_bat.py"])
    run([sys.executable, "tools/generate.py"])
    run([sys.executable, "tools/render_status.py"])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])

    if not require_clean_tree:
        print("\nRESULTAAT: GELDIG (precommit, reproduceerbaarheid niet gecontroleerd)")
        return 0

    changes = repository_status()
    if changes:
        print("\nRESULTAAT: NIET REPRODUCEERBAAR", file=sys.stderr)
        print("Generatie of tests hebben de repository gewijzigd:", file=sys.stderr)
        for change in changes:
            print(f"  {change}", file=sys.stderr)
        return 1

    print("\nRESULTAAT: GELDIG EN REPRODUCEERBAAR")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="bp", description="Beckeringh Palace project tooling")
    parser.add_argument("command", choices=("check",), help="Project command to execute")
    parser.add_argument(
        "--pre-commit",
        action="store_true",
        help=(
            "Sla de werkboomcontrole over. Gebruik dit vóór de definitieve "
            "commit, wanneer BAT-bronwijzigingen bewust nog ongecommit staan."
        ),
    )
    args = parser.parse_args()

    if args.command == "check":
        return check(require_clean_tree=not args.pre_commit)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
