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

### `naam` en `doel` zijn eindproducttekst, geen documentatie

Renderers tonen `naam` en `doel` rechtstreeks aan de eindgebruiker: als
paginakop, als panelbeschrijving, als productheader (zie
`compiler/native_layout_html_renderer.py` en `compiler/backends/grafana.py`).
Deze velden zijn dus geen interne toelichting voor BAT-auteurs, maar
zichtbare copy in het eindproduct.

Daaruit volgt: `naam` en `doel` bevatten nooit

- zelfreferentiële taal over BAT zelf ("gegenereerd uit BAT",
  "productdefinitie", "compositie") — dat hoort in commentaar bij het
  `.bp`-bestand of in `docs/`, niet in wat de gebruiker leest;
- werelduitleg of kamermetaforen uit `docs/world-bible.md` ("de kamer die
  continu meet en signaleert") — die taal hoort in de World Bible, niet in
  een productbeschrijving die een operator daadwerkelijk leest.

Ontwerpteksten (wereldkaart, architectuurbeslissingen, milestone-proza in
`project/status.json`) mogen die taal wel bevatten — dat zijn ontwerpen, geen
eindproducten. Het onderscheid is waar de tekst terechtkomt: `docs/` en BAT
Nederlandse toelichting mogen intern klinken, `naam`/`doel` op een native
object dat een renderer publiceert moet lezen als een normaal, professioneel
product.

## Compileren en controleren

```bash
python tools/compile_bat.py
python tools/bp.py check
```

De output wordt opgeslagen in `output/bat/` en is reproduceerbaar vanuit de BAT-bronnen.
