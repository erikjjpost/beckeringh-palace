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

## Lagen

### Normatieve bron

- `model/`: capabilities, services, assets, relaties en representaties.
- `organisation/`: rollen, contracten en workflows.
- `proposals/`: gecontroleerde architectuurwijzigingen.

### Compiler tooling

- `tools/validate.py`: controleert modelintegriteit en architectuurregels.
- `tools/generate.py`: genereert afgeleide representaties.
- `tools/bp.py`: voert de volledige kwaliteitsketen uit.

### Afgeleide output

- `output/docs/`: gegenereerde documentatie.
- `output/diagrams/`: gegenereerde diagrambron.

Output wordt gecommit om deterministische regeneratie te kunnen controleren. Zij blijft afgeleid; wijzigingen beginnen altijd in de normatieve bron of generator.
