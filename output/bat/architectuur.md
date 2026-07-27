# Beckeringh Architectuurmodel

## Informatiebeheer

**Soort:** capability

**Identifier:** `informatiebeheer`

### Doel

Informatie beheersen over de volledige levenscyclus.

### Eigenschappen

- **levert:** Betrouwbare informatie, Vindbare informatie, Herleidbare informatie

## Tweede Brein

**Soort:** capability

**Identifier:** `tweede-brein`

### Doel

Ideeën, kennis en besluiten vastleggen, verbinden en terugvinden.

### Eigenschappen

- **hangt_af_van:** informatiebeheer

## Architectuur Synchronisatie

**Soort:** dienst

**Identifier:** `architectuur-synchronisatie`

### Doel

Ideeën omzetten in gecontroleerde voorstellen voor het architectuurmodel.

### Eigenschappen

- **ondersteunt:** tweede-brein
- **vereist:** menselijke-goedkeuring

## Ember Orange

**Soort:** kleur

**Identifier:** `ember-orange`

### Doel

Primaire warme accentkleur van de Forge-ontwerpidentiteit.

### Eigenschappen

- **waarde:** #D86A35

## Iron Black

**Soort:** kleur

**Identifier:** `iron-black`

### Doel

Donkere structurele basiskleur van de Forge-ontwerpidentiteit.

### Eigenschappen

- **waarde:** #171A1F

## Forged Iron

**Soort:** kleur

**Identifier:** `forged-iron`

### Doel

Dragend oppervlak voor de Forge-ontwerpidentiteit.

### Eigenschappen

- **waarde:** #20252C

## Raised Iron

**Soort:** kleur

**Identifier:** `raised-iron`

### Doel

Verhoogd kaartoppervlak voor de Forge-ontwerpidentiteit.

### Eigenschappen

- **waarde:** #282E36

## Smoke White

**Soort:** kleur

**Identifier:** `smoke-white`

### Doel

Lichte voorgrondkleur voor donkere Forge-oppervlakken.

### Eigenschappen

- **waarde:** #ECECEC

## Ash Grey

**Soort:** kleur

**Identifier:** `ash-grey`

### Doel

Gedempte voorgrondkleur voor ondersteunende Forge-informatie.

### Eigenschappen

- **waarde:** #AEB4BD

## Iron Edge

**Soort:** kleur

**Identifier:** `iron-edge`

### Doel

Subtiele outlinekleur voor Forge-oppervlakken en scheidingslijnen.

### Eigenschappen

- **waarde:** #46505C

## Ember Forge

**Soort:** palet

**Identifier:** `ember-forge`

### Doel

Semantisch kleurenpalet voor de Beckeringh Palace Forge-wereld.

### Eigenschappen

- **accent:** ember-orange
- **background:** iron-black
- **foreground:** smoke-white
- **primary:** ember-orange
- **surface:** iron-black

## Forge Interface

**Soort:** typografie

**Identifier:** `forge-interface`

### Doel

Typografische rollen voor digitale Forge-producten.

### Eigenschappen

- **body:** Aptos
- **heading:** Aptos Display
- **mono:** JetBrains Mono

## Forge Type Scale

**Soort:** typeschaal

**Identifier:** `forge-type-scale`

### Doel

Semantische tekstgroottes voor digitale Forge-producten.

### Eigenschappen

- **body:** 16px
- **caption:** 12px
- **display:** 64px
- **heading:** 28px
- **label:** 14px
- **title:** 40px

## Forge Materials

**Soort:** materiaal

**Identifier:** `forge-materials`

### Doel

Materiële kleurrollen voor Forge-oppervlakken en accenten.

### Eigenschappen

- **accent:** ember-orange
- **canvas:** iron-black
- **foreground:** smoke-white
- **muted:** ash-grey
- **outline:** iron-edge
- **raised:** raised-iron
- **surface:** forged-iron

## Forge Borders

**Soort:** border

**Identifier:** `forge-borders`

### Doel

Lijndiktes en lijnstijl voor Forge-producten.

### Eigenschappen

- **hairline:** 1px
- **regular:** 2px
- **strong:** 3px
- **style:** solid

## Forge Radius

**Soort:** radius

**Identifier:** `forge-radius`

### Doel

Afrondingsschaal voor Forge-componenten.

### Eigenschappen

- **large:** 24px
- **medium:** 12px
- **pill:** 999px
- **small:** 4px

## Forge Shadows

**Soort:** shadow

**Identifier:** `forge-shadows`

### Doel

Diepteschaal voor Forge-oppervlakken.

### Eigenschappen

- **high:** 0 20px 48px #00000073
- **low:** 0 2px 8px #00000040
- **medium:** 0 8px 24px #00000059

## Forge Motion

**Soort:** motion

**Identifier:** `forge-motion`

### Doel

Tijds- en easingprofiel voor rustige Forge-interacties.

### Eigenschappen

- **easing:** cubic-bezier(0.2, 0.8, 0.2, 1)
- **fast:** 120ms
- **normal:** 220ms
- **slow:** 420ms

## Forge Spacing

**Soort:** spacing

