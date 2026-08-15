"""Deterministische PNG-rendering van opgeloste native wallpaperproducten."""
from __future__ import annotations

from dataclasses import dataclass
import binascii
from functools import lru_cache
import math
import re
import struct
from typing import Iterable
import zlib

from compiler.svg_assets import ResolvedSvgAsset
from compiler.wallpaper_products import (
    ResolvedWallpaper,
    ResolvedWallpaperAssetPlacement,
)


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_NUMBER = r"[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?"
_PATH_TOKEN = re.compile(rf"{_NUMBER}|[AaCcHhLlMmQqSsTtVvZz]")
_ARITY = {
    "A": 7,
    "C": 6,
    "H": 1,
    "L": 2,
    "M": 2,
    "Q": 4,
    "S": 4,
    "T": 2,
    "V": 1,
    "Z": 0,
}
_Point = tuple[float, float]
_Bounds = tuple[int, int, int, int]


@dataclass(frozen=True)
class _Subpath:
    points: tuple[_Point, ...]
    closed: bool


@dataclass(frozen=True)
class _PlacementTransform:
    scale_x: float
    scale_y: float
    translate_x: float
    translate_y: float
    clip: _Bounds

    def point(self, value: _Point) -> _Point:
        return (
            value[0] * self.scale_x + self.translate_x,
            value[1] * self.scale_y + self.translate_y,
        )

    @property
    def stroke_scale(self) -> float:
        return math.sqrt(abs(self.scale_x * self.scale_y))


@dataclass
class _Mask:
    bounds: _Bounds
    pixels: bytearray

    @classmethod
    def create(cls, bounds: _Bounds) -> "_Mask":
        left, top, right, bottom = bounds
        return cls(bounds, bytearray((right - left) * (bottom - top)))

    @property
    def width(self) -> int:
        return self.bounds[2] - self.bounds[0]

    def mark(self, x: int, y: int) -> None:
        left, top, right, bottom = self.bounds
        if left <= x < right and top <= y < bottom:
            self.pixels[(y - top) * self.width + x - left] = 255


@dataclass
class _Raster:
    width: int
    height: int
    pixels: bytearray

    @classmethod
    def create(cls, width: int, height: int, color: tuple[int, int, int]) -> "_Raster":
        row = bytes(color) * width
        return cls(width, height, bytearray(row * height))

    def composite(
        self,
        mask: _Mask,
        color: tuple[int, int, int, int],
        opacity: float,
    ) -> None:
        alpha = _multiply_alpha(color[3], opacity)
        if alpha == 0:
            return
        left, top, right, bottom = mask.bounds
        mask_width = right - left
        source_r, source_g, source_b, _ = color
        for local_y in range(bottom - top):
            mask_row = local_y * mask_width
            target_row = ((top + local_y) * self.width + left) * 3
            for local_x in range(mask_width):
                mask_alpha = mask.pixels[mask_row + local_x]
                if not mask_alpha:
                    continue
                pixel_alpha = (alpha * mask_alpha + 127) // 255
                offset = target_row + local_x * 3
                self.pixels[offset] = _blend(
                    source_r, self.pixels[offset], pixel_alpha
                )
                self.pixels[offset + 1] = _blend(
                    source_g, self.pixels[offset + 1], pixel_alpha
                )
                self.pixels[offset + 2] = _blend(
                    source_b, self.pixels[offset + 2], pixel_alpha
                )


def _apply_radial_falloff(mask: _Mask) -> None:
    """Maak een gevuld plaatsingsmasker zacht vanuit het centrum naar de rand."""

    left, top, right, bottom = mask.bounds
    center_x = (left + right) / 2
    center_y = (top + bottom) / 2
    radius_x = max(1.0, (right - left) / 2)
    radius_y = max(1.0, (bottom - top) / 2)
    for y in range(top, bottom):
        row = (y - top) * mask.width
        normalized_y = (y + 0.5 - center_y) / radius_y
        for x in range(left, right):
            offset = row + x - left
            if not mask.pixels[offset]:
                continue
            normalized_x = (x + 0.5 - center_x) / radius_x
            distance = math.sqrt(normalized_x ** 2 + normalized_y ** 2)
            strength = max(0.0, 1.0 - distance)
            mask.pixels[offset] = int(strength * strength * 255 + 0.5)


