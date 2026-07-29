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

## Deepest Night

**Soort:** kleur

**Identifier:** `ink-950`

### Doel

Donker invoeroppervlak binnen EmberForge bediening.

### Eigenschappen

- **waarde:** #0A111C

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

## Hover Cyan

**Soort:** kleur

**Identifier:** `sky-300`

### Doel

Lichtere cyaantoon voor hover en informatieve voorgrond.

### Eigenschappen

- **waarde:** #A5DEFB

## Soft Cyan Surface

**Soort:** kleur

**Identifier:** `sky-soft`

### Doel

Zacht cyaan oppervlak voor ghost bediening en informatieve status.

### Eigenschappen

- **waarde:** #7DD3FC0F

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

## Hover Copper

**Soort:** kleur

**Identifier:** `ember-300`

### Doel

Lichtere kopertoon voor het schaarse warme hoveraccent.

### Eigenschappen

- **waarde:** #E2A982

## Transparent

**Soort:** kleur

**Identifier:** `transparent-clear`

### Doel

Expliciet transparant oppervlak voor ghost en secondary bediening.

### Eigenschappen

- **waarde:** #00000000

## Success Green

**Soort:** kleur

**Identifier:** `status-success`

### Doel

Semantische succeskleur.

### Eigenschappen

- **waarde:** #4ADE80

## Success Surface

**Soort:** kleur

**Identifier:** `status-success-surface`

### Doel

Transparant groen statusoppervlak.

### Eigenschappen

- **waarde:** #4ADE801F

## Success Foreground

**Soort:** kleur

**Identifier:** `status-success-foreground`

### Doel

Leesbare groene statusvoorgrond.

### Eigenschappen

- **waarde:** #86EFAC

## Warning Amber

**Soort:** kleur

**Identifier:** `status-warning`

### Doel

Semantische waarschuwingskleur, onderscheiden van Ember.

### Eigenschappen

- **waarde:** #E0B341

## Warning Surface

**Soort:** kleur

**Identifier:** `status-warning-surface`

### Doel

Transparant amber statusoppervlak.

### Eigenschappen

- **waarde:** #E0B3411A

## Warning Foreground

**Soort:** kleur

**Identifier:** `status-warning-foreground`

### Doel

Leesbare amber statusvoorgrond.

### Eigenschappen

- **waarde:** #F3D783

## Danger Red

**Soort:** kleur

**Identifier:** `status-error`

### Doel

Semantische foutkleur.

### Eigenschappen

- **waarde:** #F87171

## Error Surface

**Soort:** kleur

**Identifier:** `status-error-surface`

### Doel

Transparant rood statusoppervlak.

### Eigenschappen

- **waarde:** #F871711A

## Error Foreground

**Soort:** kleur

**Identifier:** `status-error-foreground`

### Doel

Leesbare rode statusvoorgrond.

### Eigenschappen

- **waarde:** #FCA5A5

## Info Surface

**Soort:** kleur

**Identifier:** `status-info-surface`

### Doel

Transparant cyaan statusoppervlak.

### Eigenschappen

- **waarde:** #7DD3FC1A

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
- **accent-hover:** ember-300
- **canvas:** ink-900
- **disabled:** ink-500
- **error:** status-error
- **error-foreground:** status-error-foreground
- **error-surface:** status-error-surface
- **field:** ink-950
- **foreground:** bone-50
- **info:** sky-400
- **info-foreground:** sky-300
- **info-surface:** status-info-surface
- **interaction:** sky-400
- **interaction-hover:** sky-300
- **interaction-pressed:** sky-500
- **interaction-soft:** sky-soft
- **muted:** bone-300
- **outline:** ink-600
- **raised:** ink-700
- **success:** status-success
- **success-foreground:** status-success-foreground
- **success-surface:** status-success-surface
- **surface:** ink-800
- **transparent:** transparent-clear
- **warning:** status-warning
- **warning-foreground:** status-warning-foreground
- **warning-surface:** status-warning-surface

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

