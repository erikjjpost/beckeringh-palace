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

### `naam` is eindproducttekst; `doel` is dat expliciet niet

Renderers tonen `naam` rechtstreeks aan de eindgebruiker: als paginakop, als
producttitel (zie `compiler/native_layout_html_renderer.py` en
`compiler/backends/grafana.py`). `naam` is dus geen interne toelichting voor
BAT-auteurs, maar zichtbare copy in het eindproduct, en bevat daarom nooit

- zelfreferentiële taal over BAT zelf ("gegenereerd uit BAT",
  "productdefinitie", "compositie") — dat hoort in commentaar bij het
  `.bp`-bestand of in `docs/`, niet in wat de gebruiker leest;
- werelduitleg of kamermetaforen uit `docs/world-bible.md` ("de kamer die
  continu meet en signaleert") — die taal hoort in de World Bible, niet in
  een productnaam die een operator daadwerkelijk leest.

`doel` wordt daarentegen nergens meer als zichtbare UI-tekst gerenderd. Erik
Post: "als het geen toegevoegde waarde heeft, hoort het niet in de ui" — een
statische beschrijvingsparagraaf onder een producttitel voegt niets toe voor
iemand die het product daadwerkelijk gebruikt (bijvoorbeeld een operationeel
dashboard aflezen), en is dus verwijderd uit zowel de HTML- als de
Grafana-backend. `doel` blijft wel bestaan als verplicht BAT-veld en als
Grafana-panelbeschrijving (het info-icoon, alleen zichtbaar op hover, geen
permanente schermruimte) — daar mag het intern/documentatie-achtig klinken,
want het is geen altijd-zichtbare UI-tekst.

Ontwerpteksten (wereldkaart, architectuurbeslissingen, milestone-proza in
`project/status.json`) mogen zelfreferentiële of narratieve taal wel
bevatten — dat zijn ontwerpen, geen eindproducten. Het onderscheid is waar de
tekst terechtkomt en of ze permanent zichtbaar is: `docs/` en BAT
Nederlandse toelichting mogen intern klinken; alles wat een renderer als
blijvend zichtbare UI-tekst publiceert, moet ofwel toegevoegde waarde hebben
voor wie het product gebruikt, ofwel niet bestaan.

## Compileren en controleren

```bash
python tools/compile_bat.py
python tools/bp.py check
```

De output wordt opgeslagen in `output/bat/` en is reproduceerbaar vanuit de BAT-bronnen.
