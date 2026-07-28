# Projectstatus Beckeringh Palace

> Dit bestand is gegenereerd uit `project/status.json`. Wijzig de bron en voer `python tools/bp.py check` uit.

## Totaalbeeld

**Geschatte voortgang: 50%**

Gewogen architectuurschatting van het volledige einddoel. De expliciete productgebiedgewichten tellen samen op tot 100%; het totaal wordt deterministisch afgerond op een geheel percentage.

- Actuele milestone: **M11.3g — EmberForge componentfamilie** (in uitvoering)
- Laatst voltooid: **M11.3f — EmberForge componenttoestanden** (PR #78)
- Volgende stap: **M11.3h — EmberForge toegankelijkheidscontracten**

## Voortgang per productgebied

| Productgebied | Gewicht | Voortgang | Onderbouwing | Resterend werk |
|---|---:|---:|---|---|
| Compiler en reproduceerbaarheid | 10% | 84% | Validatie, deterministische generatie, CI en 187 regressietests vormen een werkende kwaliteitsketen; componentrol, anatomie, voorbeelden en volledige statecontracten worden semantisch gevalideerd. | Meer producttypen, adapters en volwassen foutdiagnostiek. |
| World Model en productcontracten | 10% | 80% | Thema's, dashboardinformatiegebieden, homepagegebieden, merkidentiteit, layouts, zes componentrollen met expliciete anatomie, zestien productvoorbeelden, varianten, composities, producten, navigatie en snapshotidentiteit zijn native gemodelleerd. | Verdere productoppervlakken, toegankelijkheidssemantiek en bredere wereldsemantiek moeten nog in BAT worden opgenomen. |
| Design System | 10% | 94% | Het geverifieerde EmberForge palet, de theme primitives, art direction, lokale typografiestacks, volledige interactietoestanden en de button, input, status, app tile en stat card families zijn native gemigreerd. | Toegankelijkheidscontracten en volledige design system documentatie moeten nog normatief worden gemigreerd. |
| Dashboard UI en Grafana | 10% | 68% | HTML en Grafana delen drie native informatiegebieden en machineleesbare statecontracten; de HTML componentcatalogus rendert vijf productgedragen componentrollen en zestien voorbeelden uit hetzelfde BAT model. | Responsief gedrag en toetsen met echte hulptechnologie zijn nog niet als productcontract uitgewerkt. |
| Visuele wereld en art direction | 10% | 33% | EmberForge heeft een native merkidentiteit, expliciete visuele balans, een eigen typografische stem en bronbewezen cyaan, koper en statusprofielen voor de componentfamilie. | Palace, het Noorse thema, bevers, muziek en de bredere symboliek moeten nog samenhangend worden uitgewerkt. |
| SVG component library en icon set | 10% | 20% | De compiler kan componenten en SVG gerichte producten dragen. | Een brede, consistente en gedocumenteerde bibliotheek ontbreekt nog. |
| Logo's en wallpapers | 10% | 10% | De visuele richting en producteisen zijn bekend. | De reproduceerbare logo en wallpaperfamilies moeten nog als compilerproducten worden gerealiseerd. |
| HTML homepage | 10% | 69% | Vier geordende homepagegebieden dragen inhoud, appearance, focus en responsief gedrag; de drie routekaarten gebruiken native hover, focus, pressed en disabled appearances zonder generieke rendererregel. | Verdere productroutes, visuele motieven en productinhoud moeten nog worden verdiept. |
| Figma masterbestand | 10% | 10% | Figma is onderdeel van de doelarchitectuur. | Het masterbestand en de reproduceerbare synchronisatie zijn nog niet gerealiseerd. |
| World Bible | 10% | 31% | Architectuur en productregels zijn gedeeltelijk gedocumenteerd; merkbelofte, principes, taal, stem, componentrollen en voorbeeldcontracten zijn normatief vastgelegd. | De bredere wereldbeschrijving, symboliek en ontwerpregels moeten nog worden samengebracht. |

## Eerstvolgende stap

### M11.3h — EmberForge toegankelijkheidscontracten

Naam, rol, waarde, fout, disabled en toetsenbordgedrag voor de native componentfamilie backendonafhankelijk modelleren en toetsen.