- **control:** 8px
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

- **focus:** 0 0 0 3px rgba(125,211,252,0.15)
- **glow:** 0 0 0 1px rgba(125,211,252,0.18), 0 6px 24px rgba(125,211,252,0.10)
- **glow-accent:** 0 0 0 1px rgba(201,137,91,0.30), 0 6px 22px rgba(201,137,91,0.18)
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

## Forge Panel Accessibility

**Soort:** toegankelijkheid

**Identifier:** `forge-panel-accessibility`

### Doel

Benoemt een informatief paneel als niet-interactieve groep.

### Eigenschappen

- **disabled:** niet-van-toepassing
- **focus:** geen
- **naambron:** titel
- **rol:** groep
- **toetsenbord:** geen

## Forge Panel

**Soort:** component

**Identifier:** `forge-panel`

### Doel

Basispaneel voor dashboards en productdocumentatie.

### Eigenschappen

- **anatomie:** titel, tekst
- **appearance:** forge-panel-appearance
- **rol:** paneel
- **toegankelijkheid:** forge-panel-accessibility

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

## Forge Primary Button Rest

**Soort:** appearance

**Identifier:** `forge-button-primary-rest-appearance`

### Doel

Primaire cyaan actie in rust.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** interaction
- **motion:** normal
- **offset:** rest
- **outline:** interaction
- **radius:** pill
- **shadow:** low
- **spacing:** small

## Forge Primary Button Hover

**Soort:** appearance

**Identifier:** `forge-button-primary-hover-appearance`

### Doel

Lichtere cyaan actie onder aanwijzer.

### Eigenschappen

- **accent:** interaction-hover
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** interaction-hover
- **motion:** normal
- **offset:** rest
- **outline:** interaction-hover
- **radius:** pill
- **shadow:** glow
- **spacing:** small

## Forge Primary Button Focus

**Soort:** appearance

**Identifier:** `forge-button-primary-focus-appearance`

### Doel

Primaire actie met expliciete cyaan focusring.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** interaction
- **motion:** normal
- **offset:** rest
- **outline:** interaction
- **radius:** pill
- **shadow:** focus
- **spacing:** small

## Forge Primary Button Pressed

**Soort:** appearance

**Identifier:** `forge-button-primary-pressed-appearance`

### Doel

Vlakkere primaire actie met donkerder cyaan.

### Eigenschappen

- **accent:** interaction-pressed
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** interaction-pressed
- **motion:** normal
- **offset:** rest
- **outline:** interaction-pressed
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Button Disabled

**Soort:** appearance

**Identifier:** `forge-button-disabled-appearance`

### Doel

Gedempte niet-beschikbare actie.

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
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Secondary Button Rest

**Soort:** appearance

**Identifier:** `forge-button-secondary-rest-appearance`

### Doel

Transparante secundaire actie met hairline.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** transparent
- **motion:** normal
- **offset:** rest
- **outline:** outline
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Secondary Button Hover

**Soort:** appearance

**Identifier:** `forge-button-secondary-hover-appearance`

### Doel

Secundaire actie met cyaan voorgrond en rand.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** interaction
- **heading-style:** heading
- **label-style:** label
- **material:** transparent
- **motion:** normal
- **offset:** rest
- **outline:** interaction
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Secondary Button Focus

**Soort:** appearance

**Identifier:** `forge-button-secondary-focus-appearance`

### Doel

Secundaire actie met cyaan focusring.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** interaction
- **heading-style:** heading
- **label-style:** label
- **material:** transparent
- **motion:** normal
- **offset:** rest
- **outline:** interaction
- **radius:** pill
- **shadow:** focus
- **spacing:** small

## Forge Secondary Button Pressed

**Soort:** appearance

**Identifier:** `forge-button-secondary-pressed-appearance`

### Doel

