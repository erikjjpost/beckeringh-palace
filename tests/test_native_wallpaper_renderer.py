from __future__ import annotations

import binascii
import struct
import unittest
import zlib
from pathlib import Path

from compiler.parser import parseer, parseer_bestand
from compiler.product_backends import standaard_backend_registry
from compiler.product_compiler import compileer_producten
from compiler.product_constraints import WORLD_MODEL_CONSTRAINTS
from compiler.semantic import analyseer
from compiler.wallpaper_png_renderer import PNG_SIGNATURE


ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "architectuur" / "world.bp"


BRON = '''
kleur ink {
    naam: "Ink"
    doel: "Donker canvas."
    waarde: "#102030"
}
kleur bone {
    naam: "Bone"
    doel: "Lichte voorgrond."
    waarde: "#F0E0D0"
}
palet forge-palette {
    naam: "Forge palette"
    doel: "Minimaal renderpalet."
    background: "ink"
    foreground: "bone"
}
typografie forge-type {
    naam: "Forge type"
    doel: "Lokale testtypografie."
    heading: ["Aptos Display", "sans-serif"]
    body: ["Aptos", "sans-serif"]
    mono: ["JetBrains Mono", "monospace"]
    levering: "local-only"
}
materiaal forge-material {
    naam: "Forge material"
    doel: "Semantische renderkleuren."
    canvas: "ink"
    foreground: "bone"
}
thema forge {
    naam: "Forge"
    doel: "Wallpaper renderthema."
    palet: "forge-palette"
    typografie: "forge-type"
    materiaal: "forge-material"
}
wereld palace {
    naam: "Palace"
    doel: "Wallpaper renderwereld."
    thema: "forge"
}
merk emberforge {
    naam: "EmberForge"
    doel: "Wallpaper testmerk."
    tagline: "Sovereign Infrastructure."
    belofte: "Sovereignty over your own stack."
    principes: ["Own your data.", "Own your nodes.", "Own your forge."]
    producten: ["Wallpaper"]
    taal: "Nederlands"
    stem: "Technisch en rustig"
}
asset forge-frame {
    naam: "Forge Frame"
    doel: "Eenvoudig gesloten lijnornament."
    formaat: "svg"
    rol: "ornament"
    viewbox: "0 0 10 10"
    paden: ["M0 0 H10 V10 H0 Z"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "1"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "decoratief"
}
wallpaper forge-test {
    naam: "Forge Test"
    doel: "Klein deterministisch rendercanvas."
    wereld: "palace"
    merk: "emberforge"
    formaat: "png"
    breedte: "64"
    hoogte: "32"
    canvas: "canvas"
    lagen: ["forge-ornament-layer"]
}
wallpaperlaag forge-ornament-layer {
    naam: "Ornamentlaag"
    doel: "Draagt het testornament."
    wallpaper: "forge-test"
    rol: "ornament"
    plaatsingen: ["forge-frame-placement"]
}
assetplaatsing forge-frame-placement {
    naam: "Forge frame"
    doel: "Plaatst het testornament."
    laag: "forge-ornament-layer"
    asset: "forge-frame"
    x: "8"
    y: "8"
    breedte: "16"
    hoogte: "16"
    fit: "contain"
    dekking: "1"
    kleur: "foreground"
}
product forge-test-png {
    naam: "Forge Test PNG"
    doel: "Rendert het kleine testcanvas."
    backend: "wallpaper-png"
    mode: "static"
    inhoud: "wallpaper"
    wereld: "palace"
    wallpaper: "forge-test"
    pad: "output/products/forge-test.png"
}
'''


def _chunks(payload: bytes) -> tuple[tuple[bytes, bytes], ...]:
    if not payload.startswith(PNG_SIGNATURE):
        raise AssertionError("Ongeldige PNG signature")
    chunks = []
    offset = len(PNG_SIGNATURE)
    while offset < len(payload):
        length = struct.unpack(">I", payload[offset:offset + 4])[0]
        name = payload[offset + 4:offset + 8]
        data = payload[offset + 8:offset + 8 + length]
        checksum = struct.unpack(
            ">I",
            payload[offset + 8 + length:offset + 12 + length],
        )[0]
        expected = binascii.crc32(name)
        expected = binascii.crc32(data, expected) & 0xFFFFFFFF
        if checksum != expected:
            raise AssertionError(f"Ongeldige CRC voor {name!r}")
        chunks.append((name, data))
        offset += length + 12
        if name == b"IEND":
            break
    if offset != len(payload):
        raise AssertionError("Data achter PNG IEND")
    return tuple(chunks)


def _png_info(payload: bytes) -> dict[str, object]:
    chunks = _chunks(payload)
    header = next(data for name, data in chunks if name == b"IHDR")
    width, height, bit_depth, color_type, _, _, _ = struct.unpack(
        ">IIBBBBB",
        header,
    )
    palette_data = next(
        (data for name, data in chunks if name == b"PLTE"),
        b"",
    )
    palette = tuple(
        tuple(palette_data[offset:offset + 3])
        for offset in range(0, len(palette_data), 3)
    )
    compressed = b"".join(data for name, data in chunks if name == b"IDAT")
    rows = zlib.decompress(compressed)
    metadata = {}
    for name, data in chunks:
        if name != b"tEXt":
            continue
        key, value = data.split(b"\x00", 1)
        metadata[key.decode("latin-1")] = value.decode("latin-1")
    return {
        "width": width,
        "height": height,
        "bit_depth": bit_depth,
        "color_type": color_type,
        "palette": palette,
        "rows": rows,
        "metadata": metadata,
    }