**Identifier:** `forge-spacing`

### Doel

Ruimtelijke schaal voor Forge-componenten en composities.

### Eigenschappen

- **large:** 24px
- **medium:** 16px
- **none:** 0
- **small:** 8px
- **xl:** 40px
- **xs:** 4px

## Forge

**Soort:** thema

**Identifier:** `forge`

### Doel

Nordic forge-ontwerpidentiteit voor Beckeringh Palace.

### Eigenschappen

- **border:** forge-borders
- **materiaal:** forge-materials
- **motion:** forge-motion
- **palet:** ember-forge
- **radius:** forge-radius
- **shadow:** forge-shadows
- **spacing:** forge-spacing
- **typeschaal:** forge-type-scale
- **typografie:** forge-interface

## Beckeringh Palace

**Soort:** wereld

**Identifier:** `beckeringh-palace`

### Doel

Eén reproduceerbare digitale ontwerpwereld leveren.

### Eigenschappen

- **thema:** forge

## Ember

**Soort:** token

**Identifier:** `color-ember`

### Doel

Primaire warme accentkleur voor de Forge-identiteit.

### Eigenschappen

- **type:** color
- **waarde:** #D86A35

## Iron

**Soort:** token

**Identifier:** `color-iron`

### Doel

Donkere structurele basiskleur.

### Eigenschappen

- **type:** color
- **waarde:** #171A1F

## Smoke

**Soort:** token

**Identifier:** `color-smoke`

### Doel

Lichte voorgrondkleur voor donkere oppervlakken.

### Eigenschappen

- **type:** color
- **waarde:** #ECECEC

## Accent

**Soort:** token

**Identifier:** `color-accent`

### Doel

Semantische accentkleur die naar de Forge-kleur verwijst.

### Eigenschappen

- **type:** color
- **waarde:** {color-ember}

## Medium radius

**Soort:** token

**Identifier:** `radius-medium`

### Doel

Standaard afronding voor productcomponenten.

### Eigenschappen

- **type:** dimension
- **waarde:** 12px

## Forge interface font family

**Soort:** token

**Identifier:** `typography-family-forge-interface`

### Doel

Hoofdlettertype voor digitale Forge-producten.

### Eigenschappen

- **type:** font-family
- **waarde:** Aptos

## Forge Panel Appearance

**Soort:** appearance

**Identifier:** `forge-panel-appearance`

### Doel

Semantisch appearance-contract voor verhoogde Forge-panelen.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** raised
- **motion:** normal
- **radius:** medium
- **shadow:** medium
- **spacing:** small

## Forge Panel Compact Appearance

**Soort:** appearance

**Identifier:** `forge-panel-compact-appearance`

### Doel

Compact paneelprofiel met minder ruimte en diepte.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** raised
- **motion:** normal
- **radius:** medium
- **shadow:** low
- **spacing:** xs

## Forge Panel

**Soort:** component

**Identifier:** `forge-panel`

### Doel

Basispaneel voor dashboards en productdocumentatie.

### Eigenschappen

- **appearance:** forge-panel-appearance

## Forge Panel Compact

**Soort:** variant

**Identifier:** `forge-panel-compact`

### Doel

Gecontroleerde compacte appearance voor een Forge-paneel.

### Eigenschappen

- **appearance:** forge-panel-compact-appearance
- **component:** forge-panel

## Wereld en identiteit

**Soort:** informatiegebied

**Identifier:** `palace-world`

### Doel

De digitale wereld, haar merk en haar reproduceerbare bronassets.

### Eigenschappen

- **inhoud:** beckeringh-palace
- **navigatie:** forge-dashboard-html, forge-dashboard-grafana
- **soorten:** wereld, merk, asset

## Forge ontwerpsysteem

**Soort:** informatiegebied

**Identifier:** `forge-design-system`

### Doel

De ontwerpprimitieven, tokens en componentcontracten van de Forge-identiteit.

### Eigenschappen

- **inhoud:** forge, forge-materials, forge-panel
- **navigatie:** html-components, css-components, css-tokens, json-tokens
- **soorten:** kleur, palet, typografie, typeschaal, materiaal, border, radius, shadow, motion, spacing, thema, appearance, token, component, variant

## Productfamilie

**Soort:** informatiegebied

**Identifier:** `palace-product-family`

### Doel

De composities, layouts en uitvoerproducten die uit dezelfde wereld worden gegenereerd.

### Eigenschappen

- **inhoud:** forge-dashboard, forge-dashboard-ultrawide, project-status-html
- **navigatie:** project-status-html, project-status-grafana
- **soorten:** compositie, componentinstantie, layout, region, product, renderdoel

## Forge Dashboard

**Soort:** compositie

**Identifier:** `forge-dashboard`

### Doel

Informatiearchitectuur van de Beckeringh Palace wereld, het Forge ontwerpsysteem en de productfamilie.

### Eigenschappen

- **instanties:** forge-dashboard-left-panel, forge-dashboard-center-panel, forge-dashboard-right-panel

## Wereld en identiteit

**Soort:** componentinstantie

**Identifier:** `forge-dashboard-left-panel`

### Doel

