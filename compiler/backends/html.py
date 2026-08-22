"""HTML-backendplugin voor native, theme-driven producten."""
from __future__ import annotations

from collections.abc import Iterable

from compiler.backend import Backend
from compiler.cir import Architectuurobject
from compiler.design_system_html_renderer import (
    reference_content_lines,
    reference_css_lines,
)
from compiler.component_html_renderer import render_component_example
from compiler.design_components import verzamel_componenten
from compiler.design_variants import resolveer_varianten
from compiler.native_layout_html_renderer import naar_native_layout_html
from compiler.product_model import ProductDefinition
from compiler.project_status import ProjectStatus
from compiler.svg_asset_catalog import SVG_ASSET_CATALOG_CONTENT
from compiler.svg_asset_catalog_html_renderer import (
    asset_catalog_content_lines,
    asset_catalog_css_lines,
)
from compiler.theme_css import theme_variable_lines


def _theme_css(product: ProductDefinition) -> str:
    thema = product.thema
    if thema is None:
        return ""

    regels = list(theme_variable_lines(thema, indent="    "))
    regels.extend([
        "    body {",
        "      margin: 0;",
        "      min-height: 100vh;",
        "      padding: var(--bp-spacing-xl);",
        "      box-sizing: border-box;",
        "      background: var(--bp-theme-background);",
        "      color: var(--bp-theme-foreground);",
        "      font-family: var(--bp-font-body);",
        "    }",
        "    h1, h2, h3, h4, h5, h6 { font-family: var(--bp-font-heading); }",
        "    code, pre, kbd, samp { font-family: var(--bp-font-mono); }",
        "    .bp-product-header {",
        "      max-width: 72rem;",
        "      margin-bottom: var(--bp-spacing-xl);",
        "      padding: var(--bp-spacing-large);",
        "      box-sizing: border-box;",
        "      background: var(--bp-material-surface);",
        "      border-left: var(--bp-border-strong) var(--bp-border-style) var(--bp-material-accent);",
        "      border-radius: var(--bp-radius-medium);",
        "    }",
        "    .bp-product-header h1 {",
        "      margin: 0;",
        "      font-size: var(--bp-type-title);",
        "    }",
        "    .bp-layout { gap: var(--bp-spacing-medium); }",
        "    .bp-region { padding: var(--bp-spacing-large); }",
        "    .bp-region h2 { margin-top: 0; }",
        "    @media (max-width: 960px) {",
        "      body { padding: var(--bp-spacing-large); }",
        "    }",
    ])

    if thema.artdirection is not None:
        art = thema.artdirection
        regels.extend([
            "    body {",
            "      background:",
            "        radial-gradient(circle at 12% 0%, color-mix(in srgb, var(--bp-art-interaction) 8%, transparent), transparent 38%),",
            "        radial-gradient(circle at 88% 100%, color-mix(in srgb, var(--bp-art-warm-accent) 6%, transparent), transparent 34%),",
            "        var(--bp-art-canvas);",
            "    }",
            "    .bp-product-header {",
            "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
            "      border-left-color: var(--bp-material-outline);",
            "    }",
            "    .bp-product-header::after {",
            "      content: \"\";",
            "      display: block;",
            "      height: var(--bp-border-hairline);",
            "      margin-top: var(--bp-spacing-medium);",
            "      background: linear-gradient(90deg, var(--bp-material-outline), transparent);",
            "    }",
            "    @media (prefers-reduced-motion: reduce) {",
            "      .bp-region { transition: none; }",
            "    }",
        ])

    if thema.materiaal is not None:
        regels.append("    .bp-canvas { background: var(--bp-material-canvas); }")
    if all((thema.materiaal, thema.border, thema.radius, thema.shadow, thema.motion)):
        regels.extend([
            "    .bp-region {",
            "      background: var(--bp-material-raised);",
            "      color: var(--bp-material-foreground);",
            "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
            "      border-radius: var(--bp-radius-medium);",
            "      box-shadow: var(--bp-shadow-low);",
            "      transition: box-shadow var(--bp-motion-normal) var(--bp-motion-easing);",
            "    }",
            "    .bp-metric {",
            "      margin: var(--bp-spacing-small) 0;",
            "      color: var(--bp-material-accent);",
            "      font-family: var(--bp-font-heading);",
            "      font-size: calc(var(--bp-type-heading) * 2);",
            "      font-weight: 700;",
            "      line-height: 1;",
            "    }",
            "    .bp-description {",
            "      margin: var(--bp-spacing-small) 0 0;",
            "      color: var(--bp-material-muted);",
            "      font-size: var(--bp-type-body);",
            "    }",
            "    .bp-metric-details {",
            "      display: grid;",
            "      gap: var(--bp-spacing-xs);",
            "      margin: var(--bp-spacing-small) 0;",
            "      padding: 0;",
            "      list-style: none;",
            "      color: var(--bp-material-muted);",
            "      font-size: var(--bp-type-caption);",
            "    }",
            "    .bp-metric-details li {",
            "      display: flex;",
            "      justify-content: space-between;",
            "      gap: var(--bp-spacing-small);",
            "      border-bottom: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
            "    }",
            "    .bp-metric-detail-value {",
            "      color: var(--bp-material-foreground);",
            "      font-weight: 700;",
            "    }",
            "    .bp-status-summary {",
            "      display: grid;",
            "      grid-template-columns: minmax(12rem, 18rem) 1fr;",
            "      gap: var(--bp-spacing-large);",
            "      margin-bottom: var(--bp-spacing-large);",
            "    }",
            "    .bp-status-overall {",
            "      padding: var(--bp-spacing-large);",
            "      background: var(--bp-material-raised);",
            "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
            "      border-radius: var(--bp-radius-medium);",
            "    }",
            "    .bp-status-overall strong {",
            "      color: var(--bp-material-accent);",
            "      font-family: var(--bp-font-heading);",
            "      font-size: var(--bp-type-display);",
            "    }",
            "    .bp-status-milestones, .bp-status-areas {",
            "      display: grid;",
            "      gap: var(--bp-spacing-medium);",
            "    }",
            "    .bp-status-milestones { grid-template-columns: repeat(3, minmax(0, 1fr)); }",
            "    .bp-status-areas { grid-template-columns: repeat(2, minmax(0, 1fr)); }",
            "    .bp-status-card {",
            "      padding: var(--bp-spacing-large);",
            "      background: var(--bp-material-raised);",
            "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
            "      border-radius: var(--bp-radius-medium);",
            "    }",
            "    .bp-status-card h2, .bp-status-card h3 { margin-top: 0; }",
            "    .bp-status-progress {",
            "      width: 100%;",
            "      accent-color: var(--bp-material-accent);",
            "    }",
            "    .bp-status-label { color: var(--bp-material-muted); }",
            "    @media (max-width: 960px) {",
            "      .bp-status-summary, .bp-status-milestones, .bp-status-areas { grid-template-columns: 1fr; }",
            "    }",
        ])

    if product.inhoud == "design-system":
        regels.extend(reference_css_lines())
    if product.inhoud == SVG_ASSET_CATALOG_CONTENT:
        regels.extend(asset_catalog_css_lines())

    return "\n".join(regels) + "\n"


