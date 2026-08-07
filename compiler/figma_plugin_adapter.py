"""Deterministische verpakking van het Figma manifest als development plugin."""
from __future__ import annotations

import json
from pathlib import Path


SCHEMA_VERSION = 2
PLUGIN_ID = "000000000000000000"
PLUGIN_TEMPLATE = Path(__file__).resolve().parents[1] / "adapters" / "figma" / "plugin.js"


def render_plugin_code(manifest_text: str) -> str:
    """Verpak exact één gevalideerd Figma manifest in de offline adapter."""

    payload = json.loads(manifest_text)
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Figma plugin vereist manifest schema {SCHEMA_VERSION}"
        )
    template = PLUGIN_TEMPLATE.read_text(encoding="utf-8")
    marker = "__BECKERINGH_FIGMA_MANIFEST__"
    if template.count(marker) != 1:
        raise ValueError("Figma plugintemplate vereist exact één manifestmarker")
    embedded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return template.replace(marker, embedded)


def render_plugin_manifest() -> str:
    """Genereer de minimale netwerkloze Figma development-pluginmanifestatie."""

    payload = {
        "name": "Beckeringh Palace Sync",
        "id": PLUGIN_ID,
        "api": "1.0.0",
        "main": "code.js",
        "editorType": ["figma"],
        "documentAccess": "dynamic-page",
        "networkAccess": {"allowedDomains": ["none"]},
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def package_plugin(manifest_path: Path, output_dir: Path) -> tuple[Path, Path]:
    """Bouw het lokale pluginpakket uitsluitend uit het gegenereerde manifest."""

    manifest_text = manifest_path.read_text(encoding="utf-8")
    output_dir.mkdir(parents=True, exist_ok=True)
    code_path = output_dir / "code.js"
    plugin_manifest_path = output_dir / "manifest.json"
    code_path.write_text(render_plugin_code(manifest_text), encoding="utf-8")
    plugin_manifest_path.write_text(render_plugin_manifest(), encoding="utf-8")
    return code_path, plugin_manifest_path
