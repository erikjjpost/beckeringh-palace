# Beckeringh Palace

Beckeringh Palace is een reproduceerbare digitale wereld en **product- en ontwerpcompiler**. Een normatief World Model vormt de bron voor documentatie, diagrammen en ontwerpoutputs zoals SVG, HTML, Grafana en Figma-componenten.

BAT is geen vervanging voor ArchiMate. Enterprise-architectuurmodellen blijven externe bronnen en kunnen via expliciete adapters worden gekoppeld.

## Huidige vertical slice

De repository bevat nu:

- Information Management en Second Brain als bestaande migratieconcepten;
- Architectuur Synchronisatie als bestaande service;
- modelonafhankelijke rollen, contracten en workflow;
- parser, semantische validatie, dependency-analyse en constraints;
- een expliciete grens voor het Beckeringh Palace World Model;
- een native layout-engine voor `grid`, `stack`, `flow` en `layer`;
- een HTML-backend die gevalideerde native layoutintentie vertaalt;
- generatie van Markdown en Mermaid;
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
tools/          validator, generator en project-CLI
tests/          geautomatiseerde tests
output/         reproduceerbare gegenereerde output
docs/           ontwerpbesluiten en ontwikkelrichtlijnen
workspace/      werkruimte voor nieuwe ideeën
```

Lees [docs/world-model.md](docs/world-model.md) voor de domeingrens,
[docs/architecture.md](docs/architecture.md) voor de compilerarchitectuur,
[docs/product-model.md](docs/product-model.md) voor native layouts en
[CONTRIBUTING.md](CONTRIBUTING.md) voor de wijzigingsregels. De actuele,
reproduceerbare voortgang staat in [PROJECT_STATUS.md](PROJECT_STATUS.md).