De digitale wereld, haar merk en haar reproduceerbare bronassets.

### Eigenschappen

- **component:** forge-panel
- **compositie:** forge-dashboard
- **informatiegebied:** palace-world

## Forge ontwerpsysteem

**Soort:** componentinstantie

**Identifier:** `forge-dashboard-center-panel`

### Doel

De ontwerpprimitieven, tokens en componentcontracten van de Forge-identiteit.

### Eigenschappen

- **component:** forge-panel
- **compositie:** forge-dashboard
- **informatiegebied:** forge-design-system
- **variant:** forge-panel-compact

## Productfamilie

**Soort:** componentinstantie

**Identifier:** `forge-dashboard-right-panel`

### Doel

De composities, layouts en uitvoerproducten die uit dezelfde wereld worden gegenereerd.

### Eigenschappen

- **component:** forge-panel
- **compositie:** forge-dashboard
- **informatiegebied:** palace-product-family

## Forge Dashboard Ultrawide

**Soort:** layout

**Identifier:** `forge-dashboard-ultrawide`

### Doel

Ordent de drie Forge-dashboardpanelen in een semantisch grid.

### Eigenschappen

- **columns:** 3
- **regions:** forge-dashboard-left, forge-dashboard-center, forge-dashboard-right
- **rows:** 1
- **type:** grid

## Linkerpaneel

**Soort:** region

**Identifier:** `forge-dashboard-left`

### Doel

Linker dashboardregio.

### Eigenschappen

- **column:** 1
- **column-span:** 1
- **instantie:** forge-dashboard-left-panel
- **layout:** forge-dashboard-ultrawide
- **row:** 1
- **row-span:** 1

## Middenpaneel

**Soort:** region

**Identifier:** `forge-dashboard-center`

### Doel

Centrale dashboardregio.

### Eigenschappen

- **column:** 2
- **column-span:** 1
- **instantie:** forge-dashboard-center-panel
- **layout:** forge-dashboard-ultrawide
- **row:** 1
- **row-span:** 1

## Rechterpaneel

**Soort:** region

**Identifier:** `forge-dashboard-right`

### Doel

Rechter dashboardregio.

### Eigenschappen

- **column:** 3
- **column-span:** 1
- **instantie:** forge-dashboard-right-panel
- **layout:** forge-dashboard-ultrawide
- **row:** 1
- **row-span:** 1

## Forge Dashboard HTML

**Soort:** product

**Identifier:** `forge-dashboard-html`

### Doel

Het ultrawide Forge-dashboard via de HTML-backend genereren.

### Eigenschappen

- **backend:** html
- **compositie:** forge-dashboard
- **layout:** forge-dashboard-ultrawide
- **mode:** static
- **pad:** output/products/forge-dashboard.html
- **wereld:** beckeringh-palace

## Forge Dashboard Grafana

**Soort:** product

**Identifier:** `forge-dashboard-grafana`

### Doel

Het Forge-dashboard als importeerbaar Grafana dashboard genereren.

### Eigenschappen

- **backend:** grafana
- **compositie:** forge-dashboard
- **layout:** forge-dashboard-ultrawide
- **mode:** static
- **pad:** output/products/forge-dashboard.grafana.json
- **wereld:** beckeringh-palace

## Beckeringh Palace Projectstatus

**Soort:** product

**Identifier:** `project-status-html`

### Doel

De normatieve projectvoortgang als reproduceerbaar HTML product ontsluiten.

### Eigenschappen

- **backend:** html
- **compositie:** forge-dashboard
- **inhoud:** project-status
- **layout:** forge-dashboard-ultrawide
- **mode:** static
- **pad:** output/products/project-status.html
- **wereld:** beckeringh-palace

## Beckeringh Palace Projectstatus Grafana

**Soort:** product

**Identifier:** `project-status-grafana`

### Doel

De normatieve projectvoortgang als reproduceerbaar Grafana dashboard ontsluiten.

### Eigenschappen

- **backend:** grafana
- **compositie:** forge-dashboard
- **inhoud:** project-status
- **layout:** forge-dashboard-ultrawide
- **mode:** static
- **pad:** output/products/project-status.grafana.json
- **wereld:** beckeringh-palace

## CSS design tokens

**Soort:** renderdoel

**Identifier:** `css-tokens`

### Doel

Design tokens als CSS custom properties genereren.

### Eigenschappen

- **formaat:** css
- **pad:** output/products/tokens.css

## Portable design tokens

**Soort:** renderdoel

**Identifier:** `json-tokens`

### Doel

Design tokens platformneutraal als JSON genereren.

### Eigenschappen

- **formaat:** json
- **pad:** output/products/tokens.json

## CSS components

**Soort:** renderdoel

**Identifier:** `css-components`

### Doel

Componenten als reproduceerbare CSS-klassen genereren.

### Eigenschappen

- **formaat:** css
- **pad:** output/products/components.css

## HTML component catalogue

**Soort:** renderdoel

**Identifier:** `html-components`

### Doel

Een minimale componentcatalogus genereren.

### Eigenschappen

- **formaat:** html
- **pad:** output/products/components.html