# Productrunbook

`output/products/` bevat de reproduceerbare producten van Beckeringh Palace.
De bestanden zijn afgeleid. Wijzig ze niet rechtstreeks.

## Producten opnieuw genereren

Voer voor een volledige, gecontroleerde generatie uit:

```bash
python tools/bp.py check
```

Voor een gerichte ontwikkelcyclus kan de BAT-compiler afzonderlijk worden
uitgevoerd:

```bash
PYTHONDONTWRITEBYTECODE=1 python tools/compile_bat.py
```

Een wijziging is pas gereed wanneer de volledige controle eindigt met
`RESULTAAT: GELDIG EN REPRODUCEERBAAR`.

## HTML bekijken

Open `output/products/index.html` als ingang voor de bestaande
productnavigatie, het EmberForge designsystem referentieproduct en de native
Keycloak en terminal productsurfaces.

`output/products/components.html` is een statische designsystemsnapshot. De
lokale navigatie, primitives, tokens, states, voorbeelden en
toegankelijkheidscontracten worden volledig uit BAT gegenereerd.

`output/products/assets.html` is de statische native SVG assetcatalogus. Iedere
preview, contractwaarde en link komt uit de expliciete BAT assetlijst. De
artifactlink opent het bijbehorende gegenereerde SVG product in dezelfde
productmap.

`output/products/emberforge-vector-node.svg` is het eerste standalone native SVG
product. Het bevat uitsluitend gevalideerde padgeometrie, paint,
lijnattributen, assetmetadata en snapshotidentiteit.

`output/products/emberforge-icon-*.svg` vormt de eerste native EmberForge
iconenfamilie. Dashboard, Identity, Terminal en Assets gebruiken hetzelfde
24 bij 24 lijncontract en worden samen met het ornament vanuit BAT in de
assetcatalogus gepubliceerd.

`output/products/emberforge-merkteken.svg` en
`output/products/emberforge-woordmerk.svg` vormen de native EmberForge
merkfamilie. Beide artifacts zijn nieuwe BAT lijngeometrie. De aangeleverde
placeholder SVG's en PNG's blijven uitgesloten. De catalogus toont voor ieder
familielid ook het opgeloste familietype en de variant.

`output/products/emberforge-ultrawide.wallpaper.json` en
`output/products/emberforge-desktop.wallpaper.json` zijn de machineleesbare
contractproducten van één merkgebonden wallpaperfamilie. Zij publiceren
respectievelijk het zelfstandige 3840 bij 1080 en 1900 bij 1200 canvas, inclusief
familie, variant, lagen en plaatsingen. Geen van beide bevat een tweede bron
voor SVG geometrie of een schaalregel naar het andere formaat.

`output/products/emberforge-ultrawide.png` en
`output/products/emberforge-desktop.png` zijn de bijbehorende beeldartifacts.
De native backend rastert voor iedere variant de eigen opgeloste SVG
assetplaatsingen in BAT volgorde. Daaronder valt dezelfde uit BAT gegenereerde
Circle of Fifths met majeur, relatieve mineur en voortekens. Beide bestanden bevatten geen tijdstempel en
dragen product, wallpaper, familie, variant en volledige snapshotreferentie als
PNG metadata.

De manifesten publiceren per plaatsing ook `solid` of `radial-glow`. Controleer
bij visuele QA dat het koele hoofdlicht achter de informatielaag blijft, de
warme gloed geen hard vlak vormt en links geen onverwacht gevuld vlak ontstaat.

`output/products/emberforge-keycloak-login.html` is de reproduceerbare login
productsurface. Het artifact toont native email-, wachtwoord- en
submitsemantiek. Het bevat bewust geen realm, clientconfiguratie,
authenticatie-endpoint of werkende Keycloak koppeling.

`output/products/emberforge-terminal.html` is de reproduceerbare statische
terminal productsurface. Het artifact toont vensterchrome, tabs, identiteit,
dertien systeemvelden en een prompt uit het gevalideerde BAT voorbeeld. Het
voert geen shell uit en toont geen actuele telemetrie.

De Keycloak en terminal productsurfaces zijn vanaf M11.4e via eigen
routekaarten op de homepage ontsloten. De links worden uit de BAT
productdefinities afgeleid en blijven relatief binnen `output/products/`.

Een lokale webserver voorkomt browserbeperkingen bij relatieve bestanden:

```bash
python -m http.server 8000 --directory output/products
```

Open daarna `http://localhost:8000/`.

## Grafana importeren

Importeer in Grafana via **Dashboards**, **New**, **Import**:

- `output/products/forge-dashboard.grafana.json`;
- `output/products/emberforge-homelab-dashboard.grafana.json`;
- `output/products/project-status.grafana.json`.

Deze dashboards bevatten geen datasource en geen actuele operationele
meetgegevens. Het EmberForge homelab dashboard gebruikt dezelfde gevalideerde
voorbeeldinhoud als het HTML product. Een nieuwe import kan een bestaand
dashboard met dezelfde UID vervangen. Controleer daarom vóór import de
snapshotreferentie en bewaar zo nodig de bestaande JSON-export.

## Snapshot verifiëren

Statische producten delen één canonieke referentie in de vorm
`sha256:<64 hexadecimale tekens>`.

- HTML bewaart deze in het attribuut `data-snapshot-ref` op het productelement.
- Grafana bewaart dezelfde waarde als dashboardtag.
- PNG bewaart dezelfde waarde in het tekstveld `bp-snapshot`.

De eerste twaalf tekens worden als compacte identiteit getoond. Vergelijk voor
verificatie altijd de volledige referentie. Gelijke referenties betekenen dat
de gevalideerde architectuurinhoud waarop de snapshot is gebaseerd gelijk is.

## Rollback

Een rollback bestaat uit het opnieuw genereren vanuit een eerdere, bekende
Git-commit:

1. noteer de volledige snapshotreferentie van het gewenste product;
2. zoek de commit waarin `output/products/` die referentie bevat;
3. maak vanaf die commit een herstelbranch;
4. voer `python tools/bp.py check` uit;
5. importeer of publiceer uitsluitend de opnieuw gevalideerde producten.

Wijzig nooit een gegenereerd HTML- of Grafana-bestand om een oude toestand na
te bootsen. De Git-commit en het normatieve model blijven de rollbackbron.