def _indexed_pixel(info: dict[str, object], x: int, y: int) -> tuple[int, ...]:
    width = int(info["width"])
    bit_depth = int(info["bit_depth"])
    palette = info["palette"]
    rows = info["rows"]
    row_length = (width * bit_depth + 7) // 8
    row_offset = y * (row_length + 1)
    if rows[row_offset] != 0:
        raise AssertionError("Testdecoder ondersteunt alleen PNG filter 0")
    byte_value = rows[row_offset + 1 + (x * bit_depth) // 8]
    shift = 8 - bit_depth - (x * bit_depth) % 8
    index = (byte_value >> shift) & ((1 << bit_depth) - 1)
    return palette[index]


class NativeWallpaperRendererTests(unittest.TestCase):
    def _compile(self, bron: str = BRON) -> bytes:
        model = analyseer(
            parseer(bron),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        product = compileer_producten(
            model.objecten,
            standaard_backend_registry(),
        )[0]
        self.assertIsInstance(product.inhoud, bytes)
        return product.inhoud

    def test_rendert_een_geldige_deterministische_indexed_png(self) -> None:
        payload = self._compile()
        info = _png_info(payload)

        self.assertEqual((64, 32), (info["width"], info["height"]))
        self.assertEqual(1, info["bit_depth"])
        self.assertEqual(3, info["color_type"])
        self.assertEqual(
            {
                "bp-product": "forge-test-png",
                "bp-wallpaper": "forge-test",
            },
            {
                key: info["metadata"][key]
                for key in ("bp-product", "bp-wallpaper")
            },
        )
        self.assertTrue(info["metadata"]["bp-snapshot"].startswith("sha256:"))
        self.assertEqual((0x10, 0x20, 0x30), _indexed_pixel(info, 0, 0))
        self.assertEqual((0xF0, 0xE0, 0xD0), _indexed_pixel(info, 8, 8))
        self.assertEqual((0x10, 0x20, 0x30), _indexed_pixel(info, 16, 16))

    def test_png_is_onafhankelijk_van_bronvolgorde(self) -> None:
        model = analyseer(
            parseer(BRON),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        registry = standaard_backend_registry()

        first = compileer_producten(model.objecten, registry)[0].inhoud
        second = compileer_producten(
            tuple(reversed(model.objecten)),
            registry,
        )[0].inhoud

        self.assertEqual(first, second)

    def test_rasteriseert_alle_veilige_padcommandos_en_fitmodi(self) -> None:
        path = (
            "M1 5 L2 5 H3 V6 C3 7 4 7 4 6 S5 5 6 6 "
            "Q7 7 8 6 T9 5 A2 2 0 0 1 7 3 Z"
        )
        for fit in ("contain", "cover", "stretch"):
            with self.subTest(fit=fit):
                payload = self._compile(
                    BRON.replace(
                        "M0 0 H10 V10 H0 Z",
                        path,
                    ).replace(
                        '    fit: "contain"',
                        f'    fit: "{fit}"',
                    )
                )
                info = _png_info(payload)
                self.assertEqual((64, 32), (info["width"], info["height"]))

    def test_rasteriseert_gevulde_native_assets(self) -> None:
        payload = self._compile(
            BRON.replace(
                '    vulling: "none"\n'
                '    lijn: "currentColor"\n'
                '    lijndikte: "1"\n'
                '    lijneinde: "round"\n'
                '    lijnverbinding: "round"',
                '    vulling: "currentColor"\n'
                '    lijn: "none"',
            )
        )
        info = _png_info(payload)

        self.assertEqual((0xF0, 0xE0, 0xD0), _indexed_pixel(info, 16, 16))

    def test_world_publiceert_het_eerste_ultrawide_beeldartifact(self) -> None:
        model = analyseer(
            parseer_bestand(WORLD),
            constraints=WORLD_MODEL_CONSTRAINTS,
        )
        products = {
            product.definitie.id: product
            for product in compileer_producten(
                model.objecten,
                standaard_backend_registry(),
            )
        }

        product = products["emberforge-ultrawide-wallpaper-png"]
        self.assertIsInstance(product.inhoud, bytes)
        info = _png_info(product.inhoud)

        self.assertEqual((3840, 1080), (info["width"], info["height"]))
        self.assertEqual(3, info["color_type"])
        self.assertLess(len(product.inhoud), 2_000_000)
        self.assertEqual(
            product.definitie.snapshot_ref,
            info["metadata"]["bp-snapshot"],
        )
        self.assertTrue({
            (0x0F, 0x17, 0x24),
            (0xC9, 0x89, 0x5B),
            (0xE6, 0xED, 0xF5),
        }.issubset(set(info["palette"])))


if __name__ == "__main__":
    unittest.main()
