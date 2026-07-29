# EmberForge ontwerpbron

M11.3a registreert het aangeleverde EmberForge Design System als gecontroleerde
ontwerpinput. Het pakket is geen tweede bron van waarheid. BAT blijft de enige
normatieve productbron.

De vaste bronidentiteit, inventaris, mappingstatus en uitsluitingen staan in
`project/design-inputs/emberforge-design-system.json`. De compiler valideert
dat externe input nooit normatief is, geen runtimeafhankelijkheden introduceert
en ieder ontwerpgebied een expliciete bestemming en bewijs heeft.

## Gapanalyse

| Gebied | Status | BAT bestemming |
|---|---|---|
| Palette | Gemigreerd in M11.3b | palette, materiaal en semantische kleurtokens |
| Typografie | Gemigreerd in M11.3e | typography en typescale |
| Spacing, radius, border, shadow en motion | Gemigreerd in M11.3c | gelijknamige theme primitives |
| Art direction | Gemigreerd in M11.3d | artdirection en opgelost thema |
| Componenten, states, toegankelijkheid en referentie | Gemigreerd in M11.3f tot en met M11.3i | appearance, component, variant, componentvoorbeeld, toegankelijkheid en native referentieproduct |
| Dashboard, Keycloak en terminal | Gemigreerd in M11.4a tot en met M11.4d | composition, layout en product |
| Vectorassets | Geblokkeerd | SVG component library |
| Merkverhaal, productfamilie en contentregels | Gemigreerd in M11.1e en M11.4e | Native merkidentiteit, homepage entree en productroutes |

De PNG logo's, placeholder SVG logo's, ontbrekende bestanden, Google Fonts,
CDN iconen en UI kit implementatiecode worden niet als productbron overgenomen.
Daarmee kan geen renderer ongemerkt afhankelijk worden van het aangeleverde
voorbeeldpakket.

## Eerste activering

M11.1e migreert de bewezen wereldtaal naar het native BAT merkobject
`emberforge`. Merknaam, tagline, kernbelofte, drie principes, productfamilie,
taal en stem worden door de compiler gevalideerd en uitsluitend via de
homepage entree geactiveerd. De HTML backend ontvangt opgeloste merksemantiek
en bevat zelf geen EmberForge teksten.

## Paletactivering

M11.3b migreert de geverifieerde ruwe kleuren en semantische kleurrollen naar
native BAT kleur, palet, materiaal en tokenobjecten. Sky is de primaire
interactiekleur. Ember Copper blijft het spaarzame warme accent. De HTML en
Grafana backends ontvangen uitsluitend het opgeloste thema en lezen de externe
bron niet.

## Primitiefactivering

M11.3c migreert de productgedragen semantische rollen voor spacing, radius,
border, shadow en motion. De native rollen blijven de stabiele interface voor
appearances en renderers. Hun waarden komen uit de geverifieerde EmberForge
bron: een 4px ruimtebasis, zachte afronding, 1px lijnen, donkere elevaties en
rustige motion met de standaard easing. Bronstappen waarvoor nog geen
productrol bestaat worden niet als ongebruikte BAT velden toegevoegd.

## Art direction

M11.3d modelleert de vastgestelde visuele balans als één native
`artdirection` object onder het Forge thema. Diepe navy bepaalt het canvas,
lichtend cyaan de interactie en gesmeed koper maximaal twee warme punten per
view. Gloed blijft gecontroleerd, ornamentiek gebruikt technische lijnvoering,
de compositiedichtheid blijft ruim en de beeldtaal gebruikt isometrische
lijnkunst.

De HTML backend leest uitsluitend het opgeloste contract. Daaruit ontstaan
twee subtiele radiale halo's, de technische scheidingslijn, reduced-motion
gedrag en machineleesbare art-directionmetadata. De backend
bevat geen EmberForge bronwaarden of zelfstandige merkbeslissingen.

## Typografie

M11.3e lost het expliciete typografieconflict normatief op. Orbitron draagt
koppen, Inter draagt interface en lopende tekst en JetBrains Mono draagt
technische tekst. Iedere rol bevat een geordende lokale voorkeursstack met een
generieke fallback. De levering is expliciet `local-only`.

De bestaande semantische productrollen krijgen de geverifieerde EmberForge
groottes 80, 56, 32, 16, 12 en 12 pixels. Niet gebruikte bronstappen worden
niet als losse BAT velden toegevoegd. De HTML backend vertaalt uitsluitend de
opgeloste stacks naar geldige CSS en voegt geen `@import`, URL of fontdownload
toe. Daardoor blijft de compiler onafhankelijk van Google Fonts en ontbrekende
fontbestanden.

## Componenttoestanden

M11.3f migreert de volledige interactiereeks voor Forge-kaarten naar native
BAT. De rusttoestand gebruikt het donkere oppervlak en de standaard outline.
Hover gebruikt de cyaan outline, de gecontroleerde cyaangloed en een lift van
één pixel. Focus gebruikt dezelfde herkenbare gloed zonder verplaatsing.
Pressed gebruikt donkerder cyaan, keert terug naar nul pixel en schaalt niet.
Disabled gebruikt de gedempte voorgrond, geen gloed en geen verplaatsing.