def _blend(source: int, target: int, alpha: int) -> int:
    return (source * alpha + target * (255 - alpha) + 127) // 255


def _multiply_alpha(alpha: int, opacity: float) -> int:
    opacity_alpha = max(0, min(255, int(opacity * 255 + 0.5)))
    return (alpha * opacity_alpha + 127) // 255


def _hex_color(value: str) -> tuple[int, int, int, int]:
    if not isinstance(value, str) or not value.startswith("#"):
        raise ValueError(f"Ongeldige hexkleur '{value}'")
    digits = value[1:]
    if len(digits) in {3, 4}:
        digits = "".join(character * 2 for character in digits)
    if len(digits) == 6:
        digits += "FF"
    if len(digits) != 8:
        raise ValueError(f"Ongeldige hexkleur '{value}'")
    try:
        channels = tuple(
            int(digits[index:index + 2], 16)
            for index in range(0, 8, 2)
        )
    except ValueError as exc:
        raise ValueError(f"Ongeldige hexkleur '{value}'") from exc
    return channels  # type: ignore[return-value]


def _paint(
    value: str,
    placement: ResolvedWallpaperAssetPlacement,
) -> tuple[int, int, int, int]:
    return _hex_color(
        placement.color.waarde if value == "currentColor" else value
    )


def _distance(first: _Point, second: _Point) -> float:
    return math.hypot(second[0] - first[0], second[1] - first[1])


def _curve_steps(points: Iterable[_Point], scale_hint: float) -> int:
    points = tuple(points)
    control_length = sum(
        _distance(first, second)
        for first, second in zip(points, points[1:])
    )
    return max(4, min(256, math.ceil(control_length * scale_hint / 6)))


def _cubic(
    start: _Point,
    control_one: _Point,
    control_two: _Point,
    end: _Point,
    scale_hint: float,
) -> tuple[_Point, ...]:
    steps = _curve_steps(
        (start, control_one, control_two, end),
        scale_hint,
    )
    points = []
    for step in range(1, steps + 1):
        t = step / steps
        inverse = 1 - t
        points.append((
            inverse ** 3 * start[0]
            + 3 * inverse ** 2 * t * control_one[0]
            + 3 * inverse * t ** 2 * control_two[0]
            + t ** 3 * end[0],
            inverse ** 3 * start[1]
            + 3 * inverse ** 2 * t * control_one[1]
            + 3 * inverse * t ** 2 * control_two[1]
            + t ** 3 * end[1],
        ))
    return tuple(points)


def _quadratic(
    start: _Point,
    control: _Point,
    end: _Point,
    scale_hint: float,
) -> tuple[_Point, ...]:
    steps = _curve_steps((start, control, end), scale_hint)
    points = []
    for step in range(1, steps + 1):
        t = step / steps
        inverse = 1 - t
        points.append((
            inverse ** 2 * start[0]
            + 2 * inverse * t * control[0]
            + t ** 2 * end[0],
            inverse ** 2 * start[1]
            + 2 * inverse * t * control[1]
            + t ** 2 * end[1],
        ))
    return tuple(points)


def _angle(first: _Point, second: _Point) -> float:
    cross = first[0] * second[1] - first[1] * second[0]
    dot = first[0] * second[0] + first[1] * second[1]
    return math.atan2(cross, dot)