def _status_html(status: ProjectStatus) -> str:
    import html

    verification = status.current_milestone.verification
    verification_detail = f"Verificatie: {verification.state}"
    if verification.state == "geverifieerd":
        verification_detail += f" ({verification.actor}, {verification.date})"
    milestone_cards = (
        (
            "Laatst voltooid",
            f"{status.last_completed_milestone.id} — "
            f"{status.last_completed_milestone.name}",
            f"PR #{status.last_completed_milestone.pull_request}",
            None,
        ),
        (
            "Actueel",
            f"{status.current_milestone.id} — {status.current_milestone.name}",
            status.current_milestone.state,
            (verification.state, verification_detail),
        ),
        (
            "Volgende stap",
            f"{status.next_step.id} — {status.next_step.name}",
            status.next_step.purpose,
            None,
        ),
    )
    regels = [
        f'  <main class="bp-status" data-status-schema="{status.schema_version}">',
        '    <section class="bp-status-summary">',
        '      <div class="bp-status-overall">',
        '        <span class="bp-status-label">Totale voortgang</span>',
        f"        <strong>{status.overall_progress}%</strong>",
        f"        <p>{html.escape(status.overall_method)}</p>",
        "      </div>",
        '      <div class="bp-status-milestones">',
    ]
    for label, title, detail, verification_info in milestone_cards:
        attr = ""
        extra = []
        if verification_info is not None:
            state, verification_text = verification_info
            attr = f' data-verification="{html.escape(state)}"'
            extra.append(f"          <p>{html.escape(verification_text)}</p>")
        regels.extend([
            f'        <article class="bp-status-card"{attr}>',
            f'          <span class="bp-status-label">{html.escape(label)}</span>',
            f"          <h2>{html.escape(title)}</h2>",
            f"          <p>{html.escape(detail)}</p>",
            *extra,
            "        </article>",
        ])
    regels.extend([
        "      </div>",
        "    </section>",
        '    <section class="bp-status-areas" aria-label="Productgebieden">',
    ])
    for area in status.areas:
        regels.extend([
            f'      <article class="bp-status-card" data-status-area="{html.escape(area.id)}">',
            f"        <h3>{html.escape(area.name)}</h3>",
            f'        <progress class="bp-status-progress" max="100" value="{area.progress}">{area.progress}%</progress>',
            f"        <p><strong>{area.progress}%</strong></p>",
            f"        <p>{html.escape(area.evidence)}</p>",
            f'        <p class="bp-status-label">{html.escape(area.remaining)}</p>',
            "      </article>",
        ])
    regels.extend(["    </section>", "  </main>"])
    return "\n".join(regels)


