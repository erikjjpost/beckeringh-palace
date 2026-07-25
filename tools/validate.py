#!/usr/bin/env python3
"""Validate the Beckeringh Palace vertical slice using only the Python stdlib."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIRS = [ROOT / "model", ROOT / "organisation"]
PROPOSALS_DIR = ROOT / "proposals"
FORBIDDEN_TERMS = (
    "anthropic", "claude", "openai", "chatgpt", "gpt-", "mistral",
    "gemini", "cohere", "ollama"
)


def load_json_yaml(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: ongeldig JSON/YAML: {exc}") from exc


def collect_files() -> list[Path]:
    files: list[Path] = []
    for base in MODEL_DIRS + [PROPOSALS_DIR]:
        files.extend(sorted(base.rglob("*.yaml")))
    return files


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    objects: dict[str, tuple[Path, dict[str, Any]]] = {}

    for path in collect_files():
        try:
            obj = load_json_yaml(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        object_id = obj.get("id")
        if not object_id:
            errors.append(f"{path.relative_to(ROOT)}: veld 'id' ontbreekt")
            continue
        if object_id in objects:
            errors.append(
                f"Dubbel id '{object_id}' in {path.relative_to(ROOT)} en "
                f"{objects[object_id][0].relative_to(ROOT)}"
            )
        objects[object_id] = (path, obj)

        if path.is_relative_to(ROOT / "model") or path.is_relative_to(ROOT / "organisation"):
            text = path.read_text(encoding="utf-8").lower()
            for term in FORBIDDEN_TERMS:
                if term in text:
                    errors.append(
                        f"{path.relative_to(ROOT)}: providerspecifieke term gevonden: '{term}'"
                    )

    known_ids = set(objects)

    for object_id, (path, obj) in objects.items():
        if obj.get("type") == "Service":
            supports = obj.get("supports")
            if not isinstance(supports, str):
                errors.append(f"{path.relative_to(ROOT)}: service ondersteunt niet exact één capability")
            elif supports not in known_ids:
                errors.append(f"{path.relative_to(ROOT)}: onbekende capability '{supports}'")
            elif objects[supports][1].get("type") != "Capability":
                errors.append(f"{path.relative_to(ROOT)}: '{supports}' is geen Capability")
            for output in obj.get("outputs", []):
                if output not in known_ids:
                    errors.append(f"{path.relative_to(ROOT)}: onbekend output-asset '{output}'")
            workflow = obj.get("workflow")
            if workflow and workflow not in known_ids:
                errors.append(f"{path.relative_to(ROOT)}: onbekende workflow '{workflow}'")

    for object_id, (path, obj) in objects.items():
        if obj.get("type") == "AgentRole":
            contract = obj.get("contract")
            if contract not in known_ids:
                errors.append(f"{path.relative_to(ROOT)}: onbekend contract '{contract}'")
            elif objects[contract][1].get("type") != "AgentContract":
                errors.append(f"{path.relative_to(ROOT)}: '{contract}' is geen AgentContract")
            if "modify_model" not in obj.get("prohibited", []):
                errors.append(f"{path.relative_to(ROOT)}: 'modify_model' moet verboden zijn")

    for object_id, (path, obj) in objects.items():
        if obj.get("type") == "RelationSet":
            for relation in obj.get("relations", []):
                for endpoint in ("from", "to"):
                    target = relation.get(endpoint)
                    if target not in known_ids:
                        errors.append(
                            f"{path.relative_to(ROOT)}: relatie verwijst naar onbekend object '{target}'"
                        )

    for object_id, (path, obj) in objects.items():
        if obj.get("type") == "ArchitectureProposal" and obj.get("status") == "approved":
            if not obj.get("approved_by"):
                errors.append(f"{path.relative_to(ROOT)}: goedgekeurd voorstel mist 'approved_by'")
            for change in obj.get("changes", []):
                target = change.get("object")
                if target not in known_ids:
                    warnings.append(
                        f"{path.relative_to(ROOT)}: wijziging verwijst naar nog niet bestaand object '{target}'"
                    )

    print("Beckeringh Palace validator")
    print(f"Objecten gecontroleerd: {len(objects)}")
    if warnings:
        print("\nWaarschuwingen:")
        for warning in warnings:
            print(f"  - {warning}")
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
