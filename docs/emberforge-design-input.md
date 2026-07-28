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
| Typografie | Besluit nodig | typography en typescale |
| Spacing, radius, border, shadow en motion | Gemigreerd in M11.3c | gelijknamige theme primitives |
| Art direction | Gemigreerd in M11.3d | artdirection en opgelost thema |
| Componenten en states | Gedeeltelijk mapbaar | appearance, component en variant |
| Dashboard, Keycloak en terminal | Gedeeltelijk mapbaar | composition, layout en product |
| Vectorassets | Geblokkeerd | SVG component library |
| Merkverhaal en contentregels | Gemigreerd in M11.1e | Native merkidentiteit en homepage entree |

De typografie wordt in deze milestone niet geactiveerd. Het bronpakket schrijft
Orbitron, Inter en JetBrains Mono voor en de actieve Forge configuratie gebruikt
een andere typografie. Dat conflict blijft expliciet totdat een normatieve
BAT-migratie het oplost.

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
twee subtiele radiale halo's, de technische scheidingslijn, cyaan focusgloed,
reduced-motion gedrag en machineleesbare art-directionmetadata. De backend
bevat geen EmberForge bronwaarden of zelfstandige merkbeslissingen.
