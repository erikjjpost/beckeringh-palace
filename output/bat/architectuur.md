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

## Deep Night Blue

**Soort:** kleur

**Identifier:** `ink-900`

### Doel

Standaardachtergrond van de EmberForge ontwerpidentiteit.

### Eigenschappen

- **waarde:** #0F1724

## Graphite

**Soort:** kleur

**Identifier:** `ink-800`

### Doel

Primair UI oppervlak van de EmberForge ontwerpidentiteit.

### Eigenschappen

- **waarde:** #1F2937

## Steel Blue

**Soort:** kleur

**Identifier:** `ink-700`

### Doel

Verhoogd kaart en paneeloppervlak.

### Eigenschappen

- **waarde:** #243447

## Divider Blue

**Soort:** kleur

**Identifier:** `ink-600`

### Doel

Hairline en scheidingskleur op donkere oppervlakken.

### Eigenschappen

- **waarde:** #2F4259

## Muted Steel

**Soort:** kleur

**Identifier:** `ink-500`

### Doel

Gedempte voorgrondkleur voor niet-beschikbare bediening.

### Eigenschappen

- **waarde:** #3E5573

## Cyan Accent

**Soort:** kleur

**Identifier:** `sky-400`

### Doel

Primaire interactie en highlightkleur.

### Eigenschappen

- **waarde:** #7DD3FC

## Pressed Cyan

**Soort:** kleur

**Identifier:** `sky-500`

### Doel

Donkerdere interactiekleur voor de ingedrukte toestand.

### Eigenschappen

- **waarde:** #38BDF8

## Ice White

**Soort:** kleur

**Identifier:** `bone-50`

### Doel

Primaire tekstkleur op donkere oppervlakken.

### Eigenschappen

- **waarde:** #E6EDF5

## Secondary Ice

**Soort:** kleur

**Identifier:** `bone-300`

### Doel

Secundaire tekstkleur op donkere oppervlakken.

### Eigenschappen

- **waarde:** #B8C5D6

## Ember Copper

**Soort:** kleur

**Identifier:** `ember-500`

### Doel

Spaarzame warme Forge accentkleur.

### Eigenschappen

- **waarde:** #C9895B

## Success Green

**Soort:** kleur

**Identifier:** `status-success`

### Doel

Semantische succeskleur.

### Eigenschappen

- **waarde:** #4ADE80

## Warning Amber

**Soort:** kleur

**Identifier:** `status-warning`

### Doel

Semantische waarschuwingskleur, onderscheiden van Ember.

### Eigenschappen

- **waarde:** #E0B341

## Danger Red

**Soort:** kleur

**Identifier:** `status-error`

### Doel

Semantische foutkleur.

### Eigenschappen

- **waarde:** #F87171

## Ember Forge

**Soort:** palet

**Identifier:** `ember-forge`

### Doel

Gecontroleerd gemigreerd semantisch kleurenpalet van EmberForge.

### Eigenschappen

- **accent:** ember-500
- **background:** ink-900
- **error:** status-error
- **foreground:** bone-50
- **primary:** sky-400
- **success:** status-success
- **surface:** ink-800
- **warning:** status-warning

## Forge Interface

**Soort:** typografie

**Identifier:** `forge-interface`

### Doel

Gecontroleerd gemigreerde EmberForge fontrollen met lokale fallbacks.

### Eigenschappen

- **body:** Inter, IBM Plex Sans, system-ui, -apple-system, sans-serif
- **heading:** Orbitron, Iceland, Bank Gothic, system-ui, sans-serif
- **levering:** local-only
- **mono:** JetBrains Mono, Fira Code, SF Mono, Menlo, monospace

## Forge Type Scale

**Soort:** typeschaal

**Identifier:** `forge-type-scale`

### Doel

Gecontroleerd gemigreerde semantische EmberForge tekstgroottes.

### Eigenschappen

- **body:** 16px
- **caption:** 12px
- **display:** 80px
- **heading:** 32px
- **label:** 12px
- **title:** 56px

## Forge Materials

**Soort:** materiaal

**Identifier:** `forge-materials`

### Doel

