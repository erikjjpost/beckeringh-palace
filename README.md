# Beckeringh Palace

Beckeringh Palace is een reproduceerbare digitale wereld en **architectural compiler**. Een normatief model vormt de bron voor documentatie, diagrammen en toekomstige ontwerpoutputs zoals SVG, HTML, Grafana en Figma-componenten.

## Huidige vertical slice

De repository bevat nu:

- Information Management en Second Brain als eerste capabilities;
- Architectuur Synchronisatie als eerste service;
- modelonafhankelijke rollen, contracten en workflow;
- validatie van architectuurregels;
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
model/          normatieve architectuurobjecten
organisation/   rollen, contracten en workflows
proposals/      gecontroleerde wijzigingsvoorstellen
tools/          validator, generator en project-CLI
tests/          geautomatiseerde tests
output/         reproduceerbare gegenereerde output
docs/           architectuur- en ontwikkelrichtlijnen
workspace/      werkruimte voor nieuwe ideeën
```

Lees [docs/architecture.md](docs/architecture.md) voor de architectuur en [CONTRIBUTING.md](CONTRIBUTING.md) voor de wijzigingsregels.