Vlakkere secundaire actie met donkerder cyaan.

### Eigenschappen

- **accent:** interaction-pressed
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** interaction-pressed
- **heading-style:** heading
- **label-style:** label
- **material:** transparent
- **motion:** normal
- **offset:** rest
- **outline:** interaction-pressed
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Ghost Button Rest

**Soort:** appearance

**Identifier:** `forge-button-ghost-rest-appearance`

### Doel

Gedempte ghost actie zonder zichtbare rand.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** muted
- **heading-style:** heading
- **label-style:** label
- **material:** transparent
- **motion:** normal
- **offset:** rest
- **outline:** transparent
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Ghost Button Hover

**Soort:** appearance

**Identifier:** `forge-button-ghost-hover-appearance`

### Doel

Ghost actie op een zacht cyaan oppervlak.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** interaction-soft
- **motion:** normal
- **offset:** rest
- **outline:** transparent
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Ember Button Rest

**Soort:** appearance

**Identifier:** `forge-button-ember-rest-appearance`

### Doel

Schaarse warme actie met kopergloed.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** accent
- **motion:** normal
- **offset:** rest
- **outline:** accent
- **radius:** pill
- **shadow:** glow-accent
- **spacing:** small

## Forge Ember Button Hover

**Soort:** appearance

**Identifier:** `forge-button-ember-hover-appearance`

### Doel

Lichtere koperactie onder aanwijzer.

### Eigenschappen

- **accent:** accent-hover
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** accent-hover
- **motion:** normal
- **offset:** rest
- **outline:** accent-hover
- **radius:** pill
- **shadow:** glow-accent
- **spacing:** small

## Forge Ember Button Focus

**Soort:** appearance

**Identifier:** `forge-button-ember-focus-appearance`

### Doel

Warme actie met gecontroleerde kopergloed.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** accent
- **motion:** normal
- **offset:** rest
- **outline:** accent
- **radius:** pill
- **shadow:** glow-accent
- **spacing:** small

## Forge Ember Button Pressed

**Soort:** appearance

**Identifier:** `forge-button-ember-pressed-appearance`

### Doel

Vlakkere warme actie zonder schaalverandering.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** canvas
- **heading-style:** heading
- **label-style:** label
- **material:** accent
- **motion:** normal
- **offset:** rest
- **outline:** accent
- **radius:** pill
- **shadow:** none
- **spacing:** small

## Forge Input Rest

**Soort:** appearance

**Identifier:** `forge-input-rest-appearance`

### Doel

Donker invoerveld in rust.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** field
- **motion:** normal
- **offset:** rest
- **outline:** outline
- **radius:** control
- **shadow:** none
- **spacing:** small

## Forge Input Focus

**Soort:** appearance

**Identifier:** `forge-input-focus-appearance`

### Doel

Invoerveld met cyaan rand en focusring.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** field
- **motion:** normal
- **offset:** rest
- **outline:** interaction
- **radius:** control
- **shadow:** focus
- **spacing:** small

## Forge Input Disabled

**Soort:** appearance

**Identifier:** `forge-input-disabled-appearance`

### Doel

Niet-beschikbaar invoerveld met gedempte inhoud.

### Eigenschappen

- **accent:** disabled
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** disabled
- **heading-style:** heading
- **label-style:** label
- **material:** field
- **motion:** normal
- **offset:** rest
- **outline:** outline
- **radius:** control
- **shadow:** none
- **spacing:** small

## Forge Input Error

**Soort:** appearance

**Identifier:** `forge-input-error-appearance`

### Doel

Invoerveld met expliciete foutkleur.

### Eigenschappen

- **accent:** error
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** field
- **motion:** normal
- **offset:** rest
- **outline:** error
- **radius:** control
- **shadow:** none
- **spacing:** small

## Forge Running Status

**Soort:** appearance

**Identifier:** `forge-status-running-appearance`

### Doel

Groene statuscapsule voor werkende diensten.