Gecontroleerd gemigreerde EmberForge materiaalrollen.

### Eigenschappen

- **accent:** ember-500
- **canvas:** ink-900
- **disabled:** ink-500
- **foreground:** bone-50
- **interaction:** sky-400
- **interaction-pressed:** sky-500
- **muted:** bone-300
- **outline:** ink-600
- **raised:** ink-700
- **surface:** ink-800

## Forge Borders

**Soort:** border

**Identifier:** `forge-borders`

### Doel

Gecontroleerd gemigreerde EmberForge lijnhiërarchie.

### Eigenschappen

- **hairline:** 1px
- **regular:** 1px
- **strong:** 1px
- **style:** solid

## Forge Radius

**Soort:** radius

**Identifier:** `forge-radius`

### Doel

Gecontroleerd gemigreerde EmberForge afrondingsschaal.

### Eigenschappen

- **large:** 16px
- **medium:** 12px
- **pill:** 999px
- **small:** 4px

## Forge Shadows

**Soort:** shadow

**Identifier:** `forge-shadows`

### Doel

Gecontroleerd gemigreerde EmberForge diepteschaal.

### Eigenschappen

- **glow:** 0 0 0 1px rgba(125,211,252,0.18), 0 6px 24px rgba(125,211,252,0.10)
- **high:** 0 18px 44px rgba(0,0,0,0.45)
- **low:** 0 1px 2px rgba(0,0,0,0.25)
- **medium:** 0 6px 18px rgba(0,0,0,0.35)
- **none:** none

## Forge Motion

**Soort:** motion

**Identifier:** `forge-motion`

### Doel

Gecontroleerd gemigreerd EmberForge tijds- en easingprofiel.

### Eigenschappen

- **easing:** cubic-bezier(0.2, 0.7, 0.2, 1)
- **fast:** 120ms
- **hover-offset:** -1px
- **normal:** 220ms
- **rest-offset:** 0px
- **slow:** 420ms

## Forge Spacing

**Soort:** spacing

**Identifier:** `forge-spacing`

### Doel

Gecontroleerd gemigreerde EmberForge ruimte op een 4px-basis.

### Eigenschappen

- **large:** 32px
- **medium:** 16px
- **none:** 0
- **small:** 8px
- **xl:** 64px
- **xs:** 4px

## EmberForge Art Direction

**Soort:** artdirection

**Identifier:** `emberforge-art-direction`

### Doel

Rustige soevereine control room met ruime duisternis en schaarse warmte.

### Eigenschappen

- **canvas:** canvas
- **density:** spacious
- **glow:** controlled
- **imagery:** isometric-line-art
- **interaction:** primary
- **ornament:** technical-linework
- **warm-accent:** accent
- **warm-accent-limit:** 2

## Forge

**Soort:** thema

**Identifier:** `forge`

### Doel

Nordic forge-ontwerpidentiteit voor Beckeringh Palace.

### Eigenschappen

- **artdirection:** emberforge-art-direction
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

## EmberForge

**Soort:** merk

**Identifier:** `emberforge`

### Doel

Merkidentiteit voor de soevereine infrastructuur binnen Beckeringh Palace.

### Eigenschappen

- **belofte:** Sovereignty over your own stack.
- **principes:** Own your data., Own your nodes., Own your forge.
- **producten:** Homelab Dashboard, Keycloak login, CV Database, ISMS Challenger, Roadmap, Marketing en merkoppervlakken
- **stem:** Zelfverzekerd, technisch en rustig
- **taal:** Nederlands met technische termen in het Engels
- **tagline:** Sovereign Infrastructure.

## Ember Copper

**Soort:** token

**Identifier:** `color-ember`

### Doel

Ruwe warme accentkleur uit het EmberForge bronpalet.

### Eigenschappen

- **type:** color
- **waarde:** #C9895B

## Deep Night Blue

**Soort:** token

**Identifier:** `color-iron`

### Doel

Ruwe achtergrondkleur uit het EmberForge bronpalet.

### Eigenschappen

- **type:** color
- **waarde:** #0F1724

## Ice White

**Soort:** token

