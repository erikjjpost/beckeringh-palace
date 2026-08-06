# Beckeringh Palace World Model

## Besluitrecord

- ID: `ADR-0001`
- Titel: BAT is een product- en ontwerpcompiler
- Status: geaccepteerd
- Datum: 2026-07-26
- Beslissingsdocument: dit document

BAT is een **product- en ontwerpcompiler** voor Beckeringh Palace. BAT is geen algemene enterprise-architectuurtaal en geen vervanging voor ArchiMate.

De compiler beschrijft uitsluitend concepten die nodig zijn om één consistente digitale wereld en haar producten reproduceerbaar te genereren.

## Native BAT-kern

De native objectsoorten zijn:

| Objectsoort | Verantwoordelijkheid |
|---|---|
| `wereld` | begrenst één digitale wereld |
| `merk` | identiteit en merkregels |
| `thema` | visuele en semantische varianten |
| `token` | herbruikbare ontwerpwaarden |
| `asset` | veilige, getypeerde en reproduceerbare bronassets |
| `muziekcirkel` | canonieke Circle of Fifths semantiek en reproduceerbare vectorgeometrie |
| `assetfamilie` | geordende, merkgebonden samenhang tussen native assets |
| `wallpaperfamilie` | geordende, merkgebonden samenhang tussen zelfstandige canvasformaten |
| `wallpaper` | canvas, doelformaat en geordende wallpaperlagen |
| `wallpaperlaag` | semantische laag met een expliciete plaatsingenlijst |
| `assetplaatsing` | begrensde plaats van één native asset op het canvas |
| `component` | herbruikbare productonderdelen |
| `toegankelijkheid` | backendonafhankelijke naam, rol, waarde, fout, disabled, focus en toetsenbordsemantiek |
| `componentvoorbeeld` | productgedragen voorbeeldinhoud voor één componentvariant |
| `referentiesectie` | geordend semantisch deel van een native referentieproduct |
| `componentinstantie` | benoemd gebruik van een component in één compositie |
| `compositie` | geordende productinhoud zonder layoutpresentatie |
| `layout` | backend-onafhankelijke plaatsingsintentie |
| `region` | expliciete plaats van een componentinstantie binnen een native layout |
| `product` | koppeling van wereld, compositie, layout, backend en artifactpad |
| `variant` | gecontroleerde componentappearances |
| `renderdoel` | te genereren representaties |

Daaruit worden onder andere SVG, HTML, Grafana-thema's, documentatie, logo's, iconen, wallpapers en Figma-componenten afgeleid.

M11.5a activeert het eerste concrete native assetcontract. Een SVG asset
declareert uitsluitend gecontroleerde padgeometrie, een positieve viewbox,
begrensde kleur- en lijnwaarden, een semantische rol en expliciete
toegankelijkheid. BAT accepteert geen ruwe SVG markup, scripts, externe
referenties of runtimebestanden. Een statisch `product` met backend `svg`
vertaalt het vooraf opgeloste asset naar een reproduceerbaar vectorartifact.

M11.5b ontsluit dezelfde opgeloste assets via een regulier statisch
catalogusproduct. Het product noemt de volledige geordende assetlijst
expliciet. Iedere catalogusvermelding verwijst naar exact één statisch SVG
product. Previews, contractmetadata en artifactlinks worden afgeleid en bevatten
geen tweede geometriebron.

M11.5c gebruikt datzelfde contract voor Dashboard, Identity, Terminal en
Assets. Deze vier informatieve iconen delen één expliciete 24 bij 24 viewbox,
lijnstijl en toegankelijkheidscontract. De iconenfamilie is BAT inhoud en
introduceert geen nieuw domeinconcept of rendererpad.

M11.5d maakt families zelf native. Een `assetfamilie` declareert een merk, het
type `iconen` of `merk` en minstens twee geordende assets. Lidmaatschap is
wederkerig en iedere assetvariant is uniek binnen haar familie. Een merkfamilie
bevat exact een merkteken en woordmerk. De HTML catalogus consumeert de
opgeloste familiesemantiek. De SVG backend blijft uitsluitend de veilige
assetgeometrie serialiseren.

M11.6a voegt het backendonafhankelijke wallpaperproductcontract toe. Een
`wallpaper` kiest expliciet wereld, merk, PNG doelformaat, pixelafmetingen,
semantische canvasrol en geordende lagen. Iedere `wallpaperlaag` noemt haar
plaatsingen wederkerig. Een `assetplaatsing` koppelt één bestaand native SVG
asset aan canonieke coördinaten, afmetingen, fitmodus, dekking en een
semantische materiaalrol binnen de canvasgrens.

