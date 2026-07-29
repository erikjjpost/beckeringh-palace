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
| Componenten, states en toegankelijkheid | Gemigreerd in M11.3f tot en met M11.3h | appearance, component, variant, componentvoorbeeld en toegankelijkheid |
| Dashboard, Keycloak en terminal | Gedeeltelijk mapbaar | composition, layout en product |
| Vectorassets | Geblokkeerd | SVG component library |
| Merkverhaal en contentregels | Gemigreerd in M11.1e | Native merkidentiteit en homepage entree |

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

De componentcatalogus vertaalt deze opgeloste semantiek naar native buttons,
inputs, outputs en benoemde groepen. Labels en foutmeldingen zijn expliciet
gekoppeld. Product HTML publiceert hetzelfde contract als metadata en Grafana
neemt het op in de paneelbeschrijving. BAT bevat geen HTML- of ARIA-velden.

Dit bewijst programmeerbare semantiek en native browsergedrag. Toetsing met
echte hulptechnologie valt niet binnen M11.3h en blijft daarom expliciet open.