def _arc(
    start: _Point,
    rx: float,
    ry: float,
    rotation: float,
    large_arc: float,
    sweep: float,
    end: _Point,
    scale_hint: float,
) -> tuple[_Point, ...]:
    rx = abs(rx)
    ry = abs(ry)
    if rx == 0 or ry == 0 or start == end:
        return (end,)

    phi = math.radians(rotation % 360)
    cosine = math.cos(phi)
    sine = math.sin(phi)
    half_x = (start[0] - end[0]) / 2
    half_y = (start[1] - end[1]) / 2
    prime_x = cosine * half_x + sine * half_y
    prime_y = -sine * half_x + cosine * half_y

    radius_ratio = (
        prime_x ** 2 / rx ** 2
        + prime_y ** 2 / ry ** 2
    )
    if radius_ratio > 1:
        factor = math.sqrt(radius_ratio)
        rx *= factor
        ry *= factor

    numerator = max(
        0.0,
        rx ** 2 * ry ** 2
        - rx ** 2 * prime_y ** 2
        - ry ** 2 * prime_x ** 2,
    )
    denominator = (
        rx ** 2 * prime_y ** 2
        + ry ** 2 * prime_x ** 2
    )
    center_factor = (
        0.0 if denominator == 0 else math.sqrt(numerator / denominator)
    )
    if bool(int(large_arc)) == bool(int(sweep)):
        center_factor *= -1
    center_prime_x = center_factor * (rx * prime_y / ry)
    center_prime_y = center_factor * (-ry * prime_x / rx)
    center_x = (
        cosine * center_prime_x
        - sine * center_prime_y
        + (start[0] + end[0]) / 2
    )
    center_y = (
        sine * center_prime_x
        + cosine * center_prime_y
        + (start[1] + end[1]) / 2
    )

    start_vector = (
        (prime_x - center_prime_x) / rx,
        (prime_y - center_prime_y) / ry,
    )
    end_vector = (
        (-prime_x - center_prime_x) / rx,
        (-prime_y - center_prime_y) / ry,
    )
    start_angle = _angle((1, 0), start_vector)
    delta = _angle(start_vector, end_vector)
    if not int(sweep) and delta > 0:
        delta -= 2 * math.pi
    elif int(sweep) and delta < 0:
        delta += 2 * math.pi

    approximate_length = max(rx, ry) * abs(delta)
    steps = max(
        4,
        min(256, math.ceil(approximate_length * scale_hint / 6)),
    )
    points = []
    for step in range(1, steps + 1):
        theta = start_angle + delta * step / steps
        points.append((
            center_x
            + cosine * rx * math.cos(theta)
            - sine * ry * math.sin(theta),
            center_y
            + sine * rx * math.cos(theta)
            + cosine * ry * math.sin(theta),
        ))
    points[-1] = end
    return tuple(points)


def _absolute(
    point: _Point,
    current: _Point,
    relative: bool,
) -> _Point:
    if not relative:
        return point
    return point[0] + current[0], point[1] + current[1]


