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

- **waarde:** #D86A35

## Iron

**Soort:** token

**Identifier:** `color-iron`

### Doel

Donkere structurele basiskleur.

### Eigenschappen

- **waarde:** #171A1F

## Spacing unit

**Soort:** token

**Identifier:** `spacing-unit`

### Doel

Basiseenheid voor reproduceerbare tussenruimte.

### Eigenschappen

- **waarde:** 8px

## CSS design tokens

**Soort:** renderdoel

**Identifier:** `css-tokens`

### Doel

Design tokens als CSS custom properties genereren.

### Eigenschappen

- **formaat:** css
- **pad:** output/products/tokens.css