### Eigenschappen

- **accent:** success
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** success-foreground
- **heading-style:** heading
- **label-style:** label
- **material:** success-surface
- **motion:** fast
- **offset:** rest
- **outline:** success
- **radius:** pill
- **shadow:** none
- **spacing:** xs

## Forge Pending Status

**Soort:** appearance

**Identifier:** `forge-status-pending-appearance`

### Doel

Amber statuscapsule voor wachtende diensten.

### Eigenschappen

- **accent:** warning
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** warning-foreground
- **heading-style:** heading
- **label-style:** label
- **material:** warning-surface
- **motion:** fast
- **offset:** rest
- **outline:** warning
- **radius:** pill
- **shadow:** none
- **spacing:** xs

## Forge Failed Status

**Soort:** appearance

**Identifier:** `forge-status-failed-appearance`

### Doel

Rode statuscapsule voor gefaalde diensten.

### Eigenschappen

- **accent:** error
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** error-foreground
- **heading-style:** heading
- **label-style:** label
- **material:** error-surface
- **motion:** fast
- **offset:** rest
- **outline:** error
- **radius:** pill
- **shadow:** none
- **spacing:** xs

## Forge Info Status

**Soort:** appearance

**Identifier:** `forge-status-info-appearance`

### Doel

Cyaan statuscapsule voor informatieve gezondheid.

### Eigenschappen

- **accent:** info
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** info-foreground
- **heading-style:** heading
- **label-style:** label
- **material:** info-surface
- **motion:** fast
- **offset:** rest
- **outline:** info
- **radius:** pill
- **shadow:** none
- **spacing:** xs

## Forge App Tile Rest

**Soort:** appearance

**Identifier:** `forge-app-tile-rest-appearance`

### Doel

Operationele app tegel met cyaan componentaccent.

### Eigenschappen

- **accent:** interaction
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

## Forge App Tile Hover

**Soort:** appearance

**Identifier:** `forge-app-tile-hover-appearance`

### Doel

App tegel met cyaan gloed en één pixel lift.

### Eigenschappen

- **accent:** interaction
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

## Forge App Tile Focus

**Soort:** appearance

**Identifier:** `forge-app-tile-focus-appearance`

### Doel

App tegel met cyaan focusgloed.

### Eigenschappen

- **accent:** interaction
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

## Forge App Tile Pressed

**Soort:** appearance

**Identifier:** `forge-app-tile-pressed-appearance`

### Doel

Vlakkere app tegel met donkerder cyaan.

### Eigenschappen

- **accent:** interaction-pressed
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

## Forge App Tile Disabled

**Soort:** appearance

**Identifier:** `forge-app-tile-disabled-appearance`

### Doel

Niet-beschikbare app tegel zonder lift of gloed.

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

## Forge Ember App Tile Rest

**Soort:** appearance

**Identifier:** `forge-app-tile-ember-rest-appearance`

### Doel

Zeldzame app tegel met koperaccent.

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

## Forge Ember App Tile Hover

**Soort:** appearance

**Identifier:** `forge-app-tile-ember-hover-appearance`

### Doel

Koper app tegel met gecontroleerde gloed en lift.

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
- **outline:** accent
- **radius:** medium
- **shadow:** glow-accent
- **spacing:** medium

## Forge Ember App Tile Focus

**Soort:** appearance

**Identifier:** `forge-app-tile-ember-focus-appearance`

### Doel

Koper app tegel met gecontroleerde focusgloed.

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
- **outline:** accent
- **radius:** medium
- **shadow:** glow-accent
- **spacing:** medium

## Forge Ember App Tile Pressed

**Soort:** appearance

**Identifier:** `forge-app-tile-ember-pressed-appearance`

### Doel

Vlakkere koper app tegel zonder schaalverandering.

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
- **outline:** accent
- **radius:** medium
- **shadow:** low
- **spacing:** medium

## Forge Stat Card Value

