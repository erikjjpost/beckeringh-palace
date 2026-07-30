# Beckeringh Palace

Beckeringh Palace is een reproduceerbare digitale wereld en **product- en ontwerpcompiler**. Een normatief World Model vormt de bron voor documentatie, diagrammen en ontwerpoutputs zoals SVG, HTML, Grafana en Figma-componenten.

BAT is geen vervanging voor ArchiMate. Enterprise-architectuurmodellen blijven externe bronnen en kunnen via expliciete adapters worden gekoppeld.

## Huidige vertical slice

De repository bevat nu:

- Information Management en Second Brain als bestaande migratieconcepten;
- Architectuur Synchronisatie als bestaande service;
- BAT als domeinspecifieke taal voor het Beckeringh Palace World Model;
- parser, semantische validatie, dependency-analyse, constraints en getypeerde foutdiagnostiek;
- native thema's, appearances, componentvarianten met volledige
  statecontracten, toegankelijkheidscontracten, composities en layouts;
- een gedeeld productcontract met tekstuele en binaire productbackends;
- een Forge Dashboard en projectstatusproduct uit dezelfde opgeloste informatiearchitectuur;
- een native homepage met vier geordende inhoudsgebieden en drie productroutes;
- een statisch EmberForge designsystem referentieproduct met geordende
  primitives, tokens, componenttoestanden, voorbeelden en toegankelijkheid;
- een native EmberForge wallpaperfamilie met zelfstandige 3840 bij 1080 en
  1900 bij 1200 varianten die rechtstreeks uit BAT, het opgeloste thema en
  dezelfde SVG assets als de catalogus worden gerenderd;
- statische snapshotidentiteit voor verificatie en rollback;
- generatie van Markdown, Mermaid, CSS, HTML en importeerbare Grafana JSON;
- reproduceerbaarheidscontrole in lokale tooling en CI.

## Snel starten

```bash
git clone https://github.com/erikjjpost/beckeringh-palace.git
cd beckeringh-palace
python tools/bp.py check
```

## Structuur

```text
architectuur/   BAT-bronnen tijdens de migratie naar het World Model
compiler/       parser, semantisch model, constraints en renderers
model/          bestaande architectuurobjecten tijdens de migratie
organisation/   rollen, contracten en workflows
proposals/      gecontroleerde wijzigingsvoorstellen
project/        normatieve projectstatus
tools/          validator, generator en project-CLI
tests/          geautomatiseerde tests
output/         reproduceerbare gegenereerde output
docs/           ontwerpbesluiten en ontwikkelrichtlijnen
workspace/      werkruimte voor nieuwe ideeën
```

Lees [docs/world-model.md](docs/world-model.md) voor de domeingrens,
[docs/architecture.md](docs/architecture.md) voor de compilerarchitectuur,
[docs/product-model.md](docs/product-model.md) voor het productcontract,
[docs/beckeringh-architectuurtaal.md](docs/beckeringh-architectuurtaal.md) voor BAT,
[docs/product-runbook.md](docs/product-runbook.md) voor het gebruiken van de producten en
[docs/adr-convention.md](docs/adr-convention.md) voor ontwerpbesluiten en
[CONTRIBUTING.md](CONTRIBUTING.md) voor de wijzigingsregels. De actuele,
reproduceerbare voortgang staat in [PROJECT_STATUS.md](PROJECT_STATUS.md).
