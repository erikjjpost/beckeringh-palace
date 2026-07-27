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
ResolvedComposition
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

M9.1a introduceert daarnaast het native compositiecontract. Een compositie
beschrijft productinhoud als een geordende lijst benoemde componentinstanties.
Zij bevat geen richting, coördinaten of backendpresentatie. Alleen gevalideerde
CIR wordt omgezet naar `ResolvedComposition` en `ResolvedComponentInstance`.
M9.1b koppelt deze resolved compositie expliciet aan het product.

## Productcontext

Een product verwijst in BAT verplicht naar één compositie en één layout. Na
semantische validatie lost de productcompiler beide één keer op en levert deze
als `opgeloste_compositie` en `opgeloste_layout` aan de backend. Een backend
hoeft daardoor geen compositie- of layoutsemantiek opnieuw uit losse
CIR-objecten af te leiden.

De componentinstanties van de compositie moeten exact overeenkomen met de
instanties die door de regions van de layout worden geplaatst. Een ontbrekende,
extra of dubbele plaatsing is ongeldig. De koppeling gebeurt uitsluitend via
expliciete instantie-id's en nooit via lijstpositie.

Het resolved contract bevat geen HTML- of CSS-velden. De HTML-backend vertaalt
de layouttypen als volgt:

| BAT-intentie | HTML-backend |
|---|---|
| `grid` | CSS Grid met expliciete rijen, kolommen en spans |
| `stack` | Flexbox langs de expliciete richting |
| `flow` | Flexbox met expliciete richting en wrapkeuze |
| `layer` | Overlappende gridgebieden met het expliciete laagniveau |

De normatieve `instanties`-lijst van de compositie bepaalt voor alle typen de
inhouds- en DOM-volgorde. De `regions`-lijst legt uitsluitend expliciet vast
welke regions bij de layout horen. De koppeling tussen beide gebeurt via
instantie-id's en niet via lijstpositie. CSS is uitsluitend backenduitvoer en
wordt niet teruggeschreven naar BAT, CIR, `ResolvedComposition`,
`ResolvedLayout` of `ProductDefinition`.

## Native objecten

### `compositie`

Iedere compositie vereist:

- `naam`: menselijke naam;
- `doel`: beoogde productsamenstelling;
- `instanties`: expliciete, geordende en unieke lijst componentinstantie-id's.

De volgorde in `instanties` is de normatieve inhoudsvolgorde. Een compositie
bevat geen layoutvelden. Plaatsing en visuele ordening behoren uitsluitend tot
een native layout.

```bp
compositie overview {
    naam: "Overview"
    doel: "Bundelt de benoemde overzichtspanelen."
    instanties: ["overview-primary", "overview-secondary"]
}
```

### `componentinstantie`

Iedere componentinstantie vereist:

- `naam`: menselijke naam voor dit specifieke gebruik;
- `doel`: semantische rol binnen de compositie;
- `compositie`: de compositie waar de instantie bij hoort;
- `component`: de herbruikbare componentdefinitie.

De referentie is wederkerig: de compositie noemt de instantie en de instantie
verwijst terug naar exact die compositie. Daardoor kunnen meerdere instanties
van hetzelfde component afzonderlijk worden benoemd zonder hun identiteit uit
lijstpositie of rendererstructuur af te leiden.

```bp
componentinstantie overview-primary {
    naam: "Primair overzichtspaneel"
    doel: "Toont de hoofdstatus."
    compositie: "overview"
    component: "status-panel"
}
```

### `layout`

Iedere native layout vereist:

- `naam`: menselijke naam;
- `doel`: beoogd gebruik;
- `type`: exact `grid`, `stack`, `flow` of `layer`;
- `regions`: expliciete lijst met unieke region-id's.

De lijst is de normatieve en wederkerige lidmaatschapsdeclaratie. Een region die
niet in deze lijst staat, behoort niet impliciet tot de layout. De lijst bepaalt
geen tweede inhoudsvolgorde naast de compositie.

### `region`

Iedere native region vereist:

- `naam`: menselijke naam;
- `doel`: beoogde rol;
- `layout`: de layout waar deze region bij hoort;
- `instantie`: de benoemde componentinstantie die de region plaatst;
- alle plaatsingsvelden die bij het gekozen layouttype horen.

De referentie is wederkerig: de layout noemt de region en de region verwijst
terug naar diezelfde layout. Daardoor ontstaan geen impliciete regionselecties.
De onderliggende componentdefinitie wordt via de componentinstantie opgelost en
wordt niet opnieuw in de region gedeclareerd.

### `product`

