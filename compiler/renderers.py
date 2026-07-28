"""Renderers die uitsluitend de canonieke tussenrepresentatie lezen."""
from __future__ import annotations

import json
from collections.abc import Iterable

from compiler.cir import Architectuurobject


def naar_json(objecten: Iterable[Architectuurobject]) -> str:
    gegevens = [obj.als_dict() for obj in objecten]
    return json.dumps(gegevens, ensure_ascii=False, indent=2, sort_keys=True)


def naar_markdown(objecten: Iterable[Architectuurobject]) -> str:
    objecten = tuple(objecten)
    symbolen = {obj.id: obj for obj in objecten}
    delen = ["# Beckeringh Architectuurmodel", ""]
    for obj in objecten:
        eigenschappen = obj.eigenschappen
        bron = eigenschappen
        homepagegebied = eigenschappen.get("homepagegebied")
        if (
            obj.soort == "componentinstantie"
            and isinstance(homepagegebied, str)
            and homepagegebied in symbolen
        ):
            bron = symbolen[homepagegebied].eigenschappen
        delen.extend([
            f"## {bron['naam']}",
            "",
            f"**Soort:** {obj.soort}",
            "",
            f"**Identifier:** `{obj.id}`",
            "",
            "### Doel",
            "",
            str(bron["doel"]),
            "",
        ])
        overige = {k: v for k, v in eigenschappen.items() if k not in {"naam", "doel"}}
        if overige:
            delen.extend(["### Eigenschappen", ""])
            for naam, waarde in sorted(overige.items()):
                getoond = ", ".join(map(str, waarde)) if isinstance(waarde, list) else str(waarde)
                delen.append(f"- **{naam}:** {getoond}")
            delen.append("")
    return "\n".join(delen).rstrip("\n")
