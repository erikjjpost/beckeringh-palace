#!/usr/bin/env python3
"""Generate documentation and Mermaid output from the BP-Core model."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "model"
OUTPUT = ROOT / "output"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    capability = load(MODEL / "capabilities" / "second-brain.yaml")
    dependency = load(MODEL / "capabilities" / "information-management.yaml")
    service = load(MODEL / "services" / "architecture-synchronisation.yaml")
    representation = load(MODEL / "representations" / "the-library.yaml")

    docs = OUTPUT / "docs"
    diagrams = OUTPUT / "diagrams"
    docs.mkdir(parents=True, exist_ok=True)
    diagrams.mkdir(parents=True, exist_ok=True)

    document = f"""# {capability['name']}

## Doel

{capability['purpose']}

## Afhankelijkheid

- {dependency['name']}

## Service

### {service['name']}

{service['purpose']}

## Representatie

- {representation['name']}: {representation['description']}
"""
    (docs / "second-brain.md").write_text(document, encoding="utf-8")

    mermaid = f"""flowchart LR
    IM[\"{dependency['name']}\"] --> SB[\"{capability['name']}\"]
    SB --> AS[\"{service['name']}\"]
    AS --> AP[Architectuurvoorstel]
    AS --> SL[Synchronisatielog]
    LIB[\"{representation['name']}\"] -. representeert .-> SB
"""
    (diagrams / "second-brain.mmd").write_text(mermaid, encoding="utf-8")

    print("Gegenereerd:")
    print("  output/docs/second-brain.md")
    print("  output/diagrams/second-brain.mmd")


if __name__ == "__main__":
    main()
