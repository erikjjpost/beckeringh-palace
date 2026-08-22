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

M9.2a voegt gecontroleerde componentvarianten toe. Een variant koppelt exact
één component aan één alternatieve appearance. Een componentinstantie kan die
variant expliciet kiezen. Zonder variant gebruikt de instantie de appearance
van het component. Er is geen impliciete standaardvariant.

## Productcontext

Een compositieproduct verwijst in BAT verplicht naar één compositie en één
layout. Na semantische validatie lost de productcompiler beide één keer op en
levert deze als `opgeloste_compositie` en `opgeloste_layout` aan de backend.
Een assetproduct verwijst in plaats daarvan expliciet naar één native asset en
ontvangt dit als `opgelost_asset`. Een wallpaperproduct verwijst naar één
native wallpaper en ontvangt canvas, formaat, lagen en assetplaatsingen als
`opgeloste_wallpaper`. Een backend hoeft daardoor geen compositie-, layout-,
asset- of wallpapersemantiek opnieuw uit losse CIR-objecten af te leiden.

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
instantie-id's en niet via lijstpositie. De opgeloste instantie levert daarnaast
de componentidentiteit en zichtbare instantienaam. Een `ResolvedRegion` bevat
die gegevens niet opnieuw. CSS is uitsluitend backenduitvoer en wordt niet
teruggeschreven naar BAT, CIR, `ResolvedComposition`, `ResolvedLayout` of
`ProductDefinition`.

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
- `variant`: optionele, expliciete variant van datzelfde component.
- `navigatie`: optionele, geordende en unieke lijst van product- of
  renderdoel-id's.

De referentie is wederkerig: de compositie noemt de instantie en de instantie
verwijst terug naar exact die compositie. Daardoor kunnen meerdere instanties
van hetzelfde component afzonderlijk worden benoemd zonder hun identiteit uit
lijstpositie of rendererstructuur af te leiden.

Een navigatiedoel wordt tijdens de compositieresolutie vertaald naar id, naam,
objectsoort en artifactpad. Backends ontvangen daarmee een volledig opgelost
navigatiecontract en zoeken zelf geen producten of uitvoerpaden. Een onbekend
doel of een doel dat geen `product` of `renderdoel` is, wordt semantisch
afgewezen.

```bp
componentinstantie overview-primary {
    naam: "Primair overzichtspaneel"
    doel: "Toont de hoofdstatus."
    compositie: "overview"
    component: "status-panel"
    navigatie: ["overview-html"]
}
```

### `variant`

Iedere variant vereist:

- `naam`: menselijke naam;
- `doel`: de gecontroleerde afwijking;
- `component`: het component waarvoor de variant geldig is;
- `appearance`: de rustappearance.

Een variant kan alleen worden gekozen door een componentinstantie die naar
hetzelfde component verwijst. Het resolved compositiemodel bewaart zowel de
variant-id als de effectieve appearance-id. De HTML-backend bewaart beide als
expliciete `data-variant` en `data-appearance` metadata en voegt een afgeleide
variantklasse toe als CSS haak. De component CSS-renderer genereert de
alternatieve appearance onder die selectorspecifieke variantregel na de
basiscomponent. Zonder expliciete variant blijft uitsluitend de basisappearance
actief.

Een interactieve variant kan daarnaast `hover`, `focus`, `pressed` en
`disabled` declareren. Zodra één van deze velden aanwezig is, zijn alle vier
verplicht. De compiler ordent het volledige contract altijd als `rest`,
`hover`, `focus`, `pressed`, `disabled` en lost iedere waarde naar een bestaande
appearance op. De renderer ontvangt deze mapping en mag geen ontbrekende
toestand of merkwaarde zelf aanvullen.

```bp
variant status-panel-compact {
    naam: "Compact status panel"
    doel: "Gebruikt het compacte statuspaneelprofiel."
    component: "status-panel"
    appearance: "status-panel-compact-appearance"
    hover: "status-panel-hover-appearance"
    focus: "status-panel-focus-appearance"
    pressed: "status-panel-pressed-appearance"
    disabled: "status-panel-disabled-appearance"
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

### `asset`

M11.5a begrenst het native assetobject tot veilig genereerbare SVG
padgeometrie. Ieder SVG asset vereist:

- `naam` en `doel`;
- `formaat`: exact `svg`;
- `rol`: `icoon`, `logo`, `illustratie` of `ornament`;
- `viewbox`: vier eindige getallen met positieve breedte en hoogte;
- `paden`: een niet-lege, unieke en begrensde lijst geldige SVG paden;
- `vulling` en `lijn`: `none`, `currentColor` of een hexkleur, waarbij minstens
  één zichtbaar is;
- een volledig lijncontract wanneer `lijn` niet `none` is;
- `toegankelijkheid`: `informatief` met een verplicht `label`, of `decoratief`
  zonder label.
- optioneel `familie` en `variant`, uitsluitend samen en via een bekende
  wederkerige `assetfamilie`.

Het contract bevat geen ruwe XML, scripts, eventhandlers, externe referenties,
fonts of URL-gebaseerde paint. De SVG backend ontvangt alleen
`ResolvedSvgAsset` en kan daardoor uitsluitend bekende elementen en attributen
schrijven.

```bp
asset forge-vector-node {
    naam: "Forge Vector Node"
    doel: "Herbruikbaar technisch lijnornament."
    formaat: "svg"
    rol: "ornament"
    viewbox: "0 0 64 64"
    paden: ["M32 6 L56 32 L32 58 L8 32 Z"]
    vulling: "none"
    lijn: "currentColor"
    lijndikte: "2"
    lijneinde: "round"
    lijnverbinding: "round"
    toegankelijkheid: "decoratief"
}
```

### `assetfamilie`

M11.5d ordent samenhangende assets met een expliciet backendonafhankelijk
familiecontract. Iedere familie vereist:

- `naam` en `doel`;
- `type`: `iconen` of `merk`;
- `merk`: een bestaande native merkidentiteit;
- `assets`: minstens twee unieke assets in normatieve volgorde.

Ieder familielid verwijst met `familie` terug naar exact dezelfde familie en
draagt een unieke betekenisvolle `variant`. Een iconenfamilie accepteert alleen
assets met rol `icoon`. Een merkfamilie accepteert alleen rol `logo` en vereist
exact de varianten `merkteken` en `woordmerk`.

```bp
assetfamilie forge-merkassets {
    naam: "Forge merkassets"
    doel: "Ordent het merkteken en woordmerk."
    type: "merk"
    merk: "forge"
    assets: ["forge-merkteken", "forge-woordmerk"]
}
```

De resolver levert geordende `ResolvedSvgAssetFamily` objecten zonder backend
of artifactkennis. De catalogus koppelt een asset aan haar opgeloste familie.
De generieke SVG serialisatie publiceert alleen de familie en variant als
metadata en blijft onafhankelijk van het familietype.

### `wallpaperfamilie`

M11.6c ordent meerdere zelfstandig gespecificeerde canvasformaten onder één
merk. Iedere wallpaperfamilie vereist:

- `naam` en `doel`;
- `merk`: één bestaande native merkidentiteit;
- `wallpapers`: minstens twee unieke en geordende wallpapers.

Ieder lid verwijst met `familie` wederkerig naar dezelfde familie en draagt
een unieke betekenisvolle `variant`. Alle leden gebruiken hetzelfde merk en
hebben een uniek expliciet paar `breedte` en `hoogte`. De familie bevat geen
schaalfactor, basisvariant of afleidingsregel. Lagen en assetplaatsingen blijven
eigendom van iedere afzonderlijke wallpaper.

```bp
wallpaperfamilie forge-wallpapers {
    naam: "Forge Wallpapers"
    doel: "Ordent zelfstandige ultrawide en desktopformaten."
    merk: "emberforge"
    wallpapers: ["forge-ultrawide", "forge-desktop"]
}
```

### `wallpaper`

M11.6a modelleert wallpaperintentie backendonafhankelijk. M11.6b rendert
dezelfde opgeloste context als beeld. Iedere wallpaper vereist:

- `naam` en `doel`;
- `wereld`: de wereld waaruit het thema en canvas worden opgelost;
- `merk`: de bestaande native merkidentiteit;
- optioneel `familie` en `variant`, uitsluitend samen en via een bekende
  wederkerige `wallpaperfamilie`;
- `formaat`: in deze eerste slice exact `png`;
- `breedte` en `hoogte`: canonieke positieve pixelmaten tot 16384;
- `canvas`: een bestaande semantische materiaalrol in het wereldthema;
- `lagen`: een niet-lege, unieke en geordende lijst wallpaperlagen.

De lagenlijst is wederkerig. Iedere genoemde `wallpaperlaag` verwijst terug naar
dezelfde wallpaper en iedere laag van die wallpaper staat expliciet in de
lijst.

### `wallpaperlaag`

Een wallpaperlaag vereist:

- `naam` en `doel`;
- `wallpaper`: de eigenaar van de laag;
- `rol`: `ornament`, `illustratie`, `merk` of `voorgrond`;
- `plaatsingen`: een niet-lege, unieke en geordende lijst
  assetplaatsingen.

De laagrol begrenst de toegestane native assetrol. Een ornamentlaag bevat
alleen ornamenten, een illustratielaag alleen illustraties en een merklaag
alleen logo's. De voorgrondrol kan iedere bestaande SVG assetrol dragen.

### `assetplaatsing`

Een assetplaatsing vereist:

- `naam` en `doel`;
- `laag`: de wederkerige wallpaperlaag;
- `asset`: één bestaand native SVG asset;
- `x`, `y`, `breedte` en `hoogte`: canonieke pixelgeometrie die volledig
  binnen het canvas valt;
- `fit`: `contain`, `cover` of `stretch`;
- `dekking`: een canonieke waarde tussen 0 en 1;
- `kleur`: een bestaande semantische materiaalrol uit het wereldthema.

De plaatsing bevat geen SVG geometrie, bronpad of backendveld. De resolver
koppelt de assetreferentie aan hetzelfde `ResolvedSvgAsset` dat ook de
standalone SVG producten en catalogus gebruiken.

```bp
wallpaper forge-ultrawide {
    naam: "Forge Ultrawide"
    doel: "Geordende 3840 bij 1080 wallpaperintentie."
    wereld: "palace"
    merk: "emberforge"
    formaat: "png"
    breedte: "3840"
    hoogte: "1080"
    canvas: "canvas"
    lagen: ["forge-ornamentlaag"]
}