**Soort:** appearance

**Identifier:** `forge-stat-card-value-appearance`

### Doel

Operationele statistiekkaart met cyaan waardeaccent.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** surface
- **motion:** fast
- **offset:** rest
- **outline:** outline
- **radius:** medium
- **shadow:** none
- **spacing:** medium

## Forge Stat Card Health

**Soort:** appearance

**Identifier:** `forge-stat-card-health-appearance`

### Doel

Statistiekkaart met groen gezondheidsaccent.

### Eigenschappen

- **accent:** success
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** surface
- **motion:** fast
- **offset:** rest
- **outline:** outline
- **radius:** medium
- **shadow:** none
- **spacing:** medium

## Forge Stat Card Ember

**Soort:** appearance

**Identifier:** `forge-stat-card-ember-appearance`

### Doel

Statistiekkaart met één schaars koperaccent.

### Eigenschappen

- **accent:** accent
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** surface
- **motion:** fast
- **offset:** rest
- **outline:** outline
- **radius:** medium
- **shadow:** none
- **spacing:** medium

## Forge Button Accessibility

**Soort:** toegankelijkheid

**Identifier:** `forge-button-accessibility`

### Doel

Benoemt een actie en legt native activering en disabled gedrag vast.

### Eigenschappen

- **disabled:** native
- **focus:** tabvolgorde
- **naambron:** label
- **rol:** actie
- **toetsenbord:** activeren

## Forge Input Accessibility

**Soort:** toegankelijkheid

**Identifier:** `forge-input-accessibility`

### Doel

Koppelt tekstinvoer expliciet aan naam, waarde en foutmelding.

### Eigenschappen

- **disabled:** native
- **focus:** tabvolgorde
- **foutbron:** melding
- **naambron:** label
- **rol:** tekstinvoer
- **toetsenbord:** tekstinvoer
- **waardebron:** waarde

## Forge Status Accessibility

**Soort:** toegankelijkheid

**Identifier:** `forge-status-accessibility`

### Doel

Benoemt een operationele status en haar feitelijke waarde.

### Eigenschappen

- **disabled:** niet-van-toepassing
- **focus:** geen
- **naambron:** label
- **rol:** status
- **toetsenbord:** geen
- **waardebron:** waarde

## Forge App Tile Accessibility

**Soort:** toegankelijkheid

**Identifier:** `forge-app-tile-accessibility`

### Doel

Benoemt een app tegel als native activeerbare productactie.

### Eigenschappen

- **disabled:** native
- **focus:** tabvolgorde
- **naambron:** label
- **rol:** actie
- **toetsenbord:** activeren
- **waardebron:** status

## Forge Stat Card Accessibility

**Soort:** toegankelijkheid

**Identifier:** `forge-stat-card-accessibility`

### Doel

Benoemt een statistiek als niet-interactieve waardegroep.

### Eigenschappen

- **disabled:** niet-van-toepassing
- **focus:** geen
- **naambron:** label
- **rol:** groep
- **toetsenbord:** geen
- **waardebron:** waarde

## Forge Button

**Soort:** component

**Identifier:** `forge-button`

### Doel

Actiecomponent voor primaire, secundaire, ghost en warme acties.

### Eigenschappen

- **anatomie:** label
- **appearance:** forge-button-primary-rest-appearance
- **rol:** actie
- **toegankelijkheid:** forge-button-accessibility

## Forge Input

**Soort:** component

**Identifier:** `forge-input`

### Doel

Invoercomponent met waarde en optionele foutmelding.

### Eigenschappen

- **anatomie:** label, waarde, melding
- **appearance:** forge-input-rest-appearance
- **rol:** invoer
- **toegankelijkheid:** forge-input-accessibility

## Forge Status

**Soort:** component

**Identifier:** `forge-status`

### Doel

Feitelijke statuscapsule voor operationele toestand.

### Eigenschappen

