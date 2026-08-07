"""Regressiecontract voor de offline Figma development-pluginadapter."""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from compiler.figma_plugin_adapter import render_plugin_code, render_plugin_manifest


ROOT = Path(__file__).resolve().parents[1]
FIGMA_MANIFEST = ROOT / "output" / "products" / "emberforge-master.figma.json"


class FigmaPluginAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest_text = FIGMA_MANIFEST.read_text(encoding="utf-8")
        self.payload = json.loads(self.manifest_text)

    def test_pluginpakket_is_netwerkloos_en_dynamic_page_compatibel(self) -> None:
        manifest = json.loads(render_plugin_manifest())
        self.assertEqual("1.0.0", manifest["api"])
        self.assertEqual(["figma"], manifest["editorType"])
        self.assertEqual("dynamic-page", manifest["documentAccess"])
        self.assertEqual(["none"], manifest["networkAccess"]["allowedDomains"])
        self.assertEqual("code.js", manifest["main"])

    def test_plugin_code_is_deterministisch_en_snapshotgebonden(self) -> None:
        eerste = render_plugin_code(self.manifest_text)
        tweede = render_plugin_code(self.manifest_text)
        self.assertEqual(eerste, tweede)
        self.assertNotIn("__BECKERINGH_FIGMA_MANIFEST__", eerste)
        self.assertIn(self.payload["product"]["snapshot"], eerste)
        self.assertNotIn("fetch(", eerste)
        self.assertNotIn("figmaApi.fetch", eerste)

    def test_plugin_planning_dekt_het_volledige_mastermanifest(self) -> None:
        code = render_plugin_code(self.manifest_text)
        with tempfile.TemporaryDirectory() as tmp:
            plugin = Path(tmp) / "code.js"
            plugin.write_text(code, encoding="utf-8")
            script = """
const adapter = require(process.argv[1]);
const first = adapter.desiredState(adapter.manifest);
const second = adapter.desiredState(adapter.manifest);
if (JSON.stringify(first) !== JSON.stringify(second)) process.exit(3);
console.log(JSON.stringify({
  collections: first.collections,
  textStyles: first.textStyles.length,
  effectStyles: first.effectStyles.length,
  assets: first.assets.length,
  componentFamilies: first.components.length,
  figmaVariants: first.components.reduce((n, c) => n + c.figmaVariants.length, 0),
  compositions: first.compositions.length,
  layouts: first.layouts.length,
}));
"""
            result = subprocess.run(
                ["node", "-e", script, str(plugin)],
                check=True,
                capture_output=True,
                text=True,
            )
        summary = json.loads(result.stdout)
        self.assertEqual(25, summary["collections"]["primitives"])
        self.assertEqual(8, summary["collections"]["palette"])
        self.assertEqual(27, summary["collections"]["material"])
        self.assertEqual(30, summary["collections"]["typography"])
        self.assertEqual(6, summary["textStyles"])
        self.assertEqual(7, summary["effectStyles"])
        self.assertEqual(11, summary["assets"])
        self.assertEqual(7, summary["componentFamilies"])
        self.assertEqual(7, summary["compositions"])
        self.assertEqual(7, summary["layouts"])
        self.assertGreater(summary["figmaVariants"], 20)

    def test_ongeldige_schemaversie_wordt_geweigerd(self) -> None:
        payload = json.loads(self.manifest_text)
        payload["schema_version"] = 1
        with self.assertRaisesRegex(ValueError, "schema 2"):
            render_plugin_code(json.dumps(payload))


if __name__ == "__main__":
    unittest.main()