De variant koppelt iedere toestand expliciet aan een appearance. De opgeloste
compositie draagt dat contract naar HTML en Grafana. CSS vertaalt uitsluitend
de opgeloste appearances naar standaard pseudostates en expliciete
catalogusklassen. De eerdere generieke hover en focusregels in de HTML backend
zijn verwijderd, zodat UI kit code en merkwaarden niet in een renderer leven.

## Componentfamilie

M11.3g migreert de vijf productgedragen componentgroepen uit de geverifieerde
previewbestanden. Button, input, status, app tile en stat card zijn native
componenten met een expliciete semantische rol en anatomie. Zestien varianten
leggen de bronbewezen primary, secondary, ghost, Ember, validatie, status,
tegel en statistiekprofielen vast.

Voorbeeldinhoud staat niet in de catalogusrenderer. Zestien
`componentvoorbeeld` objecten leggen labels, waarden, beschrijvingen, meldingen
en operationele statussen vast. De HTML catalogus vertaalt uitsluitend deze
opgeloste data naar semantische elementen. De aangeleverde HTML, CSS en JSX
blijven bewijs en worden niet als implementatiecode gekopieerd.

Productgedragen tussenkleuren, zachte statusoppervlakken, de invoerradius en
focus en kopergloed zijn als expliciete theme rollen opgenomen. Daardoor
blijven ook de nieuwe componentvarianten afleidingen van hetzelfde Forge thema
en ontstaat geen losse CSS bron van waarheid.

## Toegankelijkheidscontracten

M11.3h voegt per native component een expliciet `toegankelijkheid` object toe.
Het contract legt de semantische rol, naambron, optionele waarde- en foutbron,
disabled gedrag, focusdeelname en toetsenbordgedrag vast. Acties en app tegels
gebruiken het activeringsprofiel met Enter en Spatie. Invoer gebruikt native
tekstinvoer. Panelen, statussen en statistieken blijven buiten de tabvolgorde.

Het native designsystem referentieproduct vertaalt deze opgeloste semantiek
naar native buttons, inputs, outputs en benoemde groepen. Labels en
foutmeldingen zijn expliciet gekoppeld. Product HTML publiceert hetzelfde
contract als metadata en Grafana neemt het op in de paneelbeschrijving. BAT
bevat geen HTML- of ARIA-velden.

Dit bewijst programmeerbare semantiek en native browsergedrag. Toetsing met
echte hulptechnologie valt niet binnen M11.3h en blijft daarom expliciet open.

## Designsystem referentieproduct

M11.3i vervangt het losse HTML catalogusrenderdoel door een regulier statisch
product. Vijf native `referentiesectie` objecten bepalen de volgorde en
betekenis van primitives, tokens, componenttoestanden, voorbeelden en
toegankelijkheid. De productcompiler draagt de volledige resolved referentie
naar de HTML backend. `components.html` leest geen ontwerpinput en bevat geen
externe runtimebron.

## Homelab dashboardproduct

M11.4a maakt van de geverifieerde statistiekkaarten, statussen en app tegels
een afzonderlijk EmberForge homelab product. Een componentinstantie verwijst
daarbij naar een volledig gevalideerd componentvoorbeeld. De compositie bevat
tien instanties en de native gridlayout ordent deze in vier kolommen, met twee
kolommen en expliciete leesvolgorde onder 960 pixels.

De HTML backend vertaalt uitsluitend de opgeloste voorbeeldinhoud. De
aangeleverde UI kit JSX en CSS blijven niet normatief en worden niet als
rendererlogica overgenomen.

M11.4b publiceert dezelfde compositie en layout via de Grafana backend. De tien
Canvas panelen ontvangen hun labels, waarden, varianten, states en
toegankelijkheidsmetadata uit dezelfde opgeloste componentvoorbeelden als het
HTML product. Het gegenereerde dashboard bevat geen datasource en claimt
daarom geen actuele operationele meetgegevens.

## Keycloak login productsurface

M11.4c modelleert de geverifieerde Keycloak loginweergave als native
loginformulier. De compositie, invoertypen en submitactie staan in BAT. HTML
vertaalt die contracten naar gekoppelde labels, email- en wachtwoordinvoer en
een submitbutton.

Het product bevat geen realm, clientconfiguratie, authenticatie-endpoint,
sessiegedrag of credentials. Het bewijst uitsluitend de statische
productsurface en niet een werkende Keycloak integratie.

## Terminal productsurface

M11.4d modelleert de geverifieerde terminalweergave als een eigen native
component, voorbeeld, compositie, layout en statisch HTML product. Het
voorbeeld draagt de venstertitel, geordende vensterknoppen, tabs, identiteit,
dertien systeemvelden en prompt. De compiler valideert deze inhoud als één
getypeerd terminalcontract.

De HTML backend vertaalt alleen de opgeloste voorbeeldinhoud en gebruikt
semantische groepering en een definitielijst. Vensterknoppen en tabs zijn
niet-interactieve bronweergaven. Er wordt geen shell uitgevoerd en de
systeemwaarden zijn voorbeelden, geen actuele telemetrie.

## Productnavigatie

M11.4e neemt de terminal op in de native EmberForge productfamilie en ontsluit
de Keycloak en terminal productsurfaces als afzonderlijke routekaarten op de
bestaande homepage. De routes verwijzen naar reguliere BAT producten. De
generieke HTML backend ontvangt alleen opgeloste relatieve artifactpaden en
bevat geen handmatig onderhouden routetabel.