- **anatomie:** label, waarde
- **appearance:** forge-status-info-appearance
- **rol:** status
- **toegankelijkheid:** forge-status-accessibility

## Forge App Tile

**Soort:** component

**Identifier:** `forge-app-tile`

### Doel

Producttegel voor één toepassing en haar operationele status.

### Eigenschappen

- **anatomie:** label, beschrijving, status
- **appearance:** forge-app-tile-rest-appearance
- **rol:** app-tegel
- **toegankelijkheid:** forge-app-tile-accessibility

## Forge Stat Card

**Soort:** component

**Identifier:** `forge-stat-card`

### Doel

Compacte operationele waarde met context.

### Eigenschappen

- **anatomie:** label, waarde, beschrijving
- **appearance:** forge-stat-card-value-appearance
- **rol:** statistiek
- **toegankelijkheid:** forge-stat-card-accessibility

## Primary

**Soort:** variant

**Identifier:** `forge-button-primary`

### Doel

Primaire actie volgens de EmberForge button preview.

### Eigenschappen

- **appearance:** forge-button-primary-rest-appearance
- **component:** forge-button
- **disabled:** forge-button-disabled-appearance
- **focus:** forge-button-primary-focus-appearance
- **hover:** forge-button-primary-hover-appearance
- **pressed:** forge-button-primary-pressed-appearance

## Secondary

**Soort:** variant

**Identifier:** `forge-button-secondary`

### Doel

Secundaire transparante actie met cyaan interactiestates.

### Eigenschappen

- **appearance:** forge-button-secondary-rest-appearance
- **component:** forge-button
- **disabled:** forge-button-disabled-appearance
- **focus:** forge-button-secondary-focus-appearance
- **hover:** forge-button-secondary-hover-appearance
- **pressed:** forge-button-secondary-pressed-appearance

## Ghost

**Soort:** variant

**Identifier:** `forge-button-ghost`

### Doel

Gedempte actie zonder permanente rand.

### Eigenschappen

- **appearance:** forge-button-ghost-rest-appearance
- **component:** forge-button
- **disabled:** forge-button-disabled-appearance
- **focus:** forge-button-secondary-focus-appearance
- **hover:** forge-button-ghost-hover-appearance
- **pressed:** forge-button-secondary-pressed-appearance

## Ember

**Soort:** variant

**Identifier:** `forge-button-ember`

### Doel

Schaarse warme actie volgens de Ember-regel.

### Eigenschappen

- **appearance:** forge-button-ember-rest-appearance
- **component:** forge-button
- **disabled:** forge-button-disabled-appearance
- **focus:** forge-button-ember-focus-appearance
- **hover:** forge-button-ember-hover-appearance
- **pressed:** forge-button-ember-pressed-appearance

## Default Input

**Soort:** variant

**Identifier:** `forge-input-default`

### Doel

Regulier invoerveld met focus en disabled toestand.

### Eigenschappen

- **appearance:** forge-input-rest-appearance
- **component:** forge-input
- **disabled:** forge-input-disabled-appearance
- **focus:** forge-input-focus-appearance
- **hover:** forge-input-rest-appearance
- **pressed:** forge-input-focus-appearance

## Error Input

**Soort:** variant

**Identifier:** `forge-input-error`

### Doel

Ongeldig invoerveld met feitelijke herstelmelding.

### Eigenschappen

- **appearance:** forge-input-error-appearance
- **component:** forge-input

## Running

**Soort:** variant

**Identifier:** `forge-status-running`

### Doel

Werkende operationele toestand.

### Eigenschappen

- **appearance:** forge-status-running-appearance
- **component:** forge-status

## Pending

**Soort:** variant

**Identifier:** `forge-status-pending`

### Doel

Wachtende operationele toestand.

### Eigenschappen

- **appearance:** forge-status-pending-appearance
- **component:** forge-status

## Failed

**Soort:** variant

**Identifier:** `forge-status-failed`

