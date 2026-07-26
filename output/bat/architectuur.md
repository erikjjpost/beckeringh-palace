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

## Smoke White

**Soort:** kleur

**Identifier:** `smoke-white`

### Doel

Lichte voorgrondkleur voor donkere Forge-oppervlakken.

### Eigenschappen

- **waarde:** #ECECEC

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

## Forge Materials

**Soort:** materiaal

**Identifier:** `forge-materials`

### Doel

Materiële kleurrollen voor Forge-oppervlakken en accenten.

### Eigenschappen

- **accent:** ember-orange
- **canvas:** iron-black
- **foreground:** smoke-white
- **raised:** iron-black
- **surface:** iron-black

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

## Spacing unit

**Soort:** token

**Identifier:** `spacing-unit`

### Doel

Basiseenheid voor reproduceerbare tussenruimte.

### Eigenschappen

- **type:** dimension
- **waarde:** 8px

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

## Forge Panel

**Soort:** component

**Identifier:** `forge-panel`

### Doel

Basispaneel voor dashboards en productdocumentatie.

### Eigenschappen

- **accent:** {color-accent}
- **foreground:** {color-smoke}
- **padding:** {spacing-unit}
- **radius:** {radius-medium}
- **surface:** {color-iron}

## Forge Dashboard

**Soort:** compositie

**Identifier:** `forge-dashboard`

### Doel

Eerste reproduceerbare productsamenstelling.

### Eigenschappen

- **componenten:** forge-panel, forge-panel, forge-panel
- **richting:** row

## Forge Dashboard Ultrawide

**Soort:** layout

**Identifier:** `forge-dashboard-ultrawide`

### Doel

Backend-onafhankelijk canvas voor het Forge-dashboard.

### Eigenschappen

- **canvas-height:** 1080
- **canvas-width:** 3840
- **compositie:** forge-dashboard

## Linkerpaneel

**Soort:** regio

**Identifier:** `forge-dashboard-left`

### Doel

Linker dashboardregio.

### Eigenschappen

- **component:** forge-panel
- **height:** 840
- **layout:** forge-dashboard-ultrawide
- **width:** 1120
- **x:** 80
- **y:** 120

## Middenpaneel

**Soort:** regio

**Identifier:** `forge-dashboard-center`

### Doel

Centrale dashboardregio.

### Eigenschappen

- **component:** forge-panel
- **height:** 840
- **layout:** forge-dashboard-ultrawide
- **width:** 1120
- **x:** 1360
- **y:** 120

## Rechterpaneel

**Soort:** regio

**Identifier:** `forge-dashboard-right`

### Doel

Rechter dashboardregio.

### Eigenschappen

- **component:** forge-panel
- **height:** 840
- **layout:** forge-dashboard-ultrawide
- **width:** 1120
- **x:** 2640
- **y:** 120

## Forge Dashboard HTML

**Soort:** product

**Identifier:** `forge-dashboard-html`

### Doel

Het ultrawide Forge-dashboard via de HTML-backend genereren.

### Eigenschappen

- **backend:** html
- **layout:** forge-dashboard-ultrawide
- **pad:** output/products/forge-dashboard.html
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

## CSS compositions

**Soort:** renderdoel

**Identifier:** `css-compositions`

### Doel

Compositielayouts als CSS genereren.

### Eigenschappen

- **formaat:** css
- **pad:** output/products/compositions.css

## HTML compositions

**Soort:** renderdoel

**Identifier:** `html-compositions`

### Doel

Composities als zelfstandig HTML-product genereren.

### Eigenschappen

- **formaat:** html
- **pad:** output/products/compositions.html

## SVG compositions

**Soort:** renderdoel

**Identifier:** `svg-compositions`

### Doel

Composities als reproduceerbaar vectorcanvas genereren.

### Eigenschappen

- **formaat:** svg
- **pad:** output/products/compositions.svg

## Spatial HTML product

**Soort:** renderdoel

**Identifier:** `html-spatial`

### Doel

Het Spatial Model als exact gepositioneerd HTML-product genereren.

### Eigenschappen

- **formaat:** html
- **pad:** output/products/spatial.html