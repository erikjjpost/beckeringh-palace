# Architectuur

Beckeringh Palace is een architectural compiler: een normatief model wordt gevalideerd en omgezet in reproduceerbare representaties.

```text
Model + Organisatie + Voorstellen
              ↓
          Validator
              ↓
          Generator
              ↓
     Markdown + Mermaid + later SVG/HTML/Grafana/Figma
```

## Ontwerpprincipes

### Elke representatie is afgeleid van het model

> Elke representatie is afgeleid van het model. Er bestaat geen handmatig onderhouden documentatie.

Dit betekent concreet:

- architectuuroverzichten worden niet handmatig in README-bestanden bijgehouden;
- Mermaid-diagrammen worden gegenereerd en niet rechtstreeks gewijzigd;
- SVG-, HTML-, Grafana- en Figma-representaties worden door renderers opgebouwd;
- gegenereerde artefacten zijn nooit de bron van waarheid;
- wijzigingen beginnen in BAT, het normatieve model of de compiler.

Mensen en AI wijzigen dus uitsluitend normatieve bronnen en compilercomponenten. Alle overige representaties worden opnieuw gecompileerd.

## Lagen

### Normatieve bron

- `architectuur/`: BAT-bronnen (`.bp`) voor de semantische architectuur.
- `model/`: bestaande capabilities, services, assets, relaties en representaties tijdens de migratie naar BAT.
- `organisation/`: rollen, contracten en workflows.
- `proposals/`: gecontroleerde architectuurwijzigingen.

### Compiler tooling

- `compiler/`: parser, canonieke tussenrepresentatie en renderers.
- `tools/validate.py`: controleert modelintegriteit en architectuurregels.
- `tools/compile_bat.py`: compileert BAT naar CIR en afgeleide output.
- `tools/generate.py`: genereert bestaande afgeleide representaties.
- `tools/bp.py`: voert de volledige kwaliteitsketen uit.

### Afgeleide output

- `output/bat/`: vanuit BAT gegenereerde CIR- en documentatie-output.
- `output/docs/`: gegenereerde documentatie.
- `output/diagrams/`: gegenereerde diagrambron.

Output wordt gecommit om deterministische regeneratie te kunnen controleren. Zij blijft afgeleid; rechtstreekse wijzigingen worden bij de volgende compilatie overschreven en gelden niet als architectuurwijziging.