### Doel

Gefaalde operationele toestand.

### Eigenschappen

- **appearance:** forge-status-failed-appearance
- **component:** forge-status

## Healthy

**Soort:** variant

**Identifier:** `forge-status-info`

### Doel

Informatieve operationele gezondheid.

### Eigenschappen

- **appearance:** forge-status-info-appearance
- **component:** forge-status

## Default App Tile

**Soort:** variant

**Identifier:** `forge-app-tile-default`

### Doel

Reguliere producttegel met cyaan interactie.

### Eigenschappen

- **appearance:** forge-app-tile-rest-appearance
- **component:** forge-app-tile
- **disabled:** forge-app-tile-disabled-appearance
- **focus:** forge-app-tile-focus-appearance
- **hover:** forge-app-tile-hover-appearance
- **pressed:** forge-app-tile-pressed-appearance

## Ember App Tile

**Soort:** variant

**Identifier:** `forge-app-tile-ember`

### Doel

Zeldzame warme producttegel voor CV Tool.

### Eigenschappen

- **appearance:** forge-app-tile-ember-rest-appearance
- **component:** forge-app-tile
- **disabled:** forge-app-tile-disabled-appearance
- **focus:** forge-app-tile-ember-focus-appearance
- **hover:** forge-app-tile-ember-hover-appearance
- **pressed:** forge-app-tile-ember-pressed-appearance

## Value Stat Card

**Soort:** variant

**Identifier:** `forge-stat-card-value`

### Doel

Statistiekkaart voor een losse operationele waarde.

### Eigenschappen

- **appearance:** forge-stat-card-value-appearance
- **component:** forge-stat-card

## Health Stat Card

**Soort:** variant

**Identifier:** `forge-stat-card-health`

### Doel

Statistiekkaart voor clustergezondheid.

### Eigenschappen

- **appearance:** forge-stat-card-health-appearance
- **component:** forge-stat-card

## Progress Stat Card

**Soort:** variant

**Identifier:** `forge-stat-card-progress`

### Doel

Statistiekkaart voor cyaan gebruiksvoortgang.

### Eigenschappen

- **appearance:** forge-stat-card-value-appearance
- **component:** forge-stat-card

## Ember Progress Stat Card

**Soort:** variant

**Identifier:** `forge-stat-card-progress-ember`

### Doel

Statistiekkaart met één schaars warm voortgangsaccent.

### Eigenschappen

- **appearance:** forge-stat-card-ember-appearance
- **component:** forge-stat-card

## Primary Button

**Soort:** componentvoorbeeld

**Identifier:** `forge-button-primary-example`

### Doel

Primair sign in voorbeeld uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-button
- **label:** Sign In
- **variant:** forge-button-primary

## Secondary Button

**Soort:** componentvoorbeeld

**Identifier:** `forge-button-secondary-example`

### Doel

Secundair annuleervoorbeeld uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-button
- **label:** Cancel
- **variant:** forge-button-secondary

## Ghost Button

**Soort:** componentvoorbeeld

**Identifier:** `forge-button-ghost-example`

### Doel

Ghost voorbeeld uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-button
- **label:** Skip
- **variant:** forge-button-ghost

## Ember Button

**Soort:** componentvoorbeeld

**Identifier:** `forge-button-ember-example`

### Doel

Schaars warm actievoorbeeld uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-button
- **label:** Forge new
- **variant:** forge-button-ember

## Default Input

**Soort:** componentvoorbeeld

**Identifier:** `forge-input-default-example`

### Doel

Regulier gebruikersveld uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-input
- **label:** Username or email
- **variant:** forge-input-default
- **waarde:** erik@thb1home.nl

## Error Input

**Soort:** componentvoorbeeld

**Identifier:** `forge-input-error-example`

### Doel

Ongeldige hostnaam met feitelijke foutmelding.

### Eigenschappen

- **component:** forge-input
- **label:** Hostname
- **melding:** Hostname is ongeldig.
- **variant:** forge-input-error
- **waarde:** lab..local

## Running Status

**Soort:** componentvoorbeeld

**Identifier:** `forge-status-running-example`

### Doel

Aantal actieve workloads uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-status
- **label:** Running
- **variant:** forge-status-running
- **waarde:** 62

## Pending Status

**Soort:** componentvoorbeeld

**Identifier:** `forge-status-pending-example`

### Doel

Aantal wachtende workloads uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-status
- **label:** Pending
- **variant:** forge-status-pending
- **waarde:** 3

## Failed Status

**Soort:** componentvoorbeeld

**Identifier:** `forge-status-failed-example`

### Doel

Aantal gefaalde workloads uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-status
- **label:** Failed
- **variant:** forge-status-failed
- **waarde:** 1

## Healthy Status

**Soort:** componentvoorbeeld

**Identifier:** `forge-status-info-example`

### Doel

Informatieve gezondheid uit het aangeleverde componentscherm.

### Eigenschappen

- **component:** forge-status
- **label:** Healthy
- **variant:** forge-status-info
- **waarde:** 98%

## ISMS App Tile

**Soort:** componentvoorbeeld

**Identifier:** `forge-app-tile-isms-example`

### Doel

Producttegel voor ISMS Challenger.

### Eigenschappen

- **beschrijving:** Information Security Management
- **component:** forge-app-tile
- **label:** ISMS Challenger
- **status:** running
- **variant:** forge-app-tile-default

## CV App Tile

**Soort:** componentvoorbeeld

**Identifier:** `forge-app-tile-cv-example`

### Doel

Zeldzame warme producttegel voor CV beheer.

### Eigenschappen

- **beschrijving:** CV beheer voor consultants
- **component:** forge-app-tile
- **label:** CV Tool
- **status:** running
- **variant:** forge-app-tile-ember

## Nodes Stat Card

**Soort:** componentvoorbeeld

**Identifier:** `forge-stat-card-nodes-example`

### Doel

Aantal actieve clusternodes.

### Eigenschappen

- **beschrijving:** All Running
- **component:** forge-stat-card
- **label:** Nodes
- **variant:** forge-stat-card-value
- **waarde:** 12

## Health Stat Card

**Soort:** componentvoorbeeld

**Identifier:** `forge-stat-card-health-example`

### Doel

Clustergezondheid als feitelijke waarde.

### Eigenschappen

- **beschrijving:** 98%
- **component:** forge-stat-card
- **label:** Cluster Health
- **variant:** forge-stat-card-health
- **waarde:** Healthy

## CPU Stat Card

**Soort:** componentvoorbeeld

**Identifier:** `forge-stat-card-cpu-example`

### Doel

Actueel CPU gebruik.

### Eigenschappen

- **component:** forge-stat-card
- **label:** CPU Usage
- **variant:** forge-stat-card-progress
- **waarde:** 24%

## Memory Stat Card

**Soort:** componentvoorbeeld

**Identifier:** `forge-stat-card-memory-example`

### Doel

Actueel geheugengebruik met één schaars koperaccent.

### Eigenschappen

- **component:** forge-stat-card
- **label:** Memory
- **variant:** forge-stat-card-progress-ember
- **waarde:** 43%

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

- **inhoud:** forge, forge-materials, forge-panel, forge-button, forge-input, forge-status, forge-app-tile, forge-stat-card, forge-button-accessibility, forge-button-primary-example, forge-input-error-example, forge-status-running-example, forge-app-tile-isms-example, forge-stat-card-nodes-example
- **leesvolgorde:** 2
- **navigatie:** html-components, css-components, css-tokens, json-tokens
- **soorten:** kleur, palet, typografie, typeschaal, materiaal, border, radius, shadow, motion, spacing, thema, appearance, token, component, variant, componentvoorbeeld, toegankelijkheid
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