# Architectuur

Beckeringh Palace is een product- en ontwerpcompiler: een normatief World Model wordt gevalideerd en omgezet in reproduceerbare representaties.

```text
World Model + Organisatie + Voorstellen
                  ↓
              Compiler
                  ↓
        Semantisch World Model
                  ↓
              Renderers
                  ↓
 Markdown / Mermaid / SVG / HTML / Grafana / Figma
```

BAT is geen algemene enterprise-architectuurtaal. ArchiMate en andere externe modellen worden uitsluitend via expliciete adapters gekoppeld. De domeingrens staat in [world-model.md](world-model.md).

## Ontwerpprincipes

### Elke representatie is afgeleid van het model

> Elke representatie is afgeleid van het model. Er bestaat geen handmatig onderhouden productdocumentatie.

Dit betekent concreet:

- overzichten worden niet handmatig in README-bestanden bijgehouden;
- Mermaid-diagrammen worden gegenereerd en niet rechtstreeks gewijzigd;
- SVG-, HTML-, Grafana- en Figma-representaties worden door renderers opgebouwd;
- gegenereerde artefacten zijn nooit de bron van waarheid;
- wijzigingen beginnen in BAT, het normatieve model of de compiler.

Mensen en AI wijzigen dus uitsluitend normatieve bronnen en compilercomponenten. Alle overige representaties worden opnieuw gecompileerd.

### De taal blijft domeinspecifiek

Een native BAT-concept moet nodig zijn om Beckeringh Palace-producten te specificeren of te renderen. Algemene enterprise-architectuurconcepten worden niet aan de kern toegevoegd. Hierdoor blijft BAT kleiner dan een architectuurmodelleertaal en gericht op reproduceerbare producten.

## Lagen

### Normatieve bron

- `architectuur/`: BAT-bronnen (`.bp`) tijdens de migratie naar het World Model.
- `model/`: bestaande capabilities, services, assets, relaties en representaties tijdens de migratie.
- `organisation/`: rollen, contracten en workflows.
- `proposals/`: gecontroleerde wijzigingen.

### Compiler tooling

- `compiler/`: parser, canonieke tussenrepresentatie, World Model, semantische analyse en renderers.
- `compiler/world_model.py`: normatieve catalogus en domeingrens van objectsoorten.
- `tools/validate.py`: controleert modelintegriteit en regels.
- `tools/compile_bat.py`: compileert BAT naar CIR en afgeleide output.
- `tools/generate.py`: genereert bestaande afgeleide representaties.
- `tools/bp.py`: voert de volledige kwaliteitsketen uit.

### Afgeleide output

- `output/bat/`: vanuit BAT gegenereerde CIR- en documentatie-output.
- `output/docs/`: gegenereerde documentatie.
- `output/diagrams/`: gegenereerde diagrambron.

Output wordt gecommit om deterministische regeneratie te kunnen controleren. Zij blijft afgeleid; rechtstreekse wijzigingen worden bij de volgende compilatie overschreven en gelden niet als modelwijziging.
