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
| Palette | Mapbaar | palette en semantische kleurrollen |
| Typografie | Besluit nodig | typography en typescale |
| Spacing, radius, shadow en motion | Mapbaar | gelijknamige theme primitives |
| Componenten en states | Gedeeltelijk mapbaar | appearance, component en variant |
| Dashboard, Keycloak en terminal | Gedeeltelijk mapbaar | composition, layout en product |
| Vectorassets | Geblokkeerd | SVG component library |
| Merkverhaal en contentregels | Mapbaar | World Bible |

De typografie wordt in deze milestone niet geactiveerd. Het bronpakket schrijft
Orbitron, Inter en JetBrains Mono voor en de actieve Forge configuratie gebruikt
een andere typografie. Dat conflict blijft expliciet totdat een normatieve
BAT-migratie het oplost.

De PNG logo's, placeholder SVG logo's, ontbrekende bestanden, Google Fonts,
CDN iconen en UI kit implementatiecode worden niet als productbron overgenomen.
Daarmee kan geen renderer ongemerkt afhankelijk worden van het aangeleverde
voorbeeldpakket.

## Vervolg

M11.1e kan de mapbare wereldtaal en productstructuur gebruiken nadat de waarden
expliciet in BAT zijn gemigreerd. Iedere migratie behoudt herkomst, tests en
reproduceerbaarheid en activeert alleen onderdelen waarvan de ontwerpbeslissing
is genomen.
