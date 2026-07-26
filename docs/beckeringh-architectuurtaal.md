# Beckeringh Architectuurtaal

De Beckeringh Architectuurtaal (BAT) is de mens- en AI-leesbare broncode van Beckeringh Palace. BAT-bestanden gebruiken de extensie `.bp`.

## Ontwerpregels

### Normatieve bron

Mensen en AI wijzigen geen gegenereerde artefacten. Zij wijzigen de Beckeringh Architectuurtaal. Alle overige representaties worden gecompileerd.

### Afgeleide representaties

> Elke representatie is afgeleid van het model. Er bestaat geen handmatig onderhouden documentatie.

Daaruit volgen vier harde regels:

1. BAT en de canonieke tussenrepresentatie bepalen de semantiek.
2. Renderers bepalen uitsluitend de presentatie.
3. Gegenereerde bestanden worden nooit rechtstreeks gewijzigd.
4. Een representatie die niet reproduceerbaar kan worden gegenereerd, hoort niet bij Beckeringh Palace.

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

## Syntaxis

```bp
capability informatiebeheer {
    naam: "Informatiebeheer"
    doel: "Informatie beheersen over de volledige levenscyclus."
    levert: ["Betrouwbare informatie", "Vindbare informatie"]
}
```

De syntaxis accepteert generieke declaraties. Het World Model bepaalt
semantisch welke objectsoorten en velden geldig zijn. Daardoor kent de parser
geen verborgen domeincatalogus.

Native objecten hebben minimaal `naam` en `doel`. Identifiers zijn technisch
stabiel. Het native layoutcontract staat in
[product-model.md](product-model.md).

## Compileren en controleren

```bash
python tools/compile_bat.py
python tools/bp.py check
```

De output wordt opgeslagen in `output/bat/` en is reproduceerbaar vanuit de BAT-bronnen.
