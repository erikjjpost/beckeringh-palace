"""Canonieke rendererbindingen voor Beckeringh Palace-renderdoelen."""
from __future__ import annotations

from compiler.component_css_renderer import naar_component_css
from compiler.css_renderer import naar_css
from compiler.render_target_renderer import RenderTargetRendererRegistry
from compiler.terminal_theme_renderer import naar_dircolors, naar_ps1
from compiler.token_json_renderer import naar_token_json


def standaard_render_target_registry() -> RenderTargetRendererRegistry:
    return RenderTargetRendererRegistry(
        {
            "css-components": naar_component_css,
            "css-tokens": naar_css,
            "json-tokens": naar_token_json,
            "emberforge-dircolors": naar_dircolors,
            "emberforge-ps1": naar_ps1,
        }
    )
