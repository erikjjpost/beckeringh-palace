"""HTML-catalogusrenderer voor Beckeringh Palace-componenten."""
from __future__ import annotations

import html

from compiler.component_accessibility import ResolvedComponentAccessibility
from compiler.component_css_identity import (
    componentklasse,
    stateklasse,
    variantklasse,
)
from compiler.component_examples import (
    ResolvedComponentExample,
)
from compiler.design_components import DesignComponent
from compiler.design_variants import ResolvedComponentVariant


def accessibility_attributes(
    contract: ResolvedComponentAccessibility | None,
) -> str:
    if contract is None:
        return ""
    attributen = [
        ("data-accessibility-contract", contract.contract_id),
        ("data-accessibility-role", contract.rol),
        ("data-accessibility-name-source", contract.naambron),
    ]
    if contract.waardebron is not None:
        attributen.append(
            ("data-accessibility-value-source", contract.waardebron)
        )
    if contract.foutbron is not None:
        attributen.append(
            ("data-accessibility-error-source", contract.foutbron)
        )
    attributen.extend([
        ("data-accessibility-disabled", contract.disabled_gedrag),
        ("data-accessibility-focus", contract.focusgedrag),
        ("data-accessibility-keyboard", contract.toetsenbordgedrag),
    ])
    if contract.toetsen:
        attributen.append(
            ("data-accessibility-keys", " ".join(contract.toetsen))
        )
    return " " + " ".join(
        f'{naam}="{html.escape(waarde)}"'
        for naam, waarde in attributen
    )


def _voorbeeld_element_id(
    example: ResolvedComponentExample,
    state: str,
    deel: str,
    id_namespace: str,
) -> str:
    namespace = f"{id_namespace}-" if id_namespace else ""
    return f"bp-example-{namespace}{example.id}-{state}-{deel}"


def _voorbeeld_attributen(
    component: DesignComponent,
    variant: ResolvedComponentVariant,
    example: ResolvedComponentExample,
    state: str,
    appearance_id: str,
) -> str:
    state_class = f" {stateklasse(state)}" if state != "rest" else ""
    state_names = " ".join(
        state_name for state_name, _ in variant.state_appearances
    )
    return (
        f'class="{componentklasse(component.id)} '
        f'{variantklasse(variant.id)}{state_class}" '
        f'data-example="{html.escape(example.id)}" '
        f'data-component="{html.escape(component.id)}" '
        f'data-component-role="{html.escape(example.component_role)}" '
        f'data-component-anatomy="'
        f'{html.escape(" ".join(example.component_anatomy))}" '
        f'data-variant="{html.escape(variant.id)}" '
        f'data-component-state="{html.escape(state)}" '
        f'data-component-states="{html.escape(state_names)}" '
        f'data-appearance="{html.escape(appearance_id)}"'
        f"{accessibility_attributes(example.accessibility)}"
    )


