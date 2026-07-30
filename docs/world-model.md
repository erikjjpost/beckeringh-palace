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
| `assetfamilie` | geordende, merkgebonden samenhang tussen native assets |
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