def _parse_path(path: str, scale_hint: float) -> tuple[_Subpath, ...]:
    tokens = tuple(match.group(0) for match in _PATH_TOKEN.finditer(path))
    subpaths: list[_Subpath] = []
    points: list[_Point] = []
    current = (0.0, 0.0)
    start = current
    last_cubic: _Point | None = None
    last_quadratic: _Point | None = None
    index = 0

    def flush(closed: bool = False) -> None:
        nonlocal points
        if points:
            subpaths.append(_Subpath(tuple(points), closed))
            points = []

    while index < len(tokens):
        command = tokens[index]
        if command.upper() not in _ARITY:
            raise ValueError(f"SVG pad bevat onverwacht token '{command}'")
        index += 1
        upper = command.upper()
        relative = command.islower()
        arity = _ARITY[upper]
        values = []
        while index < len(tokens) and tokens[index].upper() not in _ARITY:
            values.append(float(tokens[index]))
            index += 1
        if arity == 0:
            flush(closed=True)
            current = start
            last_cubic = None
            last_quadratic = None
            continue
        if not values or len(values) % arity:
            raise ValueError(f"SVG commando '{command}' heeft ongeldige ariteit")

        groups = [
            values[offset:offset + arity]
            for offset in range(0, len(values), arity)
        ]
        for group_index, group in enumerate(groups):
            effective = upper
            if upper == "M" and group_index > 0:
                effective = "L"

            if effective == "M":
                flush()
                current = _absolute((group[0], group[1]), current, relative)
                start = current
                points = [current]
            else:
                if not points:
                    points = [current]

                if effective == "L":
                    current = _absolute(
                        (group[0], group[1]), current, relative
                    )
                    points.append(current)
                elif effective == "H":
                    x = group[0] + current[0] if relative else group[0]
                    current = (x, current[1])
                    points.append(current)
                elif effective == "V":
                    y = group[0] + current[1] if relative else group[0]
                    current = (current[0], y)
                    points.append(current)
                elif effective == "C":
                    control_one = _absolute(
                        (group[0], group[1]), current, relative
                    )
                    control_two = _absolute(
                        (group[2], group[3]), current, relative
                    )
                    end = _absolute(
                        (group[4], group[5]), current, relative
                    )
                    points.extend(_cubic(
                        current,
                        control_one,
                        control_two,
                        end,
                        scale_hint,
                    ))
                    current = end
                    last_cubic = control_two
                elif effective == "S":
                    control_one = (
                        (
                            2 * current[0] - last_cubic[0],
                            2 * current[1] - last_cubic[1],
                        )
                        if last_cubic is not None
                        else current
                    )
                    control_two = _absolute(
                        (group[0], group[1]), current, relative
                    )
                    end = _absolute(
                        (group[2], group[3]), current, relative
                    )
                    points.extend(_cubic(
                        current,
                        control_one,
                        control_two,
                        end,
                        scale_hint,
                    ))
                    current = end
                    last_cubic = control_two
                elif effective == "Q":
                    control = _absolute(
                        (group[0], group[1]), current, relative
                    )
                    end = _absolute(
                        (group[2], group[3]), current, relative
                    )
                    points.extend(_quadratic(
                        current,
                        control,
                        end,
                        scale_hint,
                    ))
                    current = end
                    last_quadratic = control
                elif effective == "T":
                    control = (
                        (
                            2 * current[0] - last_quadratic[0],
                            2 * current[1] - last_quadratic[1],
                        )
                        if last_quadratic is not None
                        else current
                    )
                    end = _absolute(
                        (group[0], group[1]), current, relative
                    )
                    points.extend(_quadratic(
                        current,
                        control,
                        end,
                        scale_hint,
                    ))
                    current = end
                    last_quadratic = control
                elif effective == "A":
                    end = _absolute(
                        (group[5], group[6]), current, relative
                    )
                    points.extend(_arc(
                        current,
                        group[0],
                        group[1],
                        group[2],
                        group[3],
                        group[4],
                        end,
                        scale_hint,
                    ))
                    current = end
                else:
                    raise ValueError(f"Onondersteund SVG commando '{command}'")

            if effective not in {"C", "S"}:
                last_cubic = None
            if effective not in {"Q", "T"}:
                last_quadratic = None
    flush()
    return tuple(subpaths)