De eerste 3840 bij 1080 EmberForge specificatie wordt als deterministisch
`.wallpaper.json` manifest en als echte `.png` gepubliceerd. M11.6b voegt
daarvoor een binaire productpayload en een native rasterbackend toe. De backend
consumeert uitsluitend de opgeloste productcontext. Geometrie, kleurkeuze,
laagvolgorde en plaatsing blijven daardoor in BAT en worden niet opnieuw in de
backend vastgelegd.

M11.6c ordent de 3840 bij 1080 ultrawide en 1900 bij 1200 desktopvariant als
één `wallpaperfamilie`. De familie bindt beide wallpapers aan hetzelfde merk en
vereist unieke varianten en canvasmaten. Iedere wallpaper houdt eigen lagen,
plaatsingen en producten. De compiler leidt geen verhouding, schaalfactor of
plaatsing van een andere variant af.

M11.6d voegt `muziekcirkel` toe als native informatieobject. BAT bewaart de
twaalf majeurtoonsoorten, relatieve mineurtoonsoorten en voortekens in
canonieke klokvolgorde. De resolver zet deze gevalideerde waarden om naar
veilige vectorlijnen en generieke enkel-lijn vectorglyphs. De wallpaperbackend
ontvangt alleen opgeloste geometrie en bevat geen muziektheorie. Beide
wallpaperformaten plaatsen dezelfde functionele cirkel met eigen coördinaten
volledig binnen hun canvas.

M11.6e maakt zachte lichtwerking expliciet met `radial-glow` op gevulde
plaatsingsmaskers. Het effect blijft achter de informatielaag, koelblauw is het
hoofdlicht en ieder formaat houdt exact twee begrensde warme accenten.

M11.6f voegt geen nieuwe objectsoort toe. Palace, bever en Noorse vlecht zijn
gewone veilige `asset` objecten met expliciete lijngeometrie. De wallpapers
componeren ze in zelfstandige lagen voor ornamenten en illustraties onder de
muziekcirkel. De eerdere technische vectornode blijft beschikbaar in de
assetcatalogus en is geen onderdeel meer van de wallpapercompositie.

M11.7a voegt `figmamaster` toe omdat een Figma master een concrete productsurface
is die expliciet moet selecteren welke bestaande ontwerpsemantiek wordt
gesynchroniseerd. Het object bezit geen Figma node-id's, pluginvelden of
rendererlogica. Het verwijst uitsluitend naar één wereld en expliciete native
assets, componenten, varianten, composities en layouts. De
`figma-manifest` backend publiceert die opgeloste selectie als statisch JSON
contract. Live synchronisatie naar Figma valt buiten deze milestone.

## Niet native

Concepten zoals `capability`, `dienst` en `agent` blijven tijdelijk beschikbaar als migratieconcepten. Zij mogen de kern van het World Model niet uitbreiden en worden niet als precedent gebruikt voor nieuwe enterprise-architectuursemantiek.

ArchiMate-modellen zijn externe bronnen. Integratie gebeurt later via een expliciete adapter:

```text
ArchiMate-model
      ↓ adapter
BAT-importmodel
      ↓ mapping
Beckeringh World Model
      ↓ renderers
SVG / HTML / Grafana / Figma / documentatie
```

BAT neemt dus geen ArchiMate-elementtypen, relatietypen of notatieleer over in de kern.

## Ontwerpregels

1. Een native objectsoort moet aantoonbaar nodig zijn voor minstens één productrenderer.
2. Een objectsoort die alleen enterprise-architectuur beschrijft, hoort in een adapter of extern model.
3. Renderers consumeren het semantische World Model en lezen geen handmatig onderhouden productbestanden.
4. Gegenereerde artefacten zijn nooit de bron van waarheid.
5. Nieuwe objectsoorten worden expliciet aan `compiler/world_model.py` toegevoegd; onbekende soorten krijgen geen impliciete semantiek.

## Migratiepad

M5 bouwt het World Model incrementeel op:

1. domeingrens en objectcatalogus;
2. minimale BAT-syntax voor native objectsoorten;
3. semantische regels per objectsoort;
4. eerste verticale product-slice;
5. adapters voor externe modellen, alleen waar aantoonbaar nodig.

De eerste verticale slice moet één klein product volledig uit BAT genereren. Daarmee wordt de bruikbaarheid van het World Model bewezen voordat extra concepten worden toegevoegd.