**Identifier:** `color-smoke`

### Doel

Ruwe voorgrondkleur uit het EmberForge bronpalet.

### Eigenschappen

- **type:** color
- **waarde:** #E6EDF5

## Cyan Accent

**Soort:** token

**Identifier:** `color-sky`

### Doel

Ruwe primaire interactiekleur uit het EmberForge bronpalet.

### Eigenschappen

- **type:** color
- **waarde:** #7DD3FC

## Background

**Soort:** token

**Identifier:** `color-background`

### Doel

Semantische EmberForge achtergrondkleur.

### Eigenschappen

- **type:** color
- **waarde:** {color-iron}

## Primary

**Soort:** token

**Identifier:** `color-primary`

### Doel

Semantische EmberForge interactiekleur.

### Eigenschappen

- **type:** color
- **waarde:** {color-sky}

## Foreground

**Soort:** token

**Identifier:** `color-foreground`

### Doel

Semantische EmberForge voorgrondkleur.

### Eigenschappen

- **type:** color
- **waarde:** {color-smoke}

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
- **waarde:** Inter, IBM Plex Sans, system-ui, -apple-system, sans-serif

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
- **offset:** rest
- **outline:** outline
- **radius:** medium
- **shadow:** medium
- **spacing:** small

## Forge Panel Card Rest Appearance

**Soort:** appearance

**Identifier:** `forge-panel-card-rest-appearance`

### Doel

Rusttoestand van een interactief Forge-paneel.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** surface
- **motion:** normal
- **offset:** rest
- **outline:** outline
- **radius:** medium
- **shadow:** low
- **spacing:** medium

## Forge Panel Card Hover Appearance

**Soort:** appearance

**Identifier:** `forge-panel-card-hover-appearance`

### Doel

Cyaan omlijnde kaart met gecontroleerde gloed en één pixel lift.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** surface
- **motion:** normal
- **offset:** hover
- **outline:** interaction
- **radius:** medium
- **shadow:** glow
- **spacing:** medium

## Forge Panel Card Focus Appearance

**Soort:** appearance

**Identifier:** `forge-panel-card-focus-appearance`

### Doel

Toetsenbordfocus met cyaan omlijning en gecontroleerde gloed.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** surface
- **motion:** normal
- **offset:** rest
- **outline:** interaction
- **radius:** medium
- **shadow:** glow
- **spacing:** medium

## Forge Panel Card Pressed Appearance

**Soort:** appearance

**Identifier:** `forge-panel-card-pressed-appearance`

### Doel

Vlakkere ingedrukte toestand met donkerder cyaan en zonder verkleining.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** surface
- **motion:** normal
- **offset:** rest
- **outline:** interaction-pressed
- **radius:** medium
- **shadow:** low
- **spacing:** medium

## Forge Panel Card Disabled Appearance

**Soort:** appearance

**Identifier:** `forge-panel-card-disabled-appearance`

### Doel

Niet-beschikbare toestand met gedempte voorgrond zonder lift of gloed.

### Eigenschappen

- **accent:** disabled
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** disabled
- **heading-style:** heading
- **label-style:** label
- **material:** raised
- **motion:** normal
- **offset:** rest
- **outline:** outline
- **radius:** medium
- **shadow:** none
- **spacing:** medium

## Forge Panel Hero Appearance

**Soort:** appearance

**Identifier:** `forge-panel-hero-appearance`

### Doel

Ruime en verhoogde appearance voor de homepage-entree.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** strong
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** display
- **label-style:** label
- **material:** raised
- **motion:** slow
- **offset:** rest
- **outline:** outline
- **radius:** large
- **shadow:** high
- **spacing:** xl

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

- **appearance:** forge-panel-card-rest-appearance
- **component:** forge-panel
- **disabled:** forge-panel-card-disabled-appearance
- **focus:** forge-panel-card-focus-appearance
- **hover:** forge-panel-card-hover-appearance
- **pressed:** forge-panel-card-pressed-appearance

## Forge Panel Hero

**Soort:** variant

**Identifier:** `forge-panel-hero`

### Doel

Gecontroleerde hero-appearance voor de homepage-entree.

