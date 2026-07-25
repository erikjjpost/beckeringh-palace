# Beckeringh Architectuurtaal

De Beckeringh Architectuurtaal (BAT) is de mens- en AI-leesbare broncode van Beckeringh Palace. BAT-bestanden gebruiken de extensie `.bp`.

## Ontwerpregel

Mensen en AI wijzigen geen gegenereerde artefacten. Zij wijzigen de Beckeringh Architectuurtaal. Alle overige representaties worden gecompileerd.

## Compilerlagen

```text
BAT-bron (.bp)
    ↓
Parser
    ↓
Canonieke tussenrepresentatie (CIR)
    ↓
Renderers
    ├── JSON
    └── Markdown
```

Renderers mogen uitsluitend de CIR lezen. Zij kennen de syntaxis van BAT niet.

## Eerste syntaxis

```bp
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen over de volledige levenscyclus."
    levert: ["Betrouwbare informatie", "Vindbare informatie"]
}
```

Ondersteunde soorten in M3:

- `capability`
- `dienst`
- `proces`
- `representatie`
- `agent`

Ieder object heeft minimaal `naam` en `doel`. Identifiers zijn technisch stabiel en waarden zijn Nederlandstalig.

## Compileren en controleren

```bash
python tools/compile_bat.py
python tools/bp.py check
```

De output wordt opgeslagen in `output/bat/` en is reproduceerbaar vanuit de BAT-bronnen.
