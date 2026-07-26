# Product Model

Beckeringh Palace compileert producten vanuit expliciete BAT-semantiek. M9.0a
introduceert daarvoor een native layout-engine. Deze engine bepaalt geen pixels
en bevat geen HTML-, CSS-, SVG-, Grafana-, Figma- of PowerPoint-concepten.

## Compilerketen

```text
BAT
 ↓
Parser
 ↓
CIR
 ↓
Semantische validatie
 ↓
ResolvedLayout
 ↓
ProductDefinition
 ↓
Renderers
```

De parser bewaart de declaraties en waarden ongewijzigd in de CIR. De
semantische laag controleert het volledige layoutcontract. Alleen gevalideerde
CIR wordt omgezet naar `ResolvedLayout` en `ResolvedRegion`.

M9.0a voegt geen rendererondersteuning toe. M9.0b levert de eerste verticale
backendintegratie: de productcompiler koppelt de `ResolvedLayout` expliciet aan
de `ProductDefinition` en de HTML-backend vertaalt die intentie naar HTML en
CSS. Andere backends krijgen later een eigen vertaling van hetzelfde resolved
contract.

## Productcontext

Een product blijft in BAT naar een layout-id verwijzen. Na semantische
validatie lost de productcompiler een native layout één keer op en levert deze
als `opgeloste_layout` aan de backend. Een backend hoeft daardoor geen
layoutsemantiek opnieuw uit losse CIR-objecten af te leiden.

Het resolved contract bevat geen HTML- of CSS-velden. De HTML-backend vertaalt
de layouttypen als volgt:

| BAT-intentie | HTML-backend |
|---|---|
| `grid` | CSS Grid met expliciete rijen, kolommen en spans |
| `stack` | Flexbox langs de expliciete richting |
| `flow` | Flexbox met expliciete richting en wrapkeuze |
| `layer` | Overlappende gridgebieden met het expliciete laagniveau |

De normatieve `regions`-lijst bepaalt voor alle typen de DOM-volgorde. CSS is
uitsluitend backenduitvoer en wordt niet teruggeschreven naar BAT, CIR,
`ResolvedLayout` of `ProductDefinition`.

## Native objecten

### `layout`

Iedere native layout vereist:

- `naam`: menselijke naam;
- `doel`: beoogd gebruik;
- `type`: exact `grid`, `stack`, `flow` of `layer`;
- `regions`: expliciete, geordende lijst met unieke region-id's.

De volgorde in `regions` is normatief. Een region die niet in deze lijst staat,
behoort niet impliciet tot de layout.

### `region`

Iedere native region vereist:

- `naam`: menselijke naam;
- `doel`: beoogde rol;
- `layout`: de layout waar deze region bij hoort;
- `component`: het component dat de region bevat;
- alle plaatsingsvelden die bij het gekozen layouttype horen.

De referentie is wederkerig: de layout noemt de region en de region verwijst
terug naar diezelfde layout. Daardoor ontstaan geen impliciete regionselecties.

## Layouttypen

### Grid

Een grid beschrijft plaatsing in een expliciet aantal rijen en kolommen.

```bp
layout overview-grid {
    naam: "Overview grid"
    doel: "Plaatst overzichtspanelen in een raster."
    type: "grid"
    regions: ["overview-main"]
    columns: "12"
    rows: "4"
}

region overview-main {
    naam: "Main"
    doel: "Hoofdinhoud van het overzicht."
    layout: "overview-grid"
    component: "overview-panel"
    column: "1"
    row: "1"
    column-span: "12"
    row-span: "4"
}
```

`columns`, `rows`, `column`, `row`, `column-span` en `row-span` zijn positieve
gehele getallen. Een region mag niet buiten het grid vallen.

### Stack

Een stack ordent regions langs één expliciete as.

```bp
layout detail-stack {
    naam: "Detail stack"
    doel: "Ordent detailsecties verticaal."
    type: "stack"
    regions: ["detail-header", "detail-body"]
    direction: "vertical"
}
```

`direction` is exact `horizontal` of `vertical`. De volgorde van de regions
staat uitsluitend in de normatieve `regions`-lijst van de layout.

### Flow

Een flow ordent regions langs een as en legt expliciet vast of doorloop naar een
volgende baan is toegestaan.

```bp
layout card-flow {
    naam: "Card flow"
    doel: "Ordent een variabel aantal kaarten."
    type: "flow"
    regions: ["first-card"]
    direction: "horizontal"
    wrap: "true"
}
```

`direction` is exact `horizontal` of `vertical`. `wrap` is verplicht en is exact
`true` of `false`. De volgorde van de regions staat uitsluitend in de
normatieve `regions`-lijst van de layout.

### Layer

Een layer-layout stapelt regions op expliciete niveaus.

```bp
layout hero-layer {
    naam: "Hero layer"
    doel: "Combineert basisinhoud en annotatie."
    type: "layer"
    regions: ["hero-base", "hero-annotation"]
}
```

Iedere region heeft een niet-negatief geheel getal in `layer`. Een hoger getal
betekent een hogere semantische laag. De renderer bepaalt hoe dat mechanisme in
de backend wordt gerealiseerd.

## Geen impliciete defaults

Een typegebonden veld wordt nooit afgeleid:

- een grid zonder `rows` of `columns` is ongeldig;
- een stack zonder `direction` is ongeldig;
- een flow zonder `direction` of `wrap` is ongeldig;
- een region zonder alle plaatsingsvelden voor zijn layouttype is ongeldig.

Velden van een ander layouttype zijn eveneens ongeldig. Hierdoor blijft iedere
BAT-declaratie volledig en eenduidig.

## Migratiegrens

Het bestaande M6 spatial contract gebruikt `regio`, canvasafmetingen en absolute
coördinaten. Dat contract blijft uitsluitend als expliciet migratieobject
bestaan zolang bestaande productrenderers ervan afhankelijk zijn. `region` is
het native M9-object. Er bestaat geen automatische omzetting tussen beide
contracten.

M9.0b behoudt het bestaande HTML-pad voor producten die expliciet naar een M6
spatial layout verwijzen. Een native product gebruikt de native HTML-vertaling;
een spatial product gebruikt de bestaande spatial renderer.

M9.0c migreert de canonieke Forge productbron naar een native grid-layout. De
drie dashboardpanelen zijn expliciete `region`-objecten en de normatieve
`regions`-lijst bepaalt hun volgorde. De oude pixelcoördinaten worden niet
vertaald naar impliciete presentatievelden. Het M6 spatial contract blijft
uitsluitend beschikbaar voor expliciete legacyproducten.

## Diagnostics

| Code | Betekenis |
|---|---|
| `BP3601` | Onbekend layouttype |
| `BP3602` | Eigenschap past niet bij het layouttype |
| `BP3603` | `regions` is niet expliciet, uniek of geldig |
| `BP3604` | Layout verwijst naar een onbekende region |
| `BP3605` | Region verwijst niet terug naar de layout |
| `BP3606` | Ongeldige gridafmeting |
| `BP3607` | Ongeldige of ontbrekende richting |
| `BP3608` | Ongeldige of ontbrekende flow-wrapkeuze |
| `BP3611` | Region verwijst naar een onbekende native layout |
| `BP3612` | Layout noemt de region niet |
| `BP3613` | Region verwijst naar een onbekend component |
| `BP3614` | Region-eigenschap past niet bij het layouttype |
| `BP3615` | Ongeldig of ontbrekend plaatsingsgetal |
| `BP3616` | Grid-region valt buiten de kolommen |
| `BP3617` | Grid-region valt buiten de rijen |