Ieder product vereist:

- `naam`: menselijke naam;
- `doel`: het te genereren product;
- `backend`: de expliciete backend;
- `compositie`: de productinhoud;
- `layout`: de plaatsingsintentie;
- `pad`: het veilige relatieve uitvoerpad;
- `wereld`: verplicht wanneer een themalaag aanwezig is.

De productvalidator vereist dat `compositie` en `layout` exact dezelfde
componentinstanties bevatten. Daarmee is het product de enige expliciete
koppeling tussen inhoud, plaatsing en backend.

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
    instantie: "overview-primary"
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

`direction` is exact `horizontal` of `vertical`. De volgorde van de geplaatste
inhoud staat uitsluitend in de normatieve `instanties`-lijst van de compositie.

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
`true` of `false`. De volgorde van de geplaatste inhoud staat uitsluitend in de
normatieve `instanties`-lijst van de compositie.

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

## Voltooide migratie

M9.0c migreert de canonieke Forge productbron naar een native grid-layout. De
drie dashboardpanelen zijn expliciete `region`-objecten. De oude
pixelcoördinaten worden niet vertaald naar impliciete presentatievelden.

M9.0d verwijdert daarna het volledige M6 spatial contract. `layout` vereist
altijd een expliciet native type en `regio`, canvasafmetingen, absolute
coördinaten en de spatial HTML-fallback bestaan niet meer. Er is geen
automatische omzetting en geen backwards magic. Een productbackend ontvangt
uitsluitend een gevalideerde `ResolvedLayout`.

M9.1a vervangt vervolgens het M6 compositiecontract. `componenten` en
`richting` verdwijnen uit compositie. De zelfstandige compositie CSS-, HTML-
en SVG-renderers en hun renderdoelen verdwijnen eveneens, omdat zij
presentatiegedrag zonder product en zonder native layout vastlegden. De
canonieke Forge-compositie gebruikt drie expliciete componentinstanties.

M9.1b koppelt de Forge-compositie vervolgens aan het Forge-product. Regions
plaatsen voortaan een expliciete `componentinstantie` in plaats van een
componentdefinitie. De productcompiler levert zowel `ResolvedComposition` als
`ResolvedLayout` aan de backend. De HTML-backend behoudt de instantie-identiteit
in `data-instance` en gebruikt de opgeloste componentdefinitie voor
`data-component` en de componentklasse.

M9.1c verwijdert de dubbele productvolgorde. De geordende instanties van de
compositie bepalen de inhouds- en DOM-volgorde. De regions van de layout leggen
alleen expliciete plaatsing en lidmaatschap vast. De HTML-backend koppelt beide
op instantie-id en leidt niets af uit de positie van een item in beide lijsten.

## Diagnostics

| Code | Betekenis |
|---|---|
| `BP3506` | Product verwijst naar een onbekende of ontbrekende compositie |
| `BP3507` | Compositie en layout bevatten niet exact dezelfde instanties |
| `BP3601` | Onbekend layouttype |
| `BP3602` | Eigenschap past niet bij het layouttype |
| `BP3603` | `regions` is niet expliciet, uniek of geldig |
| `BP3604` | Layout verwijst naar een onbekende region |
| `BP3605` | Region verwijst niet terug naar de layout |
| `BP3606` | Ongeldige gridafmeting |
| `BP3607` | Ongeldige of ontbrekende richting |
| `BP3608` | Ongeldige of ontbrekende flow-wrapkeuze |
| `BP3609` | Layout plaatst dezelfde componentinstantie meer dan één keer |
| `BP3611` | Region verwijst naar een onbekende native layout |
| `BP3612` | Layout noemt de region niet |
| `BP3613` | Region verwijst naar een onbekende componentinstantie |
| `BP3614` | Region-eigenschap past niet bij het layouttype |
| `BP3615` | Ongeldig of ontbrekend plaatsingsgetal |
| `BP3616` | Grid-region valt buiten de kolommen |
| `BP3617` | Grid-region valt buiten de rijen |
| `BP3701` | Compositie heeft een onbekende eigenschap |
| `BP3702` | `instanties` is niet expliciet, uniek of geldig |
| `BP3703` | Compositie verwijst naar een onbekende componentinstantie |
| `BP3704` | Componentinstantie verwijst niet terug naar de compositie |
| `BP3710` | Componentinstantie heeft een onbekende eigenschap |
| `BP3711` | Componentinstantie verwijst naar een onbekende compositie |
| `BP3712` | Compositie noemt de componentinstantie niet |
| `BP3713` | Componentinstantie verwijst naar een onbekend component |
