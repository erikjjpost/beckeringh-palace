"""HTML-weergave van een vooraf opgeloste SVG assetcatalogus."""
from __future__ import annotations

import html
import posixpath
from pathlib import PurePosixPath

from compiler.svg_asset_catalog import ResolvedSvgAssetCatalog
from compiler.svg_serialization import svg_element_lines


def asset_catalog_css_lines() -> tuple[str, ...]:
    return (
        "    .bp-asset-catalog {",
        "      display: grid;",
        "      grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));",
        "      gap: var(--bp-spacing-large);",
        "    }",
        "    .bp-asset-card {",
        "      display: grid;",
        "      gap: var(--bp-spacing-medium);",
        "      padding: var(--bp-spacing-large);",
        "      background: var(--bp-material-surface);",
        "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "      border-radius: var(--bp-radius-medium);",
        "    }",
        "    .bp-asset-preview {",
        "      display: grid;",
        "      min-height: 12rem;",
        "      place-items: center;",
        "      color: var(--bp-material-accent);",
        "      background: var(--bp-material-canvas);",
        "      border: var(--bp-border-hairline) var(--bp-border-style) var(--bp-material-outline);",
        "      border-radius: var(--bp-radius-small);",
        "    }",
        "    .bp-asset-preview svg {",
        "      width: min(100%, 10rem);",
        "      height: auto;",
        "      overflow: visible;",
        "    }",
        "    .bp-asset-card h3, .bp-asset-card p { margin: 0; }",
        "    .bp-asset-contract {",
        "      display: grid;",
        "      grid-template-columns: max-content 1fr;",
        "      gap: var(--bp-spacing-xs) var(--bp-spacing-medium);",
        "      margin: 0;",
        "      font-size: var(--bp-type-caption);",
        "    }",
        "    .bp-asset-contract dt { color: var(--bp-material-muted); }",
        "    .bp-asset-contract dd {",
        "      margin: 0;",
        "      overflow-wrap: anywhere;",
        "    }",
        "    .bp-asset-link {",
        "      color: var(--bp-theme-accent);",
        "      font-weight: 700;",
        "    }",
    )


def _artifact_href(catalog_path: str, artifact_path: str) -> str:
    bronmap = str(PurePosixPath(catalog_path).parent)
    return posixpath.relpath(artifact_path, start=bronmap)


def asset_catalog_content_lines(
    catalog: ResolvedSvgAssetCatalog,
    *,
    catalog_path: str,
    snapshot_ref: str,
) -> tuple[str, ...]:
    regels = [
        (
            '<div class="bp-asset-catalog" '
            f'data-asset-count="{len(catalog.entries)}">'
        )
    ]
    for entry in catalog.entries:
        asset = entry.asset
        heading_id = f"bp-asset-{asset.id}-title"
        artifact_href = _artifact_href(
            catalog_path,
            entry.artifact_path,
        )
        familie_attributen = (
            f'data-asset-family="{html.escape(asset.familie)}" '
            f'data-asset-variant="{html.escape(asset.variant)}" '
            if asset.familie is not None and asset.variant is not None
            else ""
        )
        regels.extend([
            (
                f'  <article class="bp-asset-card" '
                f'data-asset="{html.escape(asset.id)}" '
                f'data-asset-role="{html.escape(asset.rol)}" '
                f"{familie_attributen}"
                f'data-asset-accessibility="'
                f'{html.escape(asset.toegankelijkheid)}" '
                f'aria-labelledby="{html.escape(heading_id)}">'
            ),
            '    <div class="bp-asset-preview">',
        ])
        regels.extend(
            f"      {regel}"
            for regel in svg_element_lines(
                asset,
                snapshot_ref,
                extra_attributes=(
                    ("class", "bp-asset-preview-graphic"),
                    ("data-bp-preview", "true"),
                ),
                force_decorative=True,
            )
        )
        regels.extend([
            "    </div>",
            (
                f'    <h3 id="{html.escape(heading_id)}">'
                f"{html.escape(asset.naam)}</h3>"
            ),
            f"    <p>{html.escape(asset.doel)}</p>",
            '    <dl class="bp-asset-contract">',
            "      <dt>Rol</dt>",
            f"      <dd>{html.escape(asset.rol)}</dd>",
            "      <dt>Viewbox</dt>",
            (
                "      <dd>"
                + html.escape(
                    " ".join(format(value, ".15g") for value in asset.viewbox)
                )
                + "</dd>"
            ),
            "      <dt>Paden</dt>",
            f"      <dd>{len(asset.paden)}</dd>",
            "      <dt>Vulling</dt>",
            f"      <dd>{html.escape(asset.vulling)}</dd>",
            "      <dt>Lijn</dt>",
            f"      <dd>{html.escape(asset.lijn)}</dd>",
            "      <dt>Toegankelijkheid</dt>",
            f"      <dd>{html.escape(asset.toegankelijkheid)}</dd>",
        ])
        if entry.familie is not None and asset.variant is not None:
            regels.extend([
                "      <dt>Familie</dt>",
                (
                    f"      <dd>{html.escape(entry.familie.naam)} "
                    f"({html.escape(entry.familie.familietype)})</dd>"
                ),
                "      <dt>Variant</dt>",
                f"      <dd>{html.escape(asset.variant)}</dd>",
            ])
        if asset.label is not None:
            regels.extend([
                "      <dt>Toegankelijke naam</dt>",
                f"      <dd>{html.escape(asset.label)}</dd>",
            ])
        regels.extend([
            "    </dl>",
            (
                f'    <a class="bp-asset-link" '
                f'href="{html.escape(artifact_href, quote=True)}" '
                f'data-asset-product="'
                f'{html.escape(entry.artifact_product_id)}">'
                "Open SVG</a>"
            ),
            "  </article>",
        ])
    regels.append("</div>")
    return tuple(regels)