wallpaperlaag forge-ornamentlaag {
    naam: "Ornamentlaag"
    doel: "Ordent rustige lijnornamentiek."
    wallpaper: "forge-ultrawide"
    rol: "ornament"
    plaatsingen: ["forge-node-links"]
}

assetplaatsing forge-node-links {
    naam: "Forge Node Links"
    doel: "Plaatst het native ornament binnen de canvasgrens."
    laag: "forge-ornamentlaag"
    asset: "forge-vector-node"
    x: "120"
    y: "120"
    breedte: "840"
    hoogte: "840"
    fit: "contain"
    dekking: "0.14"
    kleur: "interaction"
}
```

### `product`

Ieder product vereist:

- `naam`: menselijke naam;
- `doel`: het te genereren product;
- `backend`: de expliciete backend;
- `mode`: optioneel `interactive` of `static`; standaard `interactive`;
- `inhoud`: optioneel `composition`, `project-status`, `design-system`,
  `asset`, `asset-catalog` of `wallpaper`; standaard `composition`;
- `compositie` en `layout`: verplicht voor compositiegedragen producten;
- `asset`: verplicht en exclusief voor `inhoud: "asset"`;
- `wallpaper`: verplicht en exclusief voor `inhoud: "wallpaper"`;
- `pad`: het veilige relatieve uitvoerpad;
- `wereld`: verplicht wanneer een themalaag aanwezig is.

De productvalidator vereist dat `compositie` en `layout` exact dezelfde
componentinstanties bevatten. Een assetproduct gebruikt uitsluitend backend
`svg`, modus `static`, een bestaand SVG asset en een `.svg` uitvoerpad. Daarmee
blijft het product de enige expliciete koppeling tussen inhoud en backend,
zonder een lege compositie of layout te modelleren.

Een wallpaperproduct gebruikt modus `static`, dezelfde wereld als zijn
wallpaper en één expliciete wallpaperbackend. `wallpaper-manifest` vereist een
`.wallpaper.json` artifactpad. `wallpaper-png` vereist een `.png` artifactpad.
Beide consumeren exact dezelfde `ResolvedWallpaper`; het manifest bewijst het
contract en de PNG is het binaire beeldartifact.

### Homepage productcontract

M11.1a modelleert de Beckeringh Palace homepage als regulier native product.
De homepage heeft een eigen compositie, gridlayout en HTML-productdefinitie.
De entree en drie productroutes worden geplaatst met componentinstanties.
Er bestaat geen homepage-specifieke selectie- of layoutlogica in de backend.

M11.1b modelleert de inhoudsarchitectuur als vier native `homepagegebied`
objecten. Ieder gebied heeft een expliciete rol, leesvolgorde en kernboodschap.
Een routegebied verwijst naar precies één bestaand product of renderdoel; een
entreegebied bevat geen navigatiedoel. De componentinstanties verwijzen alleen
naar hun gebied. De compiler lost naam, doel, rol, kernboodschap, leesvolgorde
en navigatie backendonafhankelijk op voordat de generieke HTML-renderer ze
vertaalt.

M11.1c maakt de visuele hiërarchie onderdeel van dezelfde homepagegebieden.
Ieder gebied kiest expliciet een `componentrol`, `component` en `variant`.
De entree vereist de rol `hero`; routegebieden vereisen `routekaart`. De
variant lost de appearance op voordat de compositie wordt gebouwd.
Componentinstanties dupliceren deze keuzes niet. De HTML-backend ontvangt
componentrol, variant en appearance als opgeloste semantiek en schrijft die
machineleesbaar weg.

M11.4e ontsluit de native Keycloak en terminal productsurfaces met twee extra
`homepagegebied` routekaarten. Beide doelen blijven reguliere `product`
objecten met een relatief artifactpad. De bestaande resolutie bewaakt unieke
doelen, leesvolgorde, focusvolgorde en volledige-kaartgedrag. De homepage
groeit daardoor naar één entree en vijf routes zonder een tweede routetabel of
homepage-specifieke backendlogica.

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

M9.1d verwijdert daarna de dubbele componentidentiteit uit het resolved
layoutmodel. Een region bewaart uitsluitend de instantie-id en de
typegebonden plaatsing. De HTML-backend koppelt de resolved instantie en region
expliciet op id en gebruikt de compositie voor de componentklasse,
`data-instance`, `data-component` en de zichtbare instantienaam. Layoutmetadata
van de region wordt daardoor niet als instantie-inhoud gerenderd.

M9.2a introduceert daarna het native componentvariantcontract. Een variant
wijst één component en één alternatieve appearance aan. Een
componentinstantie kiest de variant expliciet en de semantische laag weigert
varianten van een ander component. `ResolvedComponentInstance` bevat de
gekozen variant en effectieve appearance. Rendererintegratie volgt in een
afzonderlijke verticale milestone.

M9.2b vertaalt die resolved variant daarna naar productuitvoer. De
HTML-backend schrijft de expliciete variant en effectieve appearance als
metadata op de componentinstantie. De component CSS-renderer genereert de
alternatieve appearance na de basiscomponent onder een selector die zowel
component als variant benoemt. De renderer leidt geen variant af en schrijft
geen presentatie terug naar BAT of CIR.

M9.2c maakt ook de gegenereerde HTML-componentcatalogus volledig. De catalogus
toont ieder basiscomponent één keer en iedere expliciete variant daarnaast
onder hetzelfde component. Variantitems gebruiken dezelfde component- en
variantklassen als productuitvoer en bewaren component-id, variant-id en
effectieve appearance-id als metadata. De catalogus leidt geen standaardvariant
af.

M9.2d legt de CSS-identiteit van componenten en varianten daarna vast in één
gedeeld renderercontract. Component CSS, product HTML en de componentcatalogus
gebruiken dezelfde deterministische omzetting van BAT-id naar componentklasse,
variantklasse en gecombineerde selector. De originele BAT-id blijft
ongewijzigd in de `data`-metadata. Het contract voegt geen BAT-velden of
impliciete varianten toe.

M9.3a introduceert daarna het native renderdoelcontract. Een renderdoel bevat
een naam, doel, formaat en veilig relatief artifactpad. De semantische laag
weigert onbekende velden en dubbele artifactpaden. Het resolved model ordent
renderdoelen deterministisch en blijft backendonafhankelijk. Deze stap leidt
nog geen renderer impliciet af uit een formaat en verandert de bestaande
productgeneratie niet.

M9.3b koppelt ieder native renderdoel via zijn expliciete id aan exact één
renderer. `compile_bat.py` doorloopt de opgeloste renderdoelen en schrijft ieder
artifact naar het gedeclareerde pad. Formaat en bestandsextensie kiezen nooit
impliciet een renderer. Een renderdoel zonder geregistreerde binding faalt
expliciet. Productdefinities blijven via hun eigen backendcontract compileren.

M11.11a voegt twee renderdoelen toe die het opgeloste EmberForge-materiaalthema
naar echte terminalconfiguratie vertalen: `emberforge-dircolors` (GNU
dircolors) en `emberforge-ps1` (bash PS1-snippet), beide in
`compiler/terminal_theme_renderer.py`. Aanleiding: Erik Post had zijn echte
bash-terminal eerder handmatig in EmberForge-kleuren gezet door de opgeloste
themawaarden één keer over te typen naar `~/.dircolors` en `~/.bashrc` — een
snapshot die stil zou blijven staan bij elke latere wijziging aan het BAT-thema.
Beide renderers lezen dezelfde opgeloste materiaalrollen
(`interaction`/`interaction-hover` voor mappen/links, `accent`/`accent-hover`
voor archieven/media, `success`/`error` voor executables/orphans) via
`resolveer_thema`, exact dezelfde route als `theme_css.py` voor productoutput.
`~/.bashrc` source't nu `output/products/emberforge-dircolors` en
`output/products/emberforge-ps1.sh` rechtstreeks in plaats van een handmatige
kopie te onderhouden: elke `compile_bat.py`-run na een themawijziging in
`world.bp` ververst de terminalkleuren automatisch, zonder handmatige stap.

M10.0a voegt de eerste Grafana-productbackend toe. De backend vertaalt een
opgeloste native grid-layout deterministisch naar het klassieke Grafana
dashboard JSON model. BAT-gridkolommen worden proportioneel op Grafana's
24-koloms raster geplaatst en iedere benoemde componentinstantie wordt een
tekstpaneel. Niet-grid-layouts falen expliciet. Datasources, queries en
operationele waarden worden niet afgeleid of verzonnen.

M10.0b koppelt het opgeloste native thema en de componentidentiteit aan het
Grafana-product. De luminantie van de expliciete `background`-themarol bepaalt
deterministisch de ondersteunde Grafana-stijl `dark` of `light`. Tekstpanelen
tonen het bestaande doel van de componentinstantie. Hun beschrijving bewaart
de BAT-identiteit van component, optionele variant en effectieve appearance.
De backend voegt geen eigen CSS, fonts, datasource of operationele waarden toe.

M10.0c vertaalt iedere opgeloste componentappearance naar een statisch Grafana
Canvas-paneel dat zonder datasource zichtbaar is. Materiaal, voorgrond, accent,
border, spacing en heading- en bodygrootte komen rechtstreeks uit het native
thema en appearancecontract. De Canvas-elementen tonen uitsluitend de bestaande
naam en het bestaande doel van de componentinstantie. Radius en schaduw worden
niet nagebootst, omdat het gebruikte Grafana Canvas-contract daarvoor geen
gelijkwaardige paneeleigenschappen biedt.

M10.1a voegt feitelijke, tijdens compilatie berekende modeltellingen toe aan
componentinstanties. Het optionele veld `metric-kind` telt objecten van één
expliciete BAT-soort; `*` telt alle gevalideerde architectuurobjecten. De
Grafana Canvas-backend toont de uitkomst als statische waarde tussen kop en
toelichting. Daardoor bevat het Forge-dashboard echte architectuurstatus zonder
datasource, queries of verzonnen operationele meetwaarden.

M10.1b maakt de opgeloste metriek backendonafhankelijk. De compositieresolutie
berekent iedere gedeclareerde modeltelling exact één keer en bewaart soort en
waarde op de opgeloste componentinstantie. Grafana consumeert uitsluitend die
waarde. De HTML-productbackend toont dezelfde waarde en toelichting, zodat beide
productuitvoeren dezelfde feitelijke dashboardinhoud uit één contract krijgen.

M10.1c voegt expliciete en backendonafhankelijke metriekdetails toe. Het veld
`metric-detail` accepteert uitsluitend `kinds` of `items` naast `metric-kind`.
`kinds` groepeert de geselecteerde objecten deterministisch per objectsoort;
`items` bewaart hun feitelijke namen in identifier-volgorde. HTML en Grafana
renderen dezelfde opgeloste details en selecteren zelf geen objecten.

M10.2a maakt ook de productidentiteit backendonafhankelijk zichtbaar. De
opgeloste compositienaam en het compositiedoel vormen in HTML en Grafana de
dashboardheader. Wereldnaam, themanaam en de deterministische status
`Gegenereerd uit BAT` komen uit de reeds opgeloste productcontext. De
HTML-backend vertaalt deze productshell responsief naar één kolom op smallere
viewports. De Grafana-backend reserveert een Canvas-header boven het native
grid en verschuift alle dashboardpanelen met een vaste headerhoogte.

M11.9c verwijdert de `Gegenereerd uit BAT`-kickerregel uit de dashboardheader
weer, in zowel HTML als Grafana. Wereld-, thema-, mode- en
snapshotidentiteit blijven volledig machineleesbaar (`data-world`,
`data-theme`, `data-product-mode`, `data-snapshot-id`, `data-snapshot-ref` op
`<body>` respectievelijk dashboardtags), maar de zelfreferentiële tekst
("gegenereerd uit BAT", productmodus als leestekst) hoort niet thuis in wat
een eindgebruiker daadwerkelijk leest.

M11.9d verwijdert ook de `compositiedoel`-paragraaf uit de dashboardheader,
opnieuw in zowel HTML als Grafana. Erik Post zag de doel-tekst nog gewoon
staan na M11.9c en wees op de bredere regel: tekst zonder toegevoegde waarde
voor wie het product gebruikt, hoort niet in de UI. `doel` blijft bestaan als
verplicht BAT-veld en als Grafana-panelbeschrijving (info-icoon, alleen op
hover zichtbaar), maar niet langer als permanent zichtbare paragraaf. Zie
[beckeringh-architectuurtaal.md](beckeringh-architectuurtaal.md) voor de
volledige regel: `naam` is eindproducttekst, `doel` is dat expliciet niet.

M10.2b voegt een gedeelde Forge-oppervlakhiërarchie toe. De native
materiaalrollen `canvas`, `surface` en `raised` verwijzen naar afzonderlijke
kleurdefinities. HTML en Grafana gebruiken daardoor uit dezelfde opgeloste
BAT-bron een Iron Black canvas, een Forged Iron dashboardheader en Raised Iron
kaarten.

M10.2c maakt ook de accenthiërarchie expliciet. De materiaalrollen `muted` en
`outline` verwijzen naar afzonderlijke native kleurdefinities. Kernwaarden en
de identiteitsrail behouden het Ember accent. Ondersteunende tekst gebruikt de
gedempte voorgrond en kaart- en detailranden gebruiken de outlinekleur. HTML en
Grafana selecteren deze kleuren niet zelf en consumeren dezelfde opgeloste
rollen.

M10.2d maakt de metriekdetails in beide backends semantisch gelijk. Detaillabels
gebruiken de gedempte voorgrond, detailwaarden gebruiken de gewone voorgrond en
scheidingslijnen gebruiken de outlinekleur. Het Ember accent blijft daardoor
beperkt tot de hoofdmetriek en de identiteitsrail. Grafana vertaalt labels,
waarden en regels naar afzonderlijke Canvas-elementen; HTML gebruikt dezelfde
opgeloste materiaalrollen.

M10.3a maakt de productmodus expliciet en backendonafhankelijk. `mode: "static"`
markeert een deterministisch gegenereerde snapshot zonder interactieve
productstatus. HTML bewaart de opgeloste modus als machineleesbare metadata.
Grafana schakelt voor een statisch product handmatige dashboardbewerking uit en
verbergt de tijdkiezer, omdat het dashboard geen tijdreeks of datasource bevat.
Producten zonder `mode` blijven voor compatibiliteit `interactive`.

M10.3b maakt dezelfde productmodus ook zichtbaar voor de gebruiker. De compiler
lost iedere gevalideerde modus op naar één vaste aanduiding:
`Statische architectuursnapshot` of `Interactief product`. HTML en Grafana
tonen die gedeelde aanduiding in hun productheader en formuleren de betekenis
van de modus niet afzonderlijk in een backend.

M10.3c lost daarnaast centraal op of een product tijdcontext heeft. Een statisch
product heeft geen tijdcontext: HTML maakt dit machineleesbaar met
`data-time-context="none"` en Grafana laat tijdzone, relatief tijdvenster en
refreshgedrag weg. Een interactief product behoudt tijdcontext en HTML markeert
dit als `data-time-context="applicable"`.

M10.3d geeft iedere statische snapshot een deterministische identiteit. De
compiler berekent daarvoor een SHA-256 hash over de canoniek geordende,
gevalideerde architectuurobjecten, zonder bronlocaties of uitvoeromgeving.
HTML en Grafana tonen dezelfde eerste twaalf hexadecimale tekens als compacte
snapshotidentiteit. HTML bewaart daarnaast de volledige hash in
`data-snapshot-id`. Dezelfde architectuurinhoud levert daardoor steeds dezelfde
identiteit op en iedere inhoudswijziging een andere. Interactieve producten
hebben geen snapshotidentiteit.

M10.3e maakt de volledige snapshotidentiteit backendonafhankelijk
verifieerbaar. De compiler lost deze eenmaal op als canonieke referentie
`sha256:<volledige hash>`. HTML bewaart de referentie in `data-snapshot-ref`
en Grafana in de dashboardtags. Beide backends gebruiken daarmee exact dezelfde
machineleesbare verificatiewaarde en stellen het algoritme niet zelf samen.
Interactieve producten hebben geen snapshotreferentie.

M10.4c introduceert `inhoud: "project-status"` als expliciete,
contextafhankelijke productinhoud. De HTML backend rendert de getypeerde
`ProjectStatus` die de compiler aanlevert en leest `project/status.json` niet
zelf. Het product toont de totale architectuurschatting, de milestoneketen en
ieder productgebied met bewijs en resterend werk. Compilatie zonder
projectstatuscontext blijft bestaande producten ondersteunen en selecteert
contextafhankelijke statusproducten niet.

M10.4d ontsluit dezelfde getypeerde `ProjectStatus` als importeerbaar Grafana
dashboard. De Grafana backend rendert de totale architectuurschatting, de
milestoneketen en alle productgebieden zonder de normatieve JSON bron te lezen
of percentages te berekenen. Schema en totale voortgang staan daarnaast als
machineleesbare dashboardtags vast. HTML en Grafana blijven contextafhankelijke
statusproducten en worden zonder statuscontext beide overgeslagen.

M10.5a introduceert native dashboardinformatiearchitectuur. Een
`informatiegebied` bundelt een niet-lege, unieke lijst native objectsoorten
onder één naam en doel. Objectsoorten mogen ook nog nul voorkomens hebben in de
actuele snapshot, zodat de structuur stabiel blijft terwijl de wereld groeit.
Verschillende informatiegebieden mogen dezelfde objectsoort niet claimen.

Een componentinstantie kiest met `informatiegebied` exact één gebied. Dit veld
kan niet worden gecombineerd met `metric-kind` of `metric-detail`. De
compositieresolutie selecteert en telt de gebiedsinhoud één keer en levert naam,
doel, totaal en uitsplitsing per objectsoort backendonafhankelijk aan HTML en
Grafana. Het Forge Dashboard bestaat daardoor uit Wereld en identiteit, Forge
ontwerpsysteem en Productfamilie in plaats van drie losse technische tellingen.

M10.5b verbindt ieder informatiegebied met een expliciete, geordende lijst
`navigatie`. Een navigatiedoel is een bestaand `product` of `renderdoel` en
wordt door maximaal één informatiegebied geclaimd. De informatielaag lost id,
naam, doelsoort en artifactpad vóór backendselectie op. HTML rendert relatieve
productlinks en Grafana rendert dezelfde doelen als Canvas-links. Backends
zoeken daardoor geen producten of catalogi en leiden geen paden af uit
objectsoorten.

M10.5c geeft ieder informatiegebied daarnaast een expliciete, geordende lijst
`inhoud`. Ieder inhoudsanker verwijst naar een bestaand object waarvan de soort
door dat informatiegebied wordt geclaimd. De informatielaag lost id, naam,
objectsoort en doel vóór backendselectie op. Hetzelfde object mag niet door
meerdere gebieden als inhoudsanker worden gebruikt.

HTML en Grafana tonen dezelfde zeven geselecteerde kernobjecten naast tellingen,
soortverdeling en productnavigatie. De selectie en volgorde komen volledig uit
BAT. Backends kiezen daardoor geen voorbeelden op basis van aantallen,
objectsoorten of toevallige bronvolgorde.

M10.5d legt voor ieder informatiegebied daarnaast een expliciet
`toegankelijkheidslabel` en een positieve `leesvolgorde` vast. De leesposities
zijn uniek en vormen over alle informatiegebieden een aaneengesloten reeks.
De informatielaag draagt beide waarden via de opgeloste compositie naar iedere
backend.

HTML ordent de informatiegebieden in deze leesvolgorde in de DOM en schrijft
het label als `aria-label` en de positie als `data-reading-order`. De visuele
gridplaatsing blijft uit de native layout komen. Grafana gebruikt hetzelfde
label als paneeltitel en bewaart label en leespositie in de paneelbeschrijving.
Geen backend leidt toegankelijkheidssemantiek af uit kolompositie, naam of
bronvolgorde.

M11.1d legt responsief gedrag vast in dezelfde native productketen. Een
grid-layout kan alleen samen een positief `responsive-breakpoint` en
`compact-columns` declareren. Iedere bijbehorende region krijgt dan precies één
positieve `compact-order`; alle compacte posities vormen een aaneengesloten
reeks. De homepagegebieden leggen daarnaast `focusvolgorde` en
`navigatiegedrag` vast. De entree is niet focusbaar en heeft gedrag `geen`.
Routegebieden hebben een positieve focusvolgorde en gedrag `volledige-kaart`.

De generieke HTML-renderer vertaalt uitsluitend deze opgeloste intentie naar
een mediaquery, compacte gridplaatsing en machineleesbare attributen. DOM- en
focusvolgorde blijven afkomstig uit de native informatiearchitectuur. De
backend kiest geen breakpoint, herschikking of navigatiegedrag.

De totale projectvoortgang wordt vanaf M11.1d niet meer opgeslagen. Ieder
productgebied declareert een geheel percentage en een positief geheel gewicht.
De gewichten tellen exact op tot 100. De projectstatuslaag berekent het gewogen
totaal één keer met deterministische afronding en levert dezelfde waarde aan
Markdown, HTML en Grafana.

M11.3a introduceert een gecontroleerd ontwerpbroncontract voor het aangeleverde
EmberForge Design System. Het contract legt bronidentiteit, inventaris,
mappingstatus, bewijs en uitsluitingen vast. Externe ontwerpinput is expliciet
niet normatief, mag geen runtimeafhankelijkheden introduceren en wordt alleen
actief via een afzonderlijke BAT-migratie.

De gapanalyse maakt onderscheid tussen mapbare, gedeeltelijk mapbare,
besluitplichtige en geblokkeerde onderdelen. Daardoor worden voorbeeldcode,
placeholder assets, ontbrekende bestanden en externe CDN bronnen niet
stilzwijgend onderdeel van een product of renderer.

M11.1e activeert voor het eerst gecontroleerde ontwerpinput in een product.
EmberForge is een native `merk` met een expliciete tagline, kernbelofte, drie
principes, productfamilie, taal en stem. Alleen een homepagegebied met rol
`entree` verwijst naar deze identiteit; routegebieden mogen haar niet
dupliceren.

De merksemantiek wordt vóór backendselectie opgelost en via de native
compositie doorgegeven. De generieke HTML backend rendert uitsluitend deze
opgeloste velden. Externe ontwerpbestanden, logoassets, fonts en voorbeeldcode
blijven buiten de runtimeketen.

M11.3b migreert het geverifieerde EmberForge palet naar native kleur, palet,
materiaal en tokenobjecten. Deep Night Blue vormt het canvas, Graphite en Steel
Blue dragen de oppervlakken, Sky is de primaire interactiekleur en Ember Copper
blijft het spaarzame warme accent. Succes, waarschuwing en fout hebben eigen
semantische rollen. HTML en Grafana gebruiken dezelfde opgeloste waarden en
lezen het externe bronpakket niet.

M11.3c migreert de productgedragen semantische rollen voor spacing, radius,
border, shadow en motion naar native BAT. De bestaande rolnamen blijven de
stabiele interface voor appearances en renderers. Hun waarden volgen de
geverifieerde EmberForge bron: een 4px ruimtebasis, zachte afronding, 1px
lijnen, donkere elevaties en rustige motion met de standaard easing.
Bronstappen zonder productrol worden niet als ongebruikte velden toegevoegd.

M11.3d migreert de EmberForge art direction naar één native object onder het
thema. Het contract resolveert canvas, interactiekleur en warme accentkleur
naar canonieke kleuren en begrenst koper tot maximaal twee warme punten per
view. Gecontroleerde gloed, technische lijnvoering, ruime dichtheid en
isometrische lijnkunst zijn expliciete waarden. De HTML backend gebruikt alleen
de opgeloste art direction voor halo's, ornamentiek en metadata.

M11.3e migreert de EmberForge typografie naar geordende fontstacks onder het
native `typografie` object. Koppen gebruiken Orbitron, interface en lopende
tekst gebruiken Inter en technische tekst gebruikt JetBrains Mono. Iedere
stack eindigt in een expliciete generieke fallback en de levering is
`local-only`. Externe URL's, imports en fontdownloads zijn semantisch verboden.

De native typeschaal bevat alleen de rollen die producten daadwerkelijk
dragen: display, title, heading, body, label en caption. HTML rendert de
opgeloste stacks als CSS en schrijft typografie en leveringsbeleid als metadata
uit. De backend leest geen ontwerpbron en maakt geen zelfstandige fontkeuze.

M11.3f migreert de geverifieerde EmberForge componenttoestanden voor het
bestaande Forge-paneel. De rusttoestand gebruikt het vaste kaartprofiel. Hover
gebruikt een cyaan outline, de bronbewezen gloed en een offset van min één
pixel. Focus gebruikt dezelfde gloed zonder verplaatsing. Pressed gebruikt de
donkerdere cyaanrol, keert terug naar nul pixel en schaalt niet. Disabled
gebruikt een gedempte voorgrond, geen gloed en geen verplaatsing.

De variant koppelt alle vijf toestanden expliciet aan appearances.
`ResolvedComponentVariant` en `ResolvedComponentInstance` dragen de geordende
mapping backendonafhankelijk. De component CSS-renderer vertaalt haar naar de
standaard browserstates en expliciete catalogusklassen. HTML publiceert de
mapping als metadata. Grafana bewaart dezelfde mapping in de
paneelbeschrijving en simuleert geen interactie die Canvas niet ondersteunt.

M11.3g breidt het componentcontract uit met een semantische `rol` en expliciete
`anatomie`. De native rollen paneel, actie, invoer, status, app tegel en
statistiek hebben ieder een vaste geordende set inhoudssleuven. De semantische
laag weigert onbekende rollen, lege of dubbele anatomie en een anatomie die
niet bij de gekozen rol past.

Het nieuwe native `componentvoorbeeld` koppelt één component aan één variant
en bewaart de productgedragen voorbeeldinhoud. Verplichte en toegestane velden
worden per componentrol gecontroleerd. De resolver levert component, rol,
anatomie, variant, label en optionele waarde, beschrijving, melding en status
als één backendonafhankelijk contract.

De componentcatalogus vertaalt het opgeloste contract naar passende HTML
elementen en schrijft rol, anatomie, variant, toestand en appearance als
metadata uit. De component CSS renderer vertaalt alleen de semantische rol naar
structuur en gebruikt voor iedere visuele waarde de appearance en het
opgeloste thema. Voorbeeldtekst, EmberForge bronwaarden en UI kit code worden
niet in een renderer opgenomen.

M11.3h introduceert het native `toegankelijkheid` object. Ieder component met
een semantische rol en anatomie verwijst expliciet naar één contract. Dat
contract legt rol, naambron, optionele waarde- en foutbron, disabled gedrag,
focusdeelname en toetsenbordgedrag vast. De semantische laag weigert een
ontbrekende referentie, bronnen buiten de componentanatomie en gedrag dat niet
bij de componentrol past.

`ResolvedComponentAccessibility` wordt toegevoegd aan zowel
`ResolvedComponentExample` als `ResolvedComponentInstance`. De
componentcatalogus rendert acties en app tegels als native buttons en invoer als
een native input met expliciete label- en foutkoppeling. Niet-interactieve
statussen, statistieken en panelen krijgen geen tabstop. Product HTML schrijft
de opgeloste semantiek als metadata uit en benoemt groepen via zichtbare
koppen. Grafana bewaart hetzelfde contract in de paneelbeschrijving en
simuleert geen interactie.

De contracten volgen native hostsemantiek en de W3C WAI patronen voor
[buttons](https://www.w3.org/WAI/ARIA/apg/patterns/button/),
[toegankelijke namen](https://www.w3.org/WAI/ARIA/apg/practices/names-and-descriptions/)
en [formuliermeldingen](https://www.w3.org/WAI/tutorials/forms/notifications/).
M11.3h bewijst geen compatibiliteit met specifieke hulptechnologie.

M11.3i introduceert het native `referentiesectie` object en
`inhoud: "design-system"` voor producten. Het statische EmberForge
referentieproduct declareert precies vijf geordende rollen: primitives, tokens,
toestanden, voorbeelden en toegankelijkheid. De semantische laag weigert
ontbrekende secties, dubbele rollen, een afwijkende volgorde en een
interactieve productmodus.

De productcompiler lost de secties samen met alle getypeerde tokens,
appearances, componenten, varianten, voorbeelden en
toegankelijkheidscontracten op vóór backendselectie. De HTML backend vertaalt
deze context naar één navigeerbaar product. State previews gebruiken dezelfde
native hostsemantiek en CSS identiteit als productcomponenten. De voormalige
`html-components` renderdoelbinding is verwijderd; `components.html` wordt nu
uitsluitend door `forge-design-system-reference-html` gegenereerd.

M11.4a laat een `componentinstantie` optioneel naar één gevalideerd
`componentvoorbeeld` verwijzen. Component, variant, appearance,
toegankelijkheid en inhoud worden dan gezamenlijk uit dat voorbeeld opgelost.
Losse component, variant, metriek, informatiegebied, homepagegebied of
navigatievelden zijn daarmee niet combineerbaar.

Het EmberForge homelab dashboard gebruikt dit contract voor vier
statistiekkaarten, vier statussen en twee app tegels. De native gridlayout
ordent deze op vier kolommen en schakelt onder 960 pixels naar twee kolommen
met een expliciete compacte leesvolgorde. De HTML backend vertaalt alleen de
resolved voorbeeldinhoud en bevat geen homelab bronwaarden.

M11.4b voegt voor dezelfde compositie en native gridlayout een expliciet
Grafana product toe. De backend ontvangt dezelfde tien opgeloste instanties als
HTML en vertaalt labels, waarden, variants, states en
toegankelijkheidscontracten naar Canvas panelen en paneelmetadata. Het
dashboard bevat geen datasource; de voorbeeldwaarden blijven normatieve
productinhoud en worden niet als actuele telemetrie gepresenteerd.

M11.10a doorbreekt die "geen datasource"-regel, expliciet en uitsluitend voor
componentinstanties die dat zelf declareren. Het nieuwe native object
`databron` (`naam`, `doel`, `expr`, `eenheid`, optioneel `mapping`) legt een
deterministische PromQL-expressie vast; de componentinstantie krijgt daarmee
optioneel een `databron`-veld, los te combineren met `voorbeeld`. De
World Model beslist wélke query bij een componentinstantie hoort
(compileertijd, reproduceerbaar); de Grafana-backend beslist wélke
Prometheus-instantie die query op kijktijd uitvoert
(`PROMETHEUS_DATASOURCE_UID` in `compiler/backends/grafana.py`, een
omgevingsfeit, geen wereldfeit). Canvas-tekstelementen krijgen `text.mode:
"field"` in plaats van `"fixed"`; teksteenheden krijgen een Grafana
`fieldConfig`-waardemapping (bijvoorbeeld `1` naar `Healthy`). Alle tien
Observatory-componentinstanties krijgen zo een `databron` gekoppeld aan echte
Prometheus/kube-state-metrics-telemetrie op het K3s-cluster. De HTML-backend
consumeert `databron` niet en blijft daardoor volledig statisch: hetzelfde
product levert twee eerlijk verschillende garanties, een reproduceerbare
snapshot en een live dashboard, uit dezelfde opgeloste compositie. Elk ander
Grafana-product zonder expliciete `databron` (Forge Dashboard,
Projectstatus) blijft zonder datasource; de regel uit M10.0a/M10.0c/M11.4b
staat daarmee nog steeds, alleen niet meer zonder uitzondering.

M11.10a maakt ook de Grafana-rijhoogte inhoudsgedreven in plaats van een vaste
aanname. De vorige vaste rijhoogte was oorspronkelijk gekalibreerd op de
langste bekende paneelinhoud (Forge Dashboard's informatiegebieden) en maakte
daardoor elk ander paneel, waaronder Observatory's statkaarten, veel groter
dan nodig. De backend berekent nu per product de werkelijk benodigde
rijhoogte uit de opgeloste Canvas-inhoud van elk paneel (`_rijhoogte_eenheden`
in `compiler/backends/grafana.py`), inclusief Grafana's eigen vaste
paneelkoptekst. Dat onthulde bovendien dat Forge Dashboard's panelen al vóór
deze milestone te weinig ruimte kregen (988px benodigd tegen 600px
toegekend) en dus zichtbaar afgekapt waren zodra iemand het dashboard
daadwerkelijk live opende; die overflow is met dezelfde berekening opgelost.

Erik Post zag het live geïmporteerde Observatory-dashboard daarna en meldde
twee dingen: elke paneltitel stond er dubbel (Grafana's eigen koptekstbalk
toonde exact dezelfde naam als de gebrande Canvas-heading eronder), en onder
elke statkaart stond alsnog een parafrase van diezelfde naam ("Running" met
daaronder "Aantal actieve workloads"). Beide zijn opgelost, niet alleen voor
Observatory maar voor elk Grafana-product. Een spike tegen de echte
Grafana-instantie bevestigde eerst dat een lege paneltitel (`"title": ""`)
Grafana's koptekstbalk volledig laat wegvallen in plaats van een lege balk
achter te laten; `GRAFANA_PANEL_HEADER_PX` gaat daarom naar 0 en elk paneel
(inclusief de dashboardheader en Forge Dashboard/Projectstatus) krijgt een
lege `title`. Het canvas-`-body`-element dat `instantie.doel` toonde is
verwijderd uit `_canvasopties`; hetzelfde geldt voor de HTML-backend's
`bp-description`-paragraaf (`compiler/native_layout_html_renderer.py`), die
`instantie.doel` toonde voor informatiegebied-gedreven producten zoals
Forge Dashboard. Zie
[beckeringh-architectuurtaal.md](beckeringh-architectuurtaal.md) voor de
volledige regel.

Erik Post voegde daarna een derde, bredere eis toe: alle eindproducttekst is
Nederlands, ook waar de brondata (Kubernetes, Prometheus) Engelse termen
gebruikt. Observatory's `naam`-, `label`-, `waarde`- en
databron-`mapping`-velden zijn vertaald ("Running" naar "Actief", "CPU
Usage" naar "CPU-gebruik", een Grafana-waardemapping van `1` naar "Gezond"
in plaats van "Healthy"). Eigennamen (`ISMS Challenger`, `CV Tool`, `The
Observatory`) en gangbare Nederlandse IT-leenwoorden (`cluster`, `node`)
blijven staan. De rest van de productfamilie (Keycloak-loginformulier,
Design System Reference's kleur-/tokennomenclatuur) is nog niet
meegenomen; dat is een expliciet openstaande, nog niet gescopete
vervolgstap.

M11.4c modelleert de EmberForge Keycloak login als een tweede concrete
productsurface. Een compositie kan daarvoor de expliciete rol
`login-formulier` dragen. Componentvoorbeelden leggen het native
`invoertype` (`text`, `email` of `password`) en `actietype` (`button` of
`submit`) backendonafhankelijk vast. HTML vertaalt deze contracten naar een
`form`, gelabelde native invoerelementen en een submitbutton. Het product
bevat geen realm, client-ID, endpoint, sessiegedrag of credentials en claimt
daarom uitsluitend de productsurface, niet een werkende Keycloak integratie.

M11.4d modelleert de EmberForge terminal als een derde concrete
productsurface. De componentrol `terminal` vereist vensterchrome, tabs,
identiteit, geordende systeemvelden en promptinhoud. Het
`componentvoorbeeld` bewaart deze bronwaarden getypeerd; de compositierol
`terminal-sessie` plaatst precies dit opgeloste voorbeeld in een statische
stacklayout.

De HTML backend rendert een benoemde, niet-interactieve groep met een
definitielijst voor de systeemvelden. Vensterknoppen en tabs zijn visuele
bronweergaven en geen controls. Het product voert geen shell uit en behandelt
de voorbeeldwaarden niet als actuele telemetrie.

M11.4e neemt `Terminal` op in de native EmberForge productfamilie en verbindt
de Keycloak en terminal producten via afzonderlijke homepagegebieden. De
gegenereerde links gebruiken uitsluitend de reeds opgeloste product-id, naam
en het veilige relatieve artifactpad.

M11.5a introduceert `ResolvedSvgAsset` als afzonderlijke productcontext. De
eerste verticale slice modelleert `emberforge-vector-node` als decoratief
technisch lijnornament en genereert
`output/products/emberforge-vector-node.svg`. De SVG backend schrijft alleen
vaste SVG elementen en attributen, draagt de statische model snapshot en leest
geen bronbestand of externe ontwerpinput.

M11.5b introduceert `ResolvedSvgAssetCatalog` als backendonafhankelijke
cataloguscontext. Een product met inhoud `asset-catalog` declareert de volledige
geordende lijst native assets zelf. De resolver koppelt ieder item aan exact één
statisch SVG product. De HTML backend rendert uitsluitend de opgeloste assets
als veilige previews, contractmetadata en relatieve artifactlinks in
`output/products/assets.html`.

De standalone SVG backend en de cataloguspreview gebruiken dezelfde veilige
serialisatie. De catalogus bevat daardoor geen gekopieerde padgeometrie,
handmatig onderhouden routetabel, ruwe SVG markup of externe bron.

M11.5c voegt vier informatieve assets aan diezelfde keten toe:
`emberforge-icon-dashboard`, `emberforge-icon-identity`,
`emberforge-icon-terminal` en `emberforge-icon-assets`. Zij delen een 24 bij 24
viewbox, `currentColor`, geen vulling, een lijndikte van 1,5 en ronde
lijnuiteinden en verbindingen. Ieder asset krijgt precies één statisch SVG
product en één catalogusvermelding.

M11.5d voegt `emberforge-merkteken` en `emberforge-woordmerk` toe als de twee
verplichte varianten van `emberforge-merkassets`. De bestaande iconen zijn
tegelijk onder `emberforge-iconen` gebracht. Beide families zijn expliciet,
wederkerig, merkgebonden en worden vóór HTML rendering opgelost. Het merkteken
en woordmerk zijn nieuwe BAT geometrie en activeren geen placeholder uit de
ontwerpinput.

M11.6a introduceert `ResolvedWallpaper`, `ResolvedWallpaperLayer` en
`ResolvedWallpaperAssetPlacement` als één geordende productcontext. De eerste
EmberForge specificatie kiest een 3840 bij 1080 canvas, twee lagen en vier
plaatsingen van bestaande native assets. De `wallpaper-manifest` backend
publiceert deze context deterministisch als
`output/products/emberforge-ultrawide.wallpaper.json`. Er wordt in deze
milestone geen wallpaperafbeelding gegenereerd.

M11.6b maakt de kleurkeuze per plaatsing expliciet als semantische
materiaalrol en voegt `wallpaper-png` toe. De backend ondersteunt de veilige
SVG padcommando's, respecteert `contain`, `cover`, `stretch`, lijncontracten,
laagvolgorde, clipping en dekking en schrijft een deterministische PNG zonder
tijdstempel. De encoder gebruikt waar mogelijk een compact geïndexeerd
kleurenpalet en deterministische zlibcompressie. Het eerste beeldartifact is
`output/products/emberforge-ultrawide.png` van exact 3840 bij 1080 pixels.

M11.6c voegt `ResolvedWallpaperFamily` toe en maakt de bestaande ultrawide
wallpaper en een nieuwe 1900 bij 1200 desktopwallpaper wederkerige leden van
`emberforge-wallpapers`. Beide varianten hebben eigen lagen, plaatsingen,
manifest en PNG product. De manifesten publiceren familie en variant. De PNG
metadata draagt dezelfde identiteit. Assets en backends worden hergebruikt
zonder coördinaten of schaalregels tussen de varianten te delen.

M11.6d introduceert `ResolvedMusicCircle`. Het BAT object `muziekcirkel`
publiceert exact twaalf majeurtoonsoorten, relatieve mineurtoonsoorten en
voortekens. Afwijkende volgorde of inhoud faalt semantisch. De resolver bouwt
hieruit drie ringen, twaalf sectoren en vectorglyphs. De resulterende
`ResolvedSvgAsset` wordt via een gewone `assetplaatsing` aan iedere wallpaper
gekoppeld. De PNG backend kent daardoor geen toonsoorten en verzint geen tekst.

M11.6e voegt een expliciet beeldeffect toe aan
`ResolvedWallpaperAssetPlacement`. `solid` blijft de standaard.
`radial-glow` is alleen een opgeloste falloff-intentie; asset, kleurrol,
dekking en geometrie blijven afzonderlijke BAT velden en worden ook in het
wallpapermanifest gepubliceerd. Beide wallpaperformaten componeren hiermee
eigen koelblauwe lichtvelden en exact twee begrensde warme accenten.

M11.6f gebruikt het bestaande assetcontract en wallpapercontract zonder nieuwe
renderersemantiek voor wereldsymboliek. `emberforge-palace` en
`emberforge-beaver` zijn illustraties zonder vulling; `emberforge-nordic-weave`
is ornamentiek zonder vulling. Ieder asset wordt als zelfstandig SVG product en via
de bestaande catalogus gepubliceerd. Beide wallpaperformaten hebben een eigen
wereldlaag en eigen plaatsingen. De muzieklaag blijft erboven staan en de
Circle of Fifths behoudt exact haar M11.6d geometrie.

M11.7a introduceert `ResolvedFigmaMaster` als productcontext voor de eerste
Figma verticale slice. BAT selecteert expliciet de wereld, assets, componenten,
varianten, composities en layouts. De resolver koppelt daar hetzelfde opgeloste
thema aan dat HTML, Grafana en wallpaperproducten al gebruiken. De
`figma-manifest` backend schrijft vervolgens een statisch
`output/products/emberforge-master.figma.json` met snapshotidentiteit,
theme waarden, vectorgeometrie, component appearances en states en de native
surface-layouts. Er wordt nog geen Figma bestand gewijzigd en de backend bevat
geen eigen designwaarden.

M11.7b maakt de foundationsemantiek volledig genoeg voor een domme,
idempotente Figma adapter. Iedere typeschaalrol bevat naast grootte expliciet
de fontrol, weight, line height en letter spacing. Semantische palette en
material kleuren publiceren hun native kleur-ID naast de opgeloste waarde en
het Figma manifest publiceert de gebruikte kleurprimitives afzonderlijk.
`schema_version: 2` kan daardoor native Figma aliases en volledige text styles
opbouwen zonder waarden of fontkoppelingen te raden.

De synchronisatieadapter zelf is een lokale Figma development plugin. De
compiler verpakt `emberforge-master.figma.json` deterministisch in
`output/products/figma-plugin/code.js`; het bijbehorende `manifest.json`
declareert uitsluitend Figma design, dynamic page access en geen
netwerktoegang. Er is daarmee geen MCP-, REST- of netwerkruntime nodig. De
adapter vertaalt schema v2 naar acht single-mode foundation collections, zes
text styles, zeven effect styles, elf SVG assets, zeven componentfamilies en
de geselecteerde composition-layout surfaces. De twintig BAT variantprofielen
worden daarbij uitgewerkt tot 57 concrete statevarianten.

De lokaal gegenereerde plugin is een adapterartifact en geen nieuwe normatieve
bron. Een door Figma toegekende publicatie-identiteit, het draaien van de plugin
in Figma Desktop en visuele inspectie van het resulterende masterbestand zijn
externe lifecyclehandelingen en veranderen BAT niet.

M11.7c laat de development plugin na de eerste synchronisatie de beheerde Figma
toestand opnieuw uitlezen. De verificatie controleert de acht collections en
hun variables, text en effect styles, componentsets en concrete statevarianten,
assets en surfaces tegen hetzelfde schema-v2 manifest en controleert de
snapshotidentiteit op de beheerde documentatie, componenten en assets. De plugin
voert vervolgens dezelfde synchronisatie nogmaals uit en vereist een identieke
live fingerprint. Daarmee is idempotentie een runtimecontrole in het echte
Figma bestand in plaats van alleen een eigenschap van de adapterplanning. De
visuele beoordeling van het resultaat blijft een expliciete externe
lifecyclecontrole en kan niet door de netwerkloze adapter worden vervangen.

## Diagnostics

| Code | Betekenis |
|---|---|
| `BP3506` | Product verwijst naar een onbekende of ontbrekende compositie |
| `BP3507` | Compositie en layout bevatten niet exact dezelfde instanties |
| `BP3508` | Product gebruikt een onbekende modus |
| `BP3509` | Product gebruikt een onbekende inhoudsbron |
| `BP3510` | Assetproduct verwijst naar een onbekend of ontbrekend asset |
| `BP3511` | Assetproduct gebruikt niet de SVG backend |
| `BP3512` | Assetproduct is niet statisch |
| `BP3513` | Assetproduct declareert compositie-, layout- of referentievelden |
| `BP3514` | Assetproduct gebruikt geen `.svg` uitvoerpad |
| `BP3515` | Niet-assetproduct gebruikt een asset of SVG backend |
| `BP3516` | Figma product verwijst naar een onbekende of ontbrekende Figma master |
| `BP3517` | Figma product gebruikt niet de `figma-manifest` backend |
| `BP3518` | Figma product declareert inhoud buiten de expliciete masterreferentie |
| `BP3519` | Figma product is niet statisch |
| `BP3520` | Figma product gebruikt geen `.figma.json` uitvoerpad |
| `BP3521` | Figma product en Figma master gebruiken niet dezelfde wereld |
| `BP3522` | Een ander producttype probeert de Figma master of backend te gebruiken |
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
| `BP3618` | Responsief gridcontract mist breakpoint of compact kolomaantal |
| `BP3619` | Responsief gridcontract bevat geen positief geheel getal |
| `BP3630` | Art direction verwijst naar een onbekende semantische kleurrol |
| `BP3631` | Art direction begrenst warme accenten niet op één of twee |
| `BP3632` | Art direction gebruikt een onbekende visuele modus |
| `BP4401` | Figma master bevat een onbekend veld |
| `BP4402` | Figma master verwijst naar een onbekende wereld |
| `BP4403` | Figma master mist een expliciete niet-lege referentielijst |
| `BP4404` | Figma master bevat een dubbele referentie |
| `BP4405` | Figma master bevat een onbekende objectreferentie |
| `BP4406` | Figma master selecteert een variant zonder diens component |
| `BP4407` | Figma mastercompositie gebruikt een component buiten de selectie |
| `BP4408` | Figma masterlayout gebruikt een instantie buiten de geselecteerde composities |
| `BP4409` | Figma mastercompositie gebruikt een variant buiten de selectie |
| `BP3640` | Typografie gebruikt geen expliciete `local-only` levering |
| `BP3641` | Typografierol bevat geen geldige unieke fontstack |
| `BP3642` | Typografierol bevat een externe fontbron |
| `BP3643` | Typografierol eindigt niet in de vereiste generieke fallback |
| `BP3644` | Typeschaal mist een expliciete fontrol of typografiemetriek |
| `BP3645` | Typeschaal bevat een ongeldige fontrol of typografiemetriek |
| `BP3633` | Thema verwijst naar een onbekende art direction |
| `BP3634` | Thema activeert art direction zonder expliciet materiaal |
| `BP3620` | Compact grid heeft meer kolommen dan het brede grid |
| `BP3621` | Responsieve region mist een positieve compacte volgorde |
| `BP3622` | Compacte regionvolgorde is niet aaneengesloten |
| `BP3701` | Compositie heeft een onbekende eigenschap |
| `BP3702` | `instanties` is niet expliciet, uniek of geldig |
| `BP3703` | Compositie verwijst naar een onbekende componentinstantie |
| `BP3704` | Componentinstantie verwijst niet terug naar de compositie |
| `BP3705` | Compositie gebruikt een onbekende semantische rol |
| `BP3710` | Componentinstantie heeft een onbekende eigenschap |
| `BP3711` | Componentinstantie verwijst naar een onbekende compositie |
| `BP3712` | Compositie noemt de componentinstantie niet |
| `BP3713` | Componentinstantie verwijst naar een onbekend component |
| `BP3714` | Componentinstantie heeft een ongeldige `metric-kind` |
| `BP3715` | Componentinstantie telt een onbekende objectsoort |
| `BP3716` | Componentinstantie heeft een ongeldige `metric-detail` |
| `BP3717` | Componentinstantie verwijst naar een onbekend informatiegebied |
| `BP3718` | Componentinstantie combineert een informatiegebied met legacy metriekvelden |
| `BP3719` | Componentinstantie verwijst naar een onbekend componentvoorbeeld |
| `BP3720` | Componentinstantie combineert voorbeeldinhoud met losse inhoudsvelden |
| `BP3721` | Componentinstantie verwijst naar een onbekende databron |
| `BP3801` | Variant heeft een onbekende eigenschap |
| `BP3802` | Variant verwijst naar een onbekend component |
| `BP3803` | Variant verwijst naar een onbekende appearance |
| `BP3804` | Componentinstantie verwijst naar een onbekende variant |
| `BP3805` | Variant hoort niet bij het component van de componentinstantie |
| `BP3806` | Variant declareert een onvolledig statecontract |
| `BP3807` | Componentstate verwijst naar een onbekende appearance |
| `BP3220` | Component gebruikt een onbekende semantische rol |
| `BP3221` | Component heeft geen geldige unieke anatomie |
| `BP3222` | Componentanatomie past niet bij de semantische rol |
| `BP3820` | Componentvoorbeeld heeft een onbekende eigenschap |
| `BP3821` | Componentvoorbeeld verwijst naar een onbekend component |
| `BP3822` | Componentvoorbeeld verwijst naar een onbekende variant |
| `BP3823` | Componentvoorbeeld gebruikt een variant van een ander component |
| `BP3824` | Componentvoorbeeld mist verplichte rolgebonden inhoud |
| `BP3825` | Componentvoorbeeld bevat inhoud die niet bij de rol past |
| `BP3826` | App tegelvoorbeeld gebruikt een onbekende operationele status |
| `BP3827` | Invoervoorbeeld gebruikt een onbekend of rolvreemd invoertype |
| `BP3828` | Actievoorbeeld gebruikt een onbekend of rolvreemd actietype |
| `BP3829` | Terminalvoorbeeld heeft een onvolledig of inconsistent inhoudscontract |
| `BP3830` | Toegankelijkheidscontract heeft een onbekende eigenschap |
| `BP3831` | Toegankelijkheidscontract heeft een ongeldige contractwaarde |
| `BP3832` | Component mist een bestaand toegankelijkheidscontract |
| `BP3833` | Toegankelijkheidsrol past niet bij de componentrol |
| `BP3834` | Naam-, waarde- of foutbron past niet bij de componentanatomie |
| `BP3835` | Disabled gedrag past niet bij de componentrol |
| `BP3836` | Focusgedrag past niet bij de componentrol |
| `BP3837` | Toetsenbordgedrag past niet bij de componentrol |
| `BP3840` | Referentiesectie heeft een onbekende eigenschap |
| `BP3841` | Referentiesectie gebruikt een onbekende semantische rol |
| `BP3842` | Designsystemproduct mist geldige unieke referentiesecties |
| `BP3843` | Designsystemproduct bevat niet exact de vereiste geordende rollen |
| `BP3844` | Designsystemproduct is niet statisch |
| `BP3845` | Regulier product gebruikt ten onrechte referentiesecties |
| `BP3846` | Designsystemproduct heeft niet exact één inhoudsinstantie |
| `BP3901` | Renderdoel heeft een onbekende eigenschap |
| `BP3902` | Renderdoel mist een geldig formaat |
| `BP3903` | Renderdoel heeft geen veilig relatief artifactpad |
| `BP3904` | Meerdere renderdoelen gebruiken hetzelfde artifactpad |
| `BP4001` | Informatiegebied heeft een onbekende eigenschap |
| `BP4002` | Informatiegebied heeft geen geldige unieke soortenlijst |
| `BP4003` | Informatiegebied bevat een onbekende, niet-native of recursieve objectsoort |
| `BP4004` | Objectsoort komt voor in meerdere informatiegebieden |
| `BP4005` | Informatiegebied heeft geen geldige unieke navigatielijst |
| `BP4006` | Informatiegebied verwijst naar een onbekend navigatiedoel |
| `BP4007` | Navigatiedoel is geen product of renderdoel |
| `BP4008` | Navigatiedoel komt voor in meerdere informatiegebieden |
| `BP4009` | Informatiegebied heeft geen geldige unieke inhoudslijst |
| `BP4010` | Informatiegebied verwijst naar een onbekend inhoudsanker |
| `BP4011` | Inhoudsanker valt buiten de objectsoorten van het informatiegebied |
| `BP4012` | Inhoudsanker komt voor in meerdere informatiegebieden |
| `BP4013` | Informatiegebied mist een betekenisvol toegankelijkheidslabel |
| `BP4014` | Informatiegebied mist een positieve gehele leesvolgorde |
| `BP4015` | Leesvolgorde komt voor in meerdere informatiegebieden |
| `BP4016` | Leesvolgorde van informatiegebieden is niet aaneengesloten |
| `BP4101` | Homepagegebied heeft een onbekende eigenschap |
| `BP4102` | Homepagegebied heeft geen geldige rol |
| `BP4103` | Homepagegebied mist een betekenisvolle kernboodschap |
| `BP4104` | Homepagegebied mist een positieve gehele leesvolgorde |
| `BP4105` | Leesvolgorde komt voor in meerdere homepagegebieden |
| `BP4106` | Entreegebied bevat ten onrechte een navigatiedoel |
| `BP4107` | Routegebied verwijst naar een onbekend navigatiedoel |
| `BP4108` | Navigatiedoel van homepagegebied is geen product of renderdoel |
| `BP4109` | Navigatiedoel komt voor in meerdere homepagegebieden |
| `BP4110` | Leesvolgorde van homepagegebieden is niet aaneengesloten |
| `BP4111` | Homepagegebied gebruikt geen componentrol die bij zijn inhoudsrol past |
| `BP4112` | Homepagegebied verwijst naar een onbekend component |
| `BP4113` | Homepagegebied verwijst naar een onbekende variant |
| `BP4114` | Homepagevariant hoort niet bij het gekozen component |
| `BP4115` | Entreegebied heeft een ongeldige focusvolgorde of navigatiegedrag |
| `BP4116` | Routegebied heeft een ongeldige focusvolgorde of navigatiegedrag |
| `BP4117` | Entreegebied mist een bekende native merkidentiteit |
| `BP4118` | Routegebied dupliceert ten onrechte de merkidentiteit |
| `BP4201` | Merk heeft een onbekende eigenschap |
| `BP4202` | Merk mist een betekenisvol tekstveld |
| `BP4203` | Merk heeft geen drie unieke betekenisvolle principes |
| `BP4204` | Merk heeft geen unieke betekenisvolle productfamilie |
| `BP4301` | SVG asset bevat een onbekende eigenschap |
| `BP4302` | Asset gebruikt niet expliciet formaat `svg` |
| `BP4303` | SVG asset gebruikt een onbekende semantische rol |
| `BP4304` | SVG asset heeft geen geldige positieve viewbox |
| `BP4305` | SVG asset heeft geen geldige unieke en begrensde padenlijst |
| `BP4306` | SVG asset bevat ongeldige of onveilige padgeometrie |
| `BP4307` | SVG asset bevat onveilige of volledig onzichtbare paint |
| `BP4308` | SVG asset heeft een inconsistent lijncontract |
| `BP4309` | SVG asset gebruikt onbekende toegankelijkheidssemantiek |
| `BP4310` | SVG asset heeft een ontbrekend of onterecht label |
| `BP4321` | Product gebruikt `assets` zonder inhoud `asset-catalog` |
| `BP4322` | SVG assetcatalogus mist een geldige unieke assetlijst |
| `BP4323` | SVG assetcatalogus verwijst naar een onbekend asset |
| `BP4324` | SVG assetcatalogus dekt niet alle native SVG assets expliciet |
| `BP4325` | Catalogusasset heeft niet exact één statisch SVG product |
| `BP4326` | SVG assetcatalogus gebruikt niet de HTML backend |
| `BP4327` | SVG assetcatalogus is niet statisch |
| `BP4328` | SVG assetcatalogus gebruikt geen `.html` artifactpad |
| `BP4329` | SVG assetcatalogus heeft niet exact één inhoudsinstantie |
| `BP4331` | SVG assetfamilie bevat een onbekende eigenschap |
| `BP4332` | SVG assetfamilie gebruikt een onbekend familietype |
| `BP4333` | SVG assetfamilie verwijst naar een onbekend merk |
| `BP4334` | SVG assetfamilie mist minstens twee unieke geordende assets |
| `BP4335` | SVG assetfamilie verwijst naar een onbekend asset |
| `BP4336` | SVG asset mist een bekende familie of betekenisvolle variant |
| `BP4337` | SVG assetfamilie en haar leden zijn niet exact wederkerig |
| `BP4338` | SVG assetfamilie bevat ontbrekende of dubbele varianten |
| `BP4339` | Assetrol past niet bij het familietype |
| `BP4340` | SVG merkfamilie bevat niet exact merkteken en woordmerk |
| `BP4351` | Wallpaper bevat een onbekende eigenschap |
| `BP4352` | Wallpaper verwijst naar een onbekende wereld |
| `BP4353` | Wallpaper verwijst naar een onbekend merk |
| `BP4354` | Wallpaper gebruikt een onbekend doelformaat |
| `BP4355` | Wallpaper heeft geen geldige canonieke canvasmaten |
| `BP4356` | Wallpapercanvas kan niet uit het wereldthema worden opgelost |
| `BP4357` | Wallpaper mist een geldige geordende lagenlijst |
| `BP4358` | Wallpaper verwijst naar een onbekende laag |
| `BP4359` | Wallpaper en lagen zijn niet exact wederkerig |
| `BP4360` | Wallpaperlaag bevat een onbekende eigenschap |
| `BP4361` | Wallpaperlaag verwijst naar een onbekende wallpaper |
| `BP4362` | Wallpaperlaag gebruikt een onbekende semantische rol |
| `BP4363` | Wallpaperlaag mist een geldige geordende plaatsingenlijst |
| `BP4364` | Wallpaperlaag verwijst naar een onbekende assetplaatsing |
| `BP4365` | Wallpaperlaag en plaatsingen zijn niet exact wederkerig |
| `BP4366` | Assetplaatsing bevat een onbekende eigenschap |
| `BP4367` | Assetplaatsing verwijst naar een onbekende wallpaperlaag |
| `BP4368` | Assetplaatsing verwijst naar een onbekend native asset |
| `BP4369` | Assetplaatsing heeft ongeldige coördinaten of afmetingen |
| `BP4370` | Assetplaatsing valt buiten het wallpapercanvas |
| `BP4371` | Assetplaatsing gebruikt een onbekende fitmodus |
| `BP4372` | Assetplaatsing heeft geen geldige dekking tussen 0 en 1 |
| `BP4373` | Assetrol past niet bij de semantische wallpaperlaagrol |
| `BP4374` | Assetplaatsing gebruikt geen oplosbare semantische materiaalrol |
| `BP4380` | Product gebruikt `wallpaper` zonder inhoud `wallpaper` |
| `BP4381` | Wallpaperproduct verwijst naar een onbekende wallpaper |
| `BP4382` | Wallpaperproduct gebruikt geen bekende wallpaperbackend |
| `BP4383` | Wallpaperproduct is niet statisch |
| `BP4384` | Wallpaperproduct en wallpaper gebruiken verschillende werelden |
| `BP4385` | Wallpaperproduct declareert een ander inhoudscontract |
| `BP4386` | Wallpaperproduct gebruikt geen bij zijn backend passend artifactpad |
| `BP4387` | Assetplaatsing gebruikt een onbekend native beeldeffect |
| `BP4388` | Radiale gloed gebruikt geen gevuld asset zonder lijn |
| `BP4390` | Wallpaperfamilie bevat een onbekende eigenschap |
| `BP4391` | Wallpaperfamilie verwijst naar een onbekend merk |
| `BP4392` | Wallpaperfamilie mist minstens twee unieke geordende wallpapers |
| `BP4393` | Wallpaperfamilie verwijst naar een onbekende wallpaper |
| `BP4394` | Wallpaperfamilie en haar leden zijn niet exact wederkerig |
| `BP4395` | Wallpaperfamilie bevat ontbrekende of dubbele varianten |
| `BP4396` | Wallpaperfamilie en haar leden gebruiken verschillende merken |
| `BP4397` | Wallpaperfamilie bevat een dubbel canvasformaat |
| `BP4398` | Wallpaper mist een bekende familie of betekenisvolle variant |
| `BP3722` | Componentinstantie verwijst naar een onbekend homepagegebied |
| `BP3723` | Componentinstantie dupliceert inhoud van een homepagegebied |
| `BP4410` | Databron bevat een onbekende eigenschap |
| `BP4411` | Databron mist een verplicht tekstveld |
| `BP4412` | Databron gebruikt een onbekende eenheid |
| `BP4413` | Databron staat `mapping` alleen toe bij eenheid `tekst` |
| `BP4414` | Databron mist een geldige `mapping`-lijst |
| `BP4415` | Databron met eenheid `tekst` mist `mapping` |