def render_component_example(
    component: DesignComponent,
    variant: ResolvedComponentVariant,
    example: ResolvedComponentExample,
    state: str,
    appearance_id: str,
    heading_level: int = 2,
    id_namespace: str = "",
) -> list[str]:
    if heading_level not in range(2, 7):
        raise ValueError("Componentvoorbeeld vereist headingniveau 2 tot en met 6")
    attributen = _voorbeeld_attributen(
        component,
        variant,
        example,
        state,
        appearance_id,
    )
    titel = (
        example.naam
        if state == "rest"
        else f"{example.naam} · {state}"
    )
    regels = [
        '    <section class="bp-component-example-shell">',
        f"      <h{heading_level}>{html.escape(titel)}</h{heading_level}>",
        f"      <p>{html.escape(example.doel)}</p>",
    ]
    disabled = state == "disabled"
    if example.component_role == "actie":
        disabled_attribute = (
            " disabled"
            if (
                disabled
                and example.accessibility is not None
                and example.accessibility.disabled_gedrag == "native"
            )
            else ""
        )
        regels.append(
            f'      <button type="button" {attributen}'
            f"{disabled_attribute}>"
            f"{html.escape(example.label)}</button>"
        )
    elif example.component_role == "invoer":
        control_id = _voorbeeld_element_id(
            example, state, "control", id_namespace
        )
        label_id = _voorbeeld_element_id(
            example, state, "label", id_namespace
        )
        message_id = _voorbeeld_element_id(
            example, state, "message", id_namespace
        )
        disabled_attribute = (
            " disabled"
            if (
                disabled
                and example.accessibility is not None
                and example.accessibility.disabled_gedrag == "native"
            )
            else ""
        )
        error_attributes = (
            f' aria-invalid="true" '
            f'aria-describedby="{html.escape(message_id)}" '
            f'aria-errormessage="{html.escape(message_id)}"'
            if example.melding is not None
            else ""
        )
        regels.extend([
            (
                '      <div class="bp-component-example bp-example-input">'
            ),
            (
                f'        <label id="{html.escape(label_id)}" '
                f'for="{html.escape(control_id)}" '
                f'class="bp-example-label">'
                f"{html.escape(example.label)}</label>"
            ),
            (
                f'        <input id="{html.escape(control_id)}" '
                f"{attributen} "
                f'value="{html.escape(example.waarde or "")}"'
                f"{error_attributes}{disabled_attribute}>"
            ),
        ])
        if example.melding is not None:
            regels.append(
                f'        <small id="{html.escape(message_id)}" '
                'class="bp-example-message">'
                f"{html.escape(example.melding)}</small>"
            )
        regels.append("      </div>")
    elif example.component_role == "status":
        label_id = _voorbeeld_element_id(
            example, state, "label", id_namespace
        )
        regels.append(
            f'      <output {attributen} '
            f'aria-labelledby="{html.escape(label_id)}">'
            f'<span id="{html.escape(label_id)}">'
            f"{html.escape(example.label)}</span> · "
            f"<span>{html.escape(example.waarde or '')}</span></output>"
        )
    elif example.component_role == "app-tegel":
        label_id = _voorbeeld_element_id(
            example, state, "label", id_namespace
        )
        description_id = _voorbeeld_element_id(
            example, state, "description", id_namespace
        )
        status_id = _voorbeeld_element_id(
            example, state, "status", id_namespace
        )
        disabled_attribute = (
            " disabled"
            if (
                disabled
                and example.accessibility is not None
                and example.accessibility.disabled_gedrag == "native"
            )
            else ""
        )
        regels.extend([
            f'      <button type="button" {attributen} '
            f'aria-labelledby="{html.escape(label_id)}" '
            f'aria-describedby="{html.escape(description_id)} '
            f'{html.escape(status_id)}"{disabled_attribute}>',
            (
                f'        <strong id="{html.escape(label_id)}">'
                f"{html.escape(example.label)}</strong>"
            ),
            (
                f'        <span id="{html.escape(description_id)}" '
                'class="bp-example-description">'
                f"{html.escape(example.beschrijving or '')}</span>"
            ),
            (
                f'        <small id="{html.escape(status_id)}">'
                f"{html.escape(example.status or '')}</small>"
            ),
            "      </button>",
        ])
    elif example.component_role == "statistiek":
        label_id = _voorbeeld_element_id(
            example, state, "label", id_namespace
        )
        regels.extend([
            (
                f"      <article {attributen} "
                f'aria-labelledby="{html.escape(label_id)}">'
            ),
            f'        <small id="{html.escape(label_id)}">'
            f"{html.escape(example.label)}</small>",
            f"        <strong>{html.escape(example.waarde or '')}</strong>",
        ])
        if example.beschrijving is not None:
            regels.append(
                f"        <p>{html.escape(example.beschrijving)}</p>"
            )
        regels.append("      </article>")
    else:
        regels.extend([
            f"      <section {attributen}>",
            f"        <h3>{html.escape(example.label)}</h3>",
            "      </section>",
        ])
    regels.append("    </section>")
    return regels
