"""SVG-renderer voor Beckeringh Palace-composities."""
from __future__ import annotations

import html
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_compositions import verzamel_composities


def naar_compositie_svg(objecten: Iterable[Architectuurobject]) -> str:
    composities = verzamel_composities(objecten)
    regels = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675">',
        '  <style>.title{font:700 32px Aptos,sans-serif}.label{font:600 18px Aptos,sans-serif}</style>',
    ]
    y = 60
    for compositie in composities:
        regels.append(f'  <text class="title" x="60" y="{y}">{html.escape(compositie.naam)}</text>')
        y += 40
        for index, component_id in enumerate(compositie.componenten):
            x = 60 + (index * 280 if compositie.richting == "row" else 0)
            component_y = y if compositie.richting == "row" else y + index * 130
            regels.append(
                f'  <g data-component="{html.escape(component_id)}">'
                f'<rect x="{x}" y="{component_y}" width="240" height="100" rx="12" '
                'fill="var(--bp-color-iron, #171A1F)" stroke="var(--bp-color-accent, #D86A35)"/>'
                f'<text class="label" x="{x + 20}" y="{component_y + 58}" '
                'fill="var(--bp-color-smoke, #ECECEC)">'
                f'{html.escape(component_id)}</text></g>'
            )
        y += 180 if compositie.richting == "row" else len(compositie.componenten) * 130 + 40
    regels.extend(["</svg>", ""])
    return "\n".join(regels)
