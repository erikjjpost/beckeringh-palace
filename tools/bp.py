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


def check() -> int:
    """Validate, compile, generate, test and verify reproducibility."""
    run([sys.executable, "tools/validate.py"])
    run([sys.executable, "tools/compile_bat.py"])
    run([sys.executable, "tools/generate.py"])
    run([sys.executable, "tools/render_status.py"])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])

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
    args = parser.parse_args()

    if args.command == "check":
        return check()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