### Eigenschappen

- **appearance:** forge-panel-hero-appearance
- **component:** forge-panel

## Forge Panel Route

**Soort:** variant

**Identifier:** `forge-panel-route`

### Doel

Gecontroleerde routekaart-appearance voor homepage-navigatie.

### Eigenschappen

- **appearance:** forge-panel-card-rest-appearance
- **component:** forge-panel
- **disabled:** forge-panel-card-disabled-appearance
- **focus:** forge-panel-card-focus-appearance
- **hover:** forge-panel-card-hover-appearance
- **pressed:** forge-panel-card-pressed-appearance

## Wereld en identiteit

**Soort:** informatiegebied

**Identifier:** `palace-world`

### Doel

De digitale wereld, haar merk en haar reproduceerbare bronassets.

### Eigenschappen

- **inhoud:** beckeringh-palace
- **leesvolgorde:** 1
- **navigatie:** forge-dashboard-html, forge-dashboard-grafana
- **soorten:** wereld, merk, asset
- **toegankelijkheidslabel:** Wereld en identiteit, overzicht van wereld, merk en bronassets

## Forge ontwerpsysteem

**Soort:** informatiegebied

**Identifier:** `forge-design-system`

### Doel

De ontwerpprimitieven, tokens en componentcontracten van de Forge-identiteit.

### Eigenschappen

- **inhoud:** forge, forge-materials, forge-panel
- **leesvolgorde:** 2
- **navigatie:** html-components, css-components, css-tokens, json-tokens
- **soorten:** kleur, palet, typografie, typeschaal, materiaal, border, radius, shadow, motion, spacing, thema, appearance, token, component, variant
- **toegankelijkheidslabel:** Forge ontwerpsysteem, overzicht van ontwerpprimitieven en componenten

## Productfamilie

**Soort:** informatiegebied

**Identifier:** `palace-product-family`

### Doel

De composities, layouts en uitvoerproducten die uit dezelfde wereld worden gegenereerd.

### Eigenschappen

- **inhoud:** forge-dashboard, forge-dashboard-ultrawide, project-status-html
- **leesvolgorde:** 3
- **navigatie:** project-status-html, project-status-grafana
- **soorten:** homepagegebied, compositie, componentinstantie, layout, region, product, renderdoel
- **toegankelijkheidslabel:** Productfamilie, overzicht van composities, layouts en uitvoerproducten

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

## Beckeringh Palace

**Soort:** compositie

**Identifier:** `beckeringh-palace-homepage-composition`

### Doel

Toegangspoort tot de digitale wereld, het ontwerpsysteem en de actuele projectstatus.

### Eigenschappen

- **instanties:** homepage-intro, homepage-world, homepage-design-system, homepage-project-status

## Design is data

**Soort:** homepagegebied

**Identifier:** `homepage-entrance`

### Doel

Introduceert de ontwerpregel achter alle Beckeringh Palace producten.

### Eigenschappen

- **component:** forge-panel
- **componentrol:** hero
- **focusvolgorde:** 0
- **kernboodschap:** Design is data.
- **leesvolgorde:** 1
- **merk:** emberforge
- **navigatiegedrag:** geen
- **rol:** entree
- **variant:** forge-panel-hero

## Digitale wereld

**Soort:** homepagegebied

**Identifier:** `homepage-world-area`

### Doel

Verken de samenhang tussen wereld, identiteit en productfamilie.

### Eigenschappen

- **component:** forge-panel
- **componentrol:** routekaart
- **focusvolgorde:** 1
- **kernboodschap:** Eén normatief wereldmodel verbindt identiteit, ontwerp en producten.
- **leesvolgorde:** 2
- **navigatie:** forge-dashboard-html
- **navigatiegedrag:** volledige-kaart
- **rol:** route
- **variant:** forge-panel-route

## Forge ontwerpsysteem

**Soort:** homepagegebied

**Identifier:** `homepage-design-system-area`

### Doel

Bekijk de reproduceerbare componenten en ontwerpprimitieven.

### Eigenschappen