def _render(
    objecten: Iterable[Architectuurobject],
    product: ProductDefinition,
) -> str:
    if product.opgeloste_layout is None:
        raise ValueError(
            f"Product '{product.id}' vereist een opgeloste native layout"
        )
    if product.opgeloste_compositie is None:
        raise ValueError(
            f"Product '{product.id}' vereist een opgeloste native compositie"
        )
    instance_content = None
    example_instances = tuple(
        instance
        for instance in product.opgeloste_compositie.instances
        if instance.example is not None
    )
    if example_instances:
        components = {
            component.id: component
            for component in verzamel_componenten(objecten)
        }
        variants = {
            variant.id: variant
            for variant in resolveer_varianten(objecten)
        }
        instance_content = {}
        for instance in example_instances:
            example = instance.example
            assert example is not None
            variant = variants[example.variant_id]
            appearance_id = variant.appearance_for_state("rest")
            assert appearance_id is not None
            instance_content[instance.id] = tuple(
                render_component_example(
                    components[example.component_id],
                    variant,
                    example,
                    "rest",
                    appearance_id,
                    heading_level=3,
                    id_namespace=instance.id,
                    include_context=False,
                )
            )
    if product.inhoud == "design-system":
        if product.design_system_reference is None:
            raise ValueError(
                f"Product '{product.id}' vereist een opgeloste "
                "designsystemreferentie"
            )
        if product.thema is None:
            raise ValueError(
                f"Product '{product.id}' vereist een opgelost native thema"
            )
        if len(product.opgeloste_compositie.instances) != 1:
            raise ValueError(
                f"Product '{product.id}' vereist exact één inhoudsinstantie"
            )
        instance_id = product.opgeloste_compositie.instances[0].id
        instance_content = {
            instance_id: reference_content_lines(
                product.design_system_reference,
                product.thema,
            )
        }
    if product.inhoud == SVG_ASSET_CATALOG_CONTENT:
        if product.asset_catalog is None:
            raise ValueError(
                f"Product '{product.id}' vereist een opgeloste "
                "SVG assetcatalogus"
            )
        if len(product.opgeloste_compositie.instances) != 1:
            raise ValueError(
                f"Product '{product.id}' vereist exact één inhoudsinstantie"
            )
        if not product.snapshot_ref:
            raise ValueError(
                f"Product '{product.id}' vereist statische snapshotidentiteit"
            )
        instance_id = product.opgeloste_compositie.instances[0].id
        instance_content = {
            instance_id: asset_catalog_content_lines(
                product.asset_catalog,
                catalog_path=product.pad,
                snapshot_ref=product.snapshot_ref,
            )
        }
    inhoud = naar_native_layout_html(
        product.opgeloste_compositie,
        product.opgeloste_layout,
        titel=product.naam,
        inhoud_naam=(
            product.naam
            if product.inhoud
            in {
                "project-status",
                "design-system",
                SVG_ASSET_CATALOG_CONTENT,
            }
            else None
        ),
        instance_content=instance_content,
    )
    if product.inhoud == "project-status":
        if product.project_status is None:
            raise ValueError(
                f"Product '{product.id}' vereist projectstatuscontext"
            )
        begin = inhoud.index('  <main class="bp-layout')
        einde = inhoud.index("  </main>", begin) + len("  </main>")
        inhoud = inhoud[:begin] + _status_html(product.project_status) + inhoud[einde:]
    if product.thema is None:
        return inhoud

    thema = product.thema
    snapshot_attribuut = (
        f' data-snapshot-id="{product.snapshot_id}"'
        f' data-snapshot-ref="{product.snapshot_ref}"'
        if product.snapshot_id
        else ""
    )
    inhoud = inhoud.replace("  <style>\n", "  <style>\n" + _theme_css(product), 1)
    inhoud = inhoud.replace(
        "<body>",
        f'<body data-world="{thema.wereld_id}" data-theme="{thema.thema_id}" '
        f'data-typography="{thema.typografie.id}" '
        f'data-font-delivery="{thema.typografie.levering}" '
        f'data-product-mode="{product.mode}" '
        f'data-product-content="{product.inhoud}" '
        f'data-time-context="{"applicable" if product.has_time_context else "none"}"'
        f"{snapshot_attribuut}>",
        1,
    )
    if thema.artdirection is not None:
        art = thema.artdirection
        inhoud = inhoud.replace(
            f'data-theme="{thema.thema_id}" ',
            f'data-theme="{thema.thema_id}" '
            f'data-art-direction="{art.id}" '
            f'data-art-glow="{art.glow}" '
            f'data-art-ornament="{art.ornament}" '
            f'data-art-density="{art.density}" '
            f'data-art-imagery="{art.imagery}" '
            f'data-art-warm-accent-limit="{art.warm_accent_limit}" ',
            1,
        )
    return inhoud


backend = Backend("html", _render)