def _placement_transform(
    placement: ResolvedWallpaperAssetPlacement,
    asset: ResolvedSvgAsset,
    canvas_width: int,
    canvas_height: int,
) -> _PlacementTransform:
    view_x, view_y, view_width, view_height = asset.viewbox
    scale_x = placement.breedte / view_width
    scale_y = placement.hoogte / view_height
    if placement.fit == "contain":
        scale_x = scale_y = min(scale_x, scale_y)
    elif placement.fit == "cover":
        scale_x = scale_y = max(scale_x, scale_y)
    elif placement.fit != "stretch":
        raise ValueError(
            f"Assetplaatsing '{placement.id}' heeft onbekende fit "
            f"'{placement.fit}'"
        )
    rendered_width = view_width * scale_x
    rendered_height = view_height * scale_y
    translate_x = (
        placement.x
        + (placement.breedte - rendered_width) / 2
        - view_x * scale_x
    )
    translate_y = (
        placement.y
        + (placement.hoogte - rendered_height) / 2
        - view_y * scale_y
    )
    clip = (
        max(0, placement.x),
        max(0, placement.y),
        min(canvas_width, placement.x + placement.breedte),
        min(canvas_height, placement.y + placement.hoogte),
    )
    return _PlacementTransform(
        scale_x,
        scale_y,
        translate_x,
        translate_y,
        clip,
    )


def _transformed_paths(
    asset: ResolvedSvgAsset,
    transform: _PlacementTransform,
) -> tuple[tuple[_Subpath, ...], ...]:
    scale_hint = max(abs(transform.scale_x), abs(transform.scale_y))
    return tuple(
        tuple(
            _Subpath(
                tuple(transform.point(point) for point in subpath.points),
                subpath.closed,
            )
            for subpath in _parse_path(path, scale_hint)
        )
        for path in asset.paden
    )


def _mark_interval(
    mask: _Mask,
    y: int,
    first: float,
    second: float,
) -> None:
    left = math.ceil(min(first, second) - 0.5)
    right = math.ceil(max(first, second) - 0.5)
    clip_left, _, clip_right, _ = mask.bounds
    for x in range(max(left, clip_left), min(right, clip_right)):
        mask.mark(x, y)


def _fill_subpaths(mask: _Mask, subpaths: Iterable[_Subpath]) -> None:
    edges: list[tuple[_Point, _Point]] = []
    for subpath in subpaths:
        if len(subpath.points) < 2:
            continue
        path_edges = list(zip(subpath.points, subpath.points[1:]))
        if subpath.points[-1] != subpath.points[0]:
            path_edges.append((subpath.points[-1], subpath.points[0]))
        edges.extend(path_edges)
    if not edges:
        return

    _, clip_top, _, clip_bottom = mask.bounds
    minimum_y = max(
        clip_top,
        math.floor(min(min(first[1], second[1]) for first, second in edges)),
    )
    maximum_y = min(
        clip_bottom,
        math.ceil(max(max(first[1], second[1]) for first, second in edges)),
    )
    for y in range(minimum_y, maximum_y):
        scan_y = y + 0.5
        events = []
        for first, second in edges:
            if first[1] == second[1]:
                continue
            lower = min(first[1], second[1])
            upper = max(first[1], second[1])
            if not lower <= scan_y < upper:
                continue
            ratio = (scan_y - first[1]) / (second[1] - first[1])
            events.append((
                first[0] + ratio * (second[0] - first[0]),
                1 if second[1] > first[1] else -1,
            ))
        events.sort(key=lambda event: event[0])
        winding = 0
        previous_x: float | None = None
        event_index = 0
        while event_index < len(events):
            x = events[event_index][0]
            if previous_x is not None and winding:
                _mark_interval(mask, y, previous_x, x)
            direction = 0
            while (
                event_index < len(events)
                and math.isclose(events[event_index][0], x, abs_tol=1e-9)
            ):
                direction += events[event_index][1]
                event_index += 1
            winding += direction
            previous_x = x


def _distance_to_segment(
    point: _Point,
    first: _Point,
    second: _Point,
    radius: float,
    cap: str,
) -> float:
    delta_x = second[0] - first[0]
    delta_y = second[1] - first[1]
    length_squared = delta_x ** 2 + delta_y ** 2
    if length_squared == 0:
        return _distance(point, first)
    projection = (
        (point[0] - first[0]) * delta_x
        + (point[1] - first[1]) * delta_y
    ) / length_squared
    lower = 0.0
    upper = 1.0
    if cap == "butt":
        if not lower <= projection <= upper:
            return math.inf
    if cap == "square":
        extension = radius / math.sqrt(length_squared)
        lower = -extension
        upper = 1 + extension
        if not lower <= projection <= upper:
            return math.inf
    projection = max(lower, min(upper, projection))
    nearest = (
        first[0] + projection * delta_x,
        first[1] + projection * delta_y,
    )
    return _distance(point, nearest)


