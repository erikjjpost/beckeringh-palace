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

## Beckeringh Palace

**Soort:** wereld

**Identifier:** `beckeringh-palace`

### Doel

Eén reproduceerbare digitale ontwerpwereld leveren.

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

## Default font family

**Soort:** token

**Identifier:** `typography-family-default`

### Doel

Standaardlettertype voor de digitale wereld.

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
