"""Expliciete rendererbinding en generatie voor native renderdoelen."""
from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass

from compiler.cir import Architectuurobject
from compiler.design_render_targets import ResolvedRenderTarget, resolveer_renderdoelen

RenderTargetRenderer = Callable[[Iterable[Architectuurobject]], str]


@dataclass(frozen=True)
class RenderedTarget:
    definitie: ResolvedRenderTarget
    inhoud: str


class RenderTargetRendererRegistry:
    def __init__(self, renderers: Mapping[str, RenderTargetRenderer]) -> None:
        self._renderers = dict(renderers)

    def resolveer(self, renderdoel_id: str) -> RenderTargetRenderer:
        try:
            return self._renderers[renderdoel_id]
        except KeyError as exc:
            raise KeyError(
                f"Renderdoel '{renderdoel_id}' heeft geen geregistreerde renderer"
            ) from exc


def render_renderdoelen(
    objecten: Iterable[Architectuurobject],
    registry: RenderTargetRendererRegistry,
) -> tuple[RenderedTarget, ...]:
    objecten = tuple(objecten)
    return tuple(
        RenderedTarget(
            definitie=renderdoel,
            inhoud=registry.resolveer(renderdoel.id)(objecten),
        )
        for renderdoel in resolveer_renderdoelen(objecten)
    )