def _stroke_segment(
    mask: _Mask,
    first: _Point,
    second: _Point,
    radius: float,
    cap: str,
) -> None:
    clip_left, clip_top, clip_right, clip_bottom = mask.bounds
    left = max(clip_left, math.floor(min(first[0], second[0]) - radius - 1))
    top = max(clip_top, math.floor(min(first[1], second[1]) - radius - 1))
    right = min(clip_right, math.ceil(max(first[0], second[0]) + radius + 1))
    bottom = min(clip_bottom, math.ceil(max(first[1], second[1]) + radius + 1))
    for y in range(top, bottom):
        for x in range(left, right):
            if _distance_to_segment(
                (x + 0.5, y + 0.5),
                first,
                second,
                radius,
                cap,
            ) <= radius:
                mask.mark(x, y)


def _mark_disk(mask: _Mask, center: _Point, radius: float) -> None:
    clip_left, clip_top, clip_right, clip_bottom = mask.bounds
    left = max(clip_left, math.floor(center[0] - radius - 1))
    top = max(clip_top, math.floor(center[1] - radius - 1))
    right = min(clip_right, math.ceil(center[0] + radius + 1))
    bottom = min(clip_bottom, math.ceil(center[1] + radius + 1))
    radius_squared = radius ** 2
    for y in range(top, bottom):
        for x in range(left, right):
            if (
                (x + 0.5 - center[0]) ** 2
                + (y + 0.5 - center[1]) ** 2
                <= radius_squared
            ):
                mask.mark(x, y)


def _fill_polygon(mask: _Mask, points: Iterable[_Point]) -> None:
    points = tuple(points)
    if len(points) >= 3:
        _fill_subpaths(mask, (_Subpath(points, True),))


def _line_intersection(
    first: _Point,
    first_direction: _Point,
    second: _Point,
    second_direction: _Point,
) -> _Point | None:
    determinant = (
        first_direction[0] * second_direction[1]
        - first_direction[1] * second_direction[0]
    )
    if abs(determinant) < 1e-9:
        return None
    delta = (second[0] - first[0], second[1] - first[1])
    factor = (
        delta[0] * second_direction[1]
        - delta[1] * second_direction[0]
    ) / determinant
    return (
        first[0] + factor * first_direction[0],
        first[1] + factor * first_direction[1],
    )


def _mark_join(
    mask: _Mask,
    previous: _Point,
    point: _Point,
    following: _Point,
    radius: float,
    join: str,
) -> None:
    if join == "round":
        _mark_disk(mask, point, radius)
        return
    incoming_length = _distance(previous, point)
    outgoing_length = _distance(point, following)
    if incoming_length == 0 or outgoing_length == 0:
        return
    incoming = (
        (point[0] - previous[0]) / incoming_length,
        (point[1] - previous[1]) / incoming_length,
    )
    outgoing = (
        (following[0] - point[0]) / outgoing_length,
        (following[1] - point[1]) / outgoing_length,
    )
    cross = incoming[0] * outgoing[1] - incoming[1] * outgoing[0]
    if abs(cross) < 1e-9:
        return
    side = -1 if cross > 0 else 1
    incoming_normal = (
        -incoming[1] * side,
        incoming[0] * side,
    )
    outgoing_normal = (
        -outgoing[1] * side,
        outgoing[0] * side,
    )
    first = (
        point[0] + incoming_normal[0] * radius,
        point[1] + incoming_normal[1] * radius,
    )
    second = (
        point[0] + outgoing_normal[0] * radius,
        point[1] + outgoing_normal[1] * radius,
    )
    if join == "miter":
        miter = _line_intersection(first, incoming, second, outgoing)
        if miter is not None and _distance(point, miter) <= radius * 4:
            _fill_polygon(mask, (first, miter, second))
            return
    _fill_polygon(mask, (point, first, second))


def _stroke_subpaths(
    mask: _Mask,
    subpaths: Iterable[_Subpath],
    width: float,
    cap: str,
    join: str,
) -> None:
    radius = width / 2
    if radius <= 0:
        return
    for subpath in subpaths:
        if len(subpath.points) < 2:
            continue
        segments = list(zip(subpath.points, subpath.points[1:]))
        if subpath.closed:
            segments.append((subpath.points[-1], subpath.points[0]))
        segment_cap = "butt" if subpath.closed else cap
        for first, second in segments:
            _stroke_segment(mask, first, second, radius, segment_cap)

        if subpath.closed:
            vertices = [
                (
                    subpath.points[index - 1],
                    subpath.points[index],
                    subpath.points[(index + 1) % len(subpath.points)],
                )
                for index in range(len(subpath.points))
            ]
        else:
            vertices = [
                (
                    subpath.points[index - 1],
                    subpath.points[index],
                    subpath.points[index + 1],
                )
                for index in range(1, len(subpath.points) - 1)
            ]
        for previous, point, following in vertices:
            _mark_join(mask, previous, point, following, radius, join)


def _render_placement(
    raster: _Raster,
    placement: ResolvedWallpaperAssetPlacement,
) -> None:
    asset = placement.asset
    transform = _placement_transform(
        placement,
        asset,
        raster.width,
        raster.height,
    )
    paths = _transformed_paths(asset, transform)

    if asset.vulling != "none":
        fill_mask = _Mask.create(transform.clip)
        for path in paths:
            _fill_subpaths(fill_mask, path)
        if placement.effect == "radial-glow":
            _apply_radial_falloff(fill_mask)
        elif placement.effect != "solid":
            raise ValueError(
                f"Wallpaperrenderer kan beeldeffect '{placement.effect}' niet "
                f"realiseren voor assetplaatsing '{placement.id}'; ondersteund "
                "zijn uitsluitend 'solid' en 'radial-glow'"
            )
        raster.composite(
            fill_mask,
            _paint(asset.vulling, placement),
            placement.dekking,
        )

    if asset.lijn != "none":
        if placement.effect != "solid":
            raise ValueError(
                f"Beeldeffect '{placement.effect}' vereist een gevuld asset"
            )
        if (
            asset.lijndikte is None
            or asset.lijneinde is None
            or asset.lijnverbinding is None
        ):
            raise ValueError(
                f"Wallpaperasset '{asset.id}' mist opgelost lijncontract"
            )
        stroke_mask = _Mask.create(transform.clip)
        for path in paths:
            _stroke_subpaths(
                stroke_mask,
                path,
                asset.lijndikte * transform.stroke_scale,
                asset.lijneinde,
                asset.lijnverbinding,
            )
        raster.composite(
            stroke_mask,
            _paint(asset.lijn, placement),
            placement.dekking,
        )


def _chunk(name: bytes, payload: bytes) -> bytes:
    checksum = binascii.crc32(name)
    checksum = binascii.crc32(payload, checksum) & 0xFFFFFFFF
    return (
        struct.pack(">I", len(payload))
        + name
        + payload
        + struct.pack(">I", checksum)
    )


def _color_key(pixels: bytearray, offset: int) -> int:
    return (
        pixels[offset] << 16
        | pixels[offset + 1] << 8
        | pixels[offset + 2]
    )


def _indexed_rows(
    raster: _Raster,
    palette: tuple[int, ...],
    bit_depth: int,
) -> bytes:
    indices = {color: index for index, color in enumerate(palette)}
    rows = bytearray()
    for y in range(raster.height):
        rows.append(0)
        accumulator = 0
        bits = 0
        row_offset = y * raster.width * 3
        for x in range(raster.width):
            color = _color_key(raster.pixels, row_offset + x * 3)
            accumulator = (accumulator << bit_depth) | indices[color]
            bits += bit_depth
            if bits == 8:
                rows.append(accumulator)
                accumulator = 0
                bits = 0
        if bits:
            rows.append(accumulator << (8 - bits))
    return bytes(rows)


def _truecolor_rows(raster: _Raster) -> bytes:
    rows = bytearray()
    row_length = raster.width * 3
    for y in range(raster.height):
        rows.append(0)
        start = y * row_length
        rows.extend(raster.pixels[start:start + row_length])
    return bytes(rows)


def _encode_png(
    raster: _Raster,
    metadata: tuple[tuple[str, str], ...],
) -> bytes:
    colors: set[int] = set()
    for offset in range(0, len(raster.pixels), 3):
        colors.add(_color_key(raster.pixels, offset))
        if len(colors) > 256:
            break

    chunks = []
    if len(colors) <= 256:
        palette = tuple(sorted(colors))
        if len(palette) <= 2:
            bit_depth = 1
        elif len(palette) <= 4:
            bit_depth = 2
        elif len(palette) <= 16:
            bit_depth = 4
        else:
            bit_depth = 8
        color_type = 3
        palette_payload = bytes(
            channel
            for color in palette
            for channel in (
                color >> 16,
                (color >> 8) & 0xFF,
                color & 0xFF,
            )
        )
        image_rows = _indexed_rows(raster, palette, bit_depth)
    else:
        bit_depth = 8
        color_type = 2
        palette_payload = b""
        image_rows = _truecolor_rows(raster)

    header = struct.pack(
        ">IIBBBBB",
        raster.width,
        raster.height,
        bit_depth,
        color_type,
        0,
        0,
        0,
    )
    chunks.append(_chunk(b"IHDR", header))
    for key, value in metadata:
        chunks.append(_chunk(
            b"tEXt",
            key.encode("latin-1") + b"\x00" + value.encode("latin-1"),
        ))
    if palette_payload:
        chunks.append(_chunk(b"PLTE", palette_payload))
    chunks.append(_chunk(b"IDAT", zlib.compress(image_rows, level=9)))
    chunks.append(_chunk(b"IEND", b""))
    return PNG_SIGNATURE + b"".join(chunks)


@lru_cache(maxsize=8)
def render_wallpaper_png(
    wallpaper: ResolvedWallpaper,
    snapshot_ref: str,
    product_id: str,
) -> bytes:
    """Render één volledig opgeloste wallpaper tot een deterministische PNG."""

    if wallpaper.formaat != "png":
        raise ValueError(
            f"Wallpaperrenderer ondersteunt formaat '{wallpaper.formaat}' niet"
        )
    canvas = _hex_color(wallpaper.canvas.waarde)
    if canvas[3] != 255:
        raise ValueError(
            f"Wallpaper '{wallpaper.id}' vereist een ondoorzichtig canvas"
        )
    raster = _Raster.create(
        wallpaper.breedte,
        wallpaper.hoogte,
        canvas[:3],
    )
    for layer in wallpaper.lagen:
        for placement in layer.plaatsingen:
            _render_placement(raster, placement)
    metadata = [
        ("bp-product", product_id),
        ("bp-wallpaper", wallpaper.id),
    ]
    if wallpaper.familie:
        metadata.extend((
            ("bp-wallpaper-family", wallpaper.familie),
            ("bp-wallpaper-variant", wallpaper.variant),
        ))
    metadata.append(("bp-snapshot", snapshot_ref))
    return _encode_png(raster, tuple(metadata))
