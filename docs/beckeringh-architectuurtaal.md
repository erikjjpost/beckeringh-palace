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

`doel` wordt daarentegen nergens meer als zichtbare UI-tekst gerenderd, op
geen enkel niveau. Erik Post: "als het geen toegevoegde waarde heeft, hoort
het niet in de ui" — een statische beschrijvingsparagraaf onder een
producttitel voegt niets toe voor iemand die het product daadwerkelijk
gebruikt (bijvoorbeeld een operationeel dashboard aflezen). Dat gold eerst
alleen voor de compositie-brede `doel` op de dashboardheader; M11.10a trok
dezelfde regel door naar het `doel` van elke afzonderlijke
componentinstantie ("Running" toonde ooit letterlijk "Aantal actieve
workloads" eronder — een parafrase van de titel, geen nieuwe informatie).
Beide niveaus zijn verwijderd uit zowel de HTML- (`bp-description`-paragraaf,
`compiler/native_layout_html_renderer.py`) als de Grafana-backend
(canvas-`-body`-element, `compiler/backends/grafana.py`). `doel` blijft wel
bestaan als verplicht BAT-veld en als Grafana-panelbeschrijving (het
info-icoon, alleen zichtbaar op hover, geen permanente schermruimte) — daar
mag het intern/documentatie-achtig klinken, want het is geen
altijd-zichtbare UI-tekst.

Dezelfde afweging geldt voor letterlijke tekstduplicatie: Grafana's eigen
paneelkoptekst toonde bovenop elk paneel exact dezelfde naam als de
gebrande Canvas-heading eronder ("Running" boven "Running"). Een lege
paneltitel (`"title": ""`) laat Grafana's koptekstbalk volledig
wegvallen — leeg getest tegen de echte Grafana-instantie, geen aanname —
zodat alleen de gebrande Canvas-naam overblijft.

Ontwerpteksten (wereldkaart, architectuurbeslissingen, milestone-proza in
`project/status.json`) mogen zelfreferentiële of narratieve taal wel
bevatten — dat zijn ontwerpen, geen eindproducten. Het onderscheid is waar de
tekst terechtkomt en of ze permanent zichtbaar is: `docs/` en BAT
Nederlandse toelichting mogen intern klinken; alles wat een renderer als
blijvend zichtbare UI-tekst publiceert, moet ofwel toegevoegde waarde hebben
voor wie het product gebruikt, ofwel niet bestaan.

### Eindproductteksten zijn Nederlands

Alle tekst die een renderer als zichtbare UI publiceert — `naam`, `label`,
`beschrijving`, `waarde`, databron-`mapping`-labels — is Nederlands, ook
wanneer de brondata (Kubernetes, Prometheus) Engelse termen gebruikt.
"Running" werd "Actief", "CPU Usage" werd "CPU-gebruik", een
Grafana-waardemapping `1` werd niet "Healthy" maar "Gezond". Uitzonderingen:
technische ID's/identifiers (`homelab-stat-nodes`, PromQL-expressies),
merknamen en eigennamen (`ISMS Challenger`, `CV Tool`, `Grafana`, `The
Observatory` als kamernaam uit `docs/world-bible.md`), en gangbare
Nederlandse IT-leenwoorden (`cluster`, `dashboard`, `node`) — dezelfde
uitzonderingscategorie die deze taal zelf al overal gebruikt.

### `databron`: een query is reproduceerbaar, een waarde niet

BAT compileert deterministisch: `bp.py check` vereist dat regeneratie van
`output/` byte-voor-byte identiek is. Een live meetwaarde is dat per
definitie niet. `databron` lost dat op door alleen de **query** in het
World Model vast te leggen, nooit het resultaat:

```bp
databron databron-homelab-nodes {
    naam: "Node count"
    doel: "Aantal actieve clusternodes via Prometheus kube-state-metrics."
    expr: "count(kube_node_info)"
    eenheid: "aantal"
}
```

- `expr`: een statische PromQL-expressie. Deze compileert deterministisch mee
  in de Grafana-output; Grafana voert de query pas op kijktijd uit, niet de
  BAT-compiler.
- `eenheid`: `aantal`, `percentage` of `tekst`.
- `mapping`: verplicht bij `eenheid: "tekst"`, verboden bij elke andere
  eenheid. Elk element heeft de vorm `"waarde:label"` (bijvoorbeeld
  `"1:Healthy"`), en vertaalt naar een Grafana `fieldConfig`-waardemapping.

Een `componentinstantie` verwijst optioneel naar een `databron` via het veld
`databron`, vrij te combineren met `voorbeeld` (het voorbeeld levert label en
opmaak, de databron levert de live waarde). Alleen de Grafana-backend
consumeert `databron`: het Canvas-tekstelement krijgt `text.mode: "field"` in
plaats van `"fixed"`, en het paneel krijgt een `datasource`- en
`targets`-veld. Welke Prometheus-instantie die query uitvoert, is geen
wereldfeit maar een omgevingsfeit: dat UID staat als backendconstante in
`compiler/backends/grafana.py`, niet in `architectuur/world.bp`.

De HTML-backend consumeert `databron` niet en blijft daardoor volledig
statisch en netwerkvrij. Eenzelfde compositie levert zo twee eerlijk
verschillende garanties op: een reproduceerbare snapshot (HTML) en een live
dashboard (Grafana), zonder dat de een de ander tegenspreekt. Een Grafana-
product zonder enige `databron` op zijn instanties blijft, zoals voorheen,
volledig zonder datasource.

## Compileren en controleren

```bash
python tools/compile_bat.py
python tools/bp.py check
```

De output wordt opgeslagen in `output/bat/` en is reproduceerbaar vanuit de BAT-bronnen.
