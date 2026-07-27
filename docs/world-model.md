# Beckeringh Palace World Model

## Besluit

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
| `asset` | reproduceerbare bronassets |
| `component` | herbruikbare productonderdelen |
| `componentinstantie` | benoemd gebruik van een component in één compositie |
| `compositie` | geordende productinhoud zonder layoutpresentatie |
| `layout` | backend-onafhankelijke plaatsingsintentie |
| `region` | expliciete plaats binnen een native layout |
| `product` | koppeling van wereld, productmodel, backend en artifactpad |
| `variant` | gecontroleerde afwijkingen |
| `renderdoel` | te genereren representaties |

Daaruit worden onder andere SVG, HTML, Grafana-thema's, documentatie, logo's, iconen, wallpapers en Figma-componenten afgeleid.

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
