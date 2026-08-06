"""Native, reproduceerbaar contract voor een Figma masterbeschrijving."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from compiler.cir import Architectuurobject
from compiler.constraints import ConstraintContext
from compiler.design_components import DesignComponent, verzamel_componenten
from compiler.design_compositions import ResolvedComposition, resolveer_composities
from compiler.design_variants import ResolvedComponentVariant, resolveer_varianten
from compiler.diagnostics import Diagnostic
from compiler.layout_model import ResolvedLayout, resolveer_layouts
from compiler.svg_assets import ResolvedSvgAsset, resolveer_svg_assets
from compiler.theme_resolution import ResolvedTheme, resolveer_thema


FIGMA_MASTER_CONTENT = "figma-master"
FIGMA_MASTER_BACKEND = "figma-manifest"
FIGMA_MASTER_SUFFIX = ".figma.json"
FIGMA_MASTER_FIELDS = frozenset({
    "naam",
    "doel",
    "wereld",
    "assets",
    "componenten",
    "varianten",
    "composities",
    "layouts",
})


@dataclass(frozen=True)
class ResolvedFigmaMaster:
    id: str
    naam: str
    doel: str
    wereld: str
    thema: ResolvedTheme
    assets: tuple[ResolvedSvgAsset, ...]
    componenten: tuple[DesignComponent, ...]
    varianten: tuple[ResolvedComponentVariant, ...]
    composities: tuple[ResolvedComposition, ...]
    layouts: tuple[ResolvedLayout, ...]


def _tekst(obj: Architectuurobject, veld: str) -> str:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, str) or not waarde.strip():
        raise ValueError(
            f"Figma master '{obj.id}' vereist tekstveld '{veld}'"
        )
    return waarde


def _ids(obj: Architectuurobject, veld: str) -> tuple[str, ...]:
    waarde = obj.eigenschappen.get(veld)
    if not isinstance(waarde, list) or not waarde or not all(
        isinstance(item, str) and item.strip() for item in waarde
    ):
        raise ValueError(
            f"Figma master '{obj.id}' vereist niet-lege lijst '{veld}'"
        )
    return tuple(waarde)


@dataclass(frozen=True)
class FigmaMasterConstraint:
    sleutel: str = "world-model.figma-master"

    def evalueer(self, context: ConstraintContext):
        diagnostics = []
        index = {
            soort: {obj.id: obj for obj in context.objecten if obj.soort == soort}
            for soort in (
                "wereld",
                "asset",
                "component",
                "variant",
                "compositie",
                "componentinstantie",
                "componentvoorbeeld",
                "homepagegebied",
                "layout",
                "region",
            )
        }
        for obj in context.objecten:
            if obj.soort != "figmamaster":
                continue
            for veld in obj.eigenschappen:
                if veld not in FIGMA_MASTER_FIELDS:
                    diagnostics.append(Diagnostic(
                        code="BP4401",
                        boodschap=(
                            f"Figma master '{obj.id}' heeft onbekende eigenschap "
                            f"'{veld}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                    ))
            wereld = obj.eigenschappen.get("wereld")
            if wereld not in index["wereld"]:
                diagnostics.append(Diagnostic(
                    code="BP4402",
                    boodschap=(
                        f"Figma master '{obj.id}' verwijst naar onbekende of "
                        f"ontbrekende wereld '{wereld}'"
                    ),
                    locatie=obj.eigenschaplocaties.get("wereld", obj.bronlocatie),
                ))
            geselecteerd: dict[str, set[str]] = {}
            for veld, soort in (
                ("assets", "asset"),
                ("componenten", "component"),
                ("varianten", "variant"),
                ("composities", "compositie"),
                ("layouts", "layout"),
            ):
                waarde = obj.eigenschappen.get(veld)
                if not isinstance(waarde, list) or not waarde or not all(
                    isinstance(item, str) and item.strip() for item in waarde
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4403",
                        boodschap=(
                            f"Figma master '{obj.id}' vereist niet-lege "
                            f"referentielijst '{veld}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                    ))
                    continue
                if len(set(waarde)) != len(waarde):
                    diagnostics.append(Diagnostic(
                        code="BP4404",
                        boodschap=(
                            f"Figma master '{obj.id}' bevat dubbele referenties "
                            f"in '{veld}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                    ))
                onbekend = [item for item in waarde if item not in index[soort]]
                if onbekend:
                    diagnostics.append(Diagnostic(
                        code="BP4405",
                        boodschap=(
                            f"Figma master '{obj.id}' verwijst in '{veld}' naar "
                            f"onbekende {soort} '{onbekend[0]}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(veld, obj.bronlocatie),
                    ))
                geselecteerd[veld] = set(waarde)

            component_ids = geselecteerd.get("componenten", set())
            variant_ids = geselecteerd.get("varianten", set())
            for variant_id in geselecteerd.get("varianten", set()):
                variant = index["variant"].get(variant_id)
                if variant is None:
                    continue
                component_id = variant.eigenschappen.get("component")
                if component_id not in component_ids:
                    diagnostics.append(Diagnostic(
                        code="BP4406",
                        boodschap=(
                            f"Figma master '{obj.id}' selecteert variant "
                            f"'{variant_id}' zonder component '{component_id}'"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "varianten", obj.bronlocatie
                        ),
                    ))

            compositie_ids = geselecteerd.get("composities", set())
            instance_ids: set[str] = set()
            for compositie_id in compositie_ids:
                compositie = index["compositie"].get(compositie_id)
                if compositie is None:
                    continue
                instanties = compositie.eigenschappen.get("instanties", [])
                if isinstance(instanties, list):
                    instance_ids.update(
                        item for item in instanties if isinstance(item, str)
                    )
            for instance_id in instance_ids:
                instantie = index["componentinstantie"].get(instance_id)
                if instantie is None:
                    continue
                component_id = instantie.eigenschappen.get("component")
                variant_id = instantie.eigenschappen.get("variant")
                voorbeeld_id = instantie.eigenschappen.get("voorbeeld")
                homepage_id = instantie.eigenschappen.get("homepagegebied")
                if isinstance(voorbeeld_id, str):
                    voorbeeld = index["componentvoorbeeld"].get(voorbeeld_id)
                    if voorbeeld is not None:
                        component_id = voorbeeld.eigenschappen.get("component")
                        variant_id = voorbeeld.eigenschappen.get("variant")
                if isinstance(homepage_id, str):
                    homepage = index["homepagegebied"].get(homepage_id)
                    if homepage is not None:
                        component_id = homepage.eigenschappen.get("component")
                        variant_id = homepage.eigenschappen.get("variant")
                if (
                    isinstance(component_id, str)
                    and component_id not in component_ids
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4407",
                        boodschap=(
                            f"Figma master '{obj.id}' compositie gebruikt "
                            f"component '{component_id}' buiten de selectie"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "composities", obj.bronlocatie
                        ),
                    ))
                if (
                    isinstance(variant_id, str)
                    and variant_id not in variant_ids
                ):
                    diagnostics.append(Diagnostic(
                        code="BP4409",
                        boodschap=(
                            f"Figma master '{obj.id}' compositie gebruikt "
                            f"variant '{variant_id}' buiten de selectie"
                        ),
                        locatie=obj.eigenschaplocaties.get(
                            "composities", obj.bronlocatie
                        ),
                    ))
            for layout_id in geselecteerd.get("layouts", set()):
                layout = index["layout"].get(layout_id)
                if layout is None:
                    continue
                regions = layout.eigenschappen.get("regions", [])
                for region_id in regions if isinstance(regions, list) else []:
                    region = index["region"].get(region_id)
                    if region is None:
                        continue
                    instance_id = region.eigenschappen.get("instantie")
                    if instance_id not in instance_ids:
                        diagnostics.append(Diagnostic(
                            code="BP4408",
                            boodschap=(
                                f"Figma master '{obj.id}' layout '{layout_id}' "
                                f"gebruikt instantie '{instance_id}' buiten de "
                                "geselecteerde composities"
                            ),
                            locatie=obj.eigenschaplocaties.get(
                                "layouts", obj.bronlocatie
                            ),
                        ))
        return tuple(diagnostics)


def resolveer_figma_masters(
    objecten: Iterable[Architectuurobject],
) -> tuple[ResolvedFigmaMaster, ...]:
    objecten = tuple(objecten)
    assets = {item.id: item for item in resolveer_svg_assets(objecten)}
    componenten = {item.id: item for item in verzamel_componenten(objecten)}
    varianten = {item.id: item for item in resolveer_varianten(objecten)}
    composities = {item.id: item for item in resolveer_composities(objecten)}
    layouts = {item.id: item for item in resolveer_layouts(objecten)}
    masters = []
    for obj in objecten:
        if obj.soort != "figmamaster":
            continue
        wereld = _tekst(obj, "wereld")
        masters.append(ResolvedFigmaMaster(
            id=obj.id,
            naam=_tekst(obj, "naam"),
            doel=_tekst(obj, "doel"),
            wereld=wereld,
            thema=resolveer_thema(objecten, wereld),
            assets=tuple(assets[item] for item in _ids(obj, "assets")),
            componenten=tuple(
                componenten[item] for item in _ids(obj, "componenten")
            ),
            varianten=tuple(varianten[item] for item in _ids(obj, "varianten")),
            composities=tuple(
                composities[item] for item in _ids(obj, "composities")
            ),
            layouts=tuple(layouts[item] for item in _ids(obj, "layouts")),
        ))
    return tuple(sorted(masters, key=lambda master: master.id))
