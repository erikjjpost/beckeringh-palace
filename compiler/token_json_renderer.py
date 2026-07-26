"""Platformneutrale JSON-renderer voor Beckeringh Palace design tokens."""
from __future__ import annotations

import json
from collections.abc import Iterable

from compiler.cir import Architectuurobject
from compiler.design_tokens import verzamel_tokens


def naar_token_json(objecten: Iterable[Architectuurobject]) -> str:
    """Render gevalideerde tokens deterministisch naar een portable JSON-document."""

    gegevens = {
        token.id: {
            "type": token.type.value,
            "value": token.waarde,
            "description": token.doel,
        }
        for token in verzamel_tokens(objecten)
    }
    return json.dumps(gegevens, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
