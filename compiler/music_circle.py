"""Native, gevalideerde Circle of Fifths semantiek en vectorgeometrie."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.diagnostics import Diagnostic
from compiler.svg_assets import ResolvedSvgAsset


EXPECTED_MAJOR = ("C", "G", "D", "A", "E", "B", "F#/Gb", "Db", "Ab", "Eb", "Bb", "F")
EXPECTED_MINOR = ("Am", "Em", "Bm", "F#m", "C#m", "G#m", "D#m/Ebm", "Bbm", "Fm", "Cm", "Gm", "Dm")
EXPECTED_SIGNATURES = ("0", "1#", "2#", "3#", "4#", "5#", "6#/6b", "5b", "4b", "3b", "2b", "1b")


@dataclass(frozen=True)
class ResolvedMusicCircle:
    id: str
    naam: str
    doel: str
    majeur: tuple[str, ...]
    mineur: tuple[str, ...]
    voortekens: tuple[str, ...]
    asset: ResolvedSvgAsset


@dataclass(frozen=True)
class MusicCircleConstraint:
    sleutel: str = "world-model.music-circle"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        allowed = {"naam", "doel", "majeur", "mineur", "voortekens"}
        for obj in (item for item in context.objecten if item.soort == "muziekcirkel"):
            for field in obj.eigenschappen:
                if field not in allowed:
                    diagnostics.append(Diagnostic(code="BP4401", boodschap=f"Muziekcirkel '{obj.id}' heeft onbekende eigenschap '{field}'", locatie=obj.eigenschaplocaties.get(field, obj.bronlocatie)))
            for field, expected, code in (
                ("majeur", EXPECTED_MAJOR, "BP4402"),
                ("mineur", EXPECTED_MINOR, "BP4403"),
                ("voortekens", EXPECTED_SIGNATURES, "BP4404"),
            ):
                value = obj.eigenschappen.get(field)
                if not isinstance(value, list) or tuple(value) != expected:
                    diagnostics.append(Diagnostic(code=code, boodschap=f"Muziekcirkel '{obj.id}' vereist de canonieke twaalf waarden voor '{field}'", locatie=obj.eigenschaplocaties.get(field, obj.bronlocatie)))
        return tuple(diagnostics)


# Generieke enkel-lijn vectorglyphs op een 4 bij 6 raster.
_GLYPHS: dict[str, tuple[tuple[tuple[float, float], ...], ...]] = {
    "A": (((0, 6), (2, 0), (4, 6)), ((1, 3), (3, 3))),
    "B": (((0, 0), (0, 6), (2.5, 6), (4, 5), (4, 4), (2.5, 3), (0, 3)), ((2.5, 3), (4, 2), (4, 1), (2.5, 0), (0, 0))),
    "C": (((4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (3, 6), (4, 5)),),
    "D": (((0, 0), (0, 6), (1.5, 6), (4, 5), (4, 1), (1.5, 0), (0, 0)),),
    "E": (((4, 0), (0, 0), (0, 6), (4, 6)), ((0, 3), (3, 3))),
    "F": (((0, 6), (0, 0), (4, 0)), ((0, 3), (3, 3))),
    "G": (((4, 1), (3, 0), (1, 0), (0, 1), (0, 5), (1, 6), (4, 6), (4, 3), (2.5, 3)),),
    "#": (((1, 0), (1, 6)), ((3, 0), (3, 6)), ((0, 2), (4, 2)), ((0, 4), (4, 4))),
    "b": (((0, 0), (0, 6)), ((0, 3), (2, 2), (4, 3), (4, 5), (2, 6), (0, 5))),
    "m": (((0, 6), (0, 2), (2, 2), (2, 6)), ((2, 3), (3, 2), (4, 3), (4, 6))),
    "/": (((0, 6), (4, 0)),),
    "0": (((1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0)),),
    "1": (((1, 1), (2, 0), (2, 6)), ((1, 6), (3, 6))),
    "2": (((0, 1), (1, 0), (3, 0), (4, 1), (4, 2), (0, 6), (4, 6)),),
    "3": (((0, 0), (3, 0), (4, 1), (3, 3), (1.5, 3)), ((3, 3), (4, 5), (3, 6), (0, 6))),
    "4": (((3, 6), (3, 0), (0, 4), (4, 4)),),
    "5": (((4, 0), (0, 0), (0, 3), (3, 3), (4, 4), (4, 5), (3, 6), (0, 6)),),
    "6": (((4, 0), (1, 0), (0, 2), (0, 5), (1, 6), (3, 6), (4, 5), (4, 4), (3, 3), (0, 3)),),
}


def _fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def _text_paths(text: str, center_x: float, center_y: float, height: float) -> list[str]:
    scale = height / 6
    advance = 5 * scale
    width = len(text) * advance - scale
    origin_x = center_x - width / 2
    origin_y = center_y - height / 2
    paths = []
    for index, character in enumerate(text):
        for stroke in _GLYPHS[character]:
            points = [(_fmt(origin_x + index * advance + x * scale), _fmt(origin_y + y * scale)) for x, y in stroke]
            paths.append("M" + " L".join(f"{x} {y}" for x, y in points))
    return paths


def _circle_path(radius: float) -> str:
    left, right = 500 - radius, 500 + radius
    return f"M{left:g} 500 A{radius:g} {radius:g} 0 1 0 {right:g} 500 A{radius:g} {radius:g} 0 1 0 {left:g} 500 Z"


def _build_asset(circle: Architectuurobject) -> ResolvedSvgAsset:
    paths = [_circle_path(465), _circle_path(345), _circle_path(225)]
    for index in range(12):
        angle = math.radians(index * 30 - 105)
        inner = (500 + 225 * math.cos(angle), 500 + 225 * math.sin(angle))
        outer = (500 + 465 * math.cos(angle), 500 + 465 * math.sin(angle))
        paths.append(f"M{_fmt(inner[0])} {_fmt(inner[1])} L{_fmt(outer[0])} {_fmt(outer[1])}")
    for index, labels in enumerate(zip(circle.eigenschappen["majeur"], circle.eigenschappen["mineur"], circle.eigenschappen["voortekens"])):
        angle = math.radians(index * 30 - 90)
        for radius, label, height in ((405, labels[0], 33), (285, labels[1], 25), (180, labels[2], 20)):
            if radius == 285 and len(label) > 5:
                height = 19
            paths.extend(_text_paths(label, 500 + radius * math.cos(angle), 500 + radius * math.sin(angle), height))
    return ResolvedSvgAsset(
        id=circle.id, naam=circle.eigenschappen["naam"], doel=circle.eigenschappen["doel"], rol="illustratie",
        viewbox=(0.0, 0.0, 1000.0, 1000.0), paden=tuple(paths), vulling="none", lijn="currentColor",
        lijndikte=2.0, lijneinde="round", lijnverbinding="round", toegankelijkheid="informatief",
        label="Circle of Fifths met majeur, relatieve mineur en voortekens", familie=None, variant=None,
    )


def resolveer_muziekcirkels(objecten: Iterable[Architectuurobject]) -> tuple[ResolvedMusicCircle, ...]:
    circles = []
    for obj in objecten:
        if obj.soort == "muziekcirkel":
            circles.append(ResolvedMusicCircle(obj.id, obj.eigenschappen["naam"], obj.eigenschappen["doel"], tuple(obj.eigenschappen["majeur"]), tuple(obj.eigenschappen["mineur"]), tuple(obj.eigenschappen["voortekens"]), _build_asset(obj)))
    return tuple(circles)