- **component:** forge-panel
- **componentrol:** routekaart
- **focusvolgorde:** 2
- **kernboodschap:** Tokens, appearances en componenten vormen één reproduceerbaar ontwerpsysteem.
- **leesvolgorde:** 3
- **navigatie:** html-components
- **navigatiegedrag:** volledige-kaart
- **rol:** route
- **variant:** forge-panel-route

## Projectstatus

**Soort:** homepagegebied

**Identifier:** `homepage-project-status-area`

### Doel

Volg de actuele voortgang, onderbouwing en eerstvolgende milestone.

### Eigenschappen

- **component:** forge-panel
- **componentrol:** routekaart
- **focusvolgorde:** 3
- **kernboodschap:** Voortgang en vervolgstappen komen uit dezelfde normatieve projectstatus.
- **leesvolgorde:** 4
- **navigatie:** project-status-html
- **navigatiegedrag:** volledige-kaart
- **rol:** route
- **variant:** forge-panel-route

## Design is data

**Soort:** componentinstantie

**Identifier:** `homepage-intro`

### Doel

Introduceert de ontwerpregel achter alle Beckeringh Palace producten.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-entrance

## Digitale wereld

**Soort:** componentinstantie

**Identifier:** `homepage-world`

### Doel

Verken de samenhang tussen wereld, identiteit en productfamilie.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-world-area

## Forge ontwerpsysteem

**Soort:** componentinstantie

**Identifier:** `homepage-design-system`

### Doel

Bekijk de reproduceerbare componenten en ontwerpprimitieven.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-design-system-area

## Projectstatus

**Soort:** componentinstantie

**Identifier:** `homepage-project-status`

### Doel

Volg de actuele voortgang, onderbouwing en eerstvolgende milestone.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-project-status-area

## Beckeringh Palace Homepage Grid

**Soort:** layout

**Identifier:** `beckeringh-palace-homepage-grid`

### Doel

Ordent de homepage entree en drie productroutes in een responsief grid.

### Eigenschappen

- **columns:** 3
- **compact-columns:** 1
- **regions:** homepage-intro-region, homepage-world-region, homepage-design-system-region, homepage-project-status-region
- **responsive-breakpoint:** 960
- **rows:** 2
- **type:** grid

## Homepage entree

**Soort:** region

**Identifier:** `homepage-intro-region`

### Doel

Brede entree tot Beckeringh Palace.

### Eigenschappen

- **column:** 1
- **column-span:** 3
- **compact-order:** 1
- **instantie:** homepage-intro
- **layout:** beckeringh-palace-homepage-grid
- **row:** 1
- **row-span:** 1

## Wereldroute

**Soort:** region

**Identifier:** `homepage-world-region`

### Doel

Route naar het wereld en productoverzicht.

### Eigenschappen

- **column:** 1
- **column-span:** 1
- **compact-order:** 2
- **instantie:** homepage-world
- **layout:** beckeringh-palace-homepage-grid
- **row:** 2
- **row-span:** 1

## Ontwerpsysteemroute

**Soort:** region

**Identifier:** `homepage-design-system-region`

### Doel

Route naar de componentcatalogus.

### Eigenschappen

- **column:** 2
- **column-span:** 1
- **compact-order:** 3
- **instantie:** homepage-design-system
- **layout:** beckeringh-palace-homepage-grid
- **row:** 2
- **row-span:** 1

## Statusroute

**Soort:** region

**Identifier:** `homepage-project-status-region`

### Doel

Route naar de actuele projectstatus.

### Eigenschappen

- **column:** 3
- **column-span:** 1
- **compact-order:** 4
- **instantie:** homepage-project-status
- **layout:** beckeringh-palace-homepage-grid
- **row:** 2
- **row-span:** 1

## Beckeringh Palace

**Soort:** product

**Identifier:** `beckeringh-palace-homepage`

### Doel

Homepage en toegangspoort voor de reproduceerbare Beckeringh Palace productwereld.

### Eigenschappen

- **backend:** html
- **compositie:** beckeringh-palace-homepage-composition
- **layout:** beckeringh-palace-homepage-grid
- **mode:** static
- **pad:** output/products/index.html
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