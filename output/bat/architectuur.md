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
- **producten:** Homelab Dashboard, Keycloak login, Terminal, SVG Asset Catalog, CV Database, ISMS Challenger, Roadmap, Marketing en merkoppervlakken
- **stem:** Zelfverzekerd, technisch en rustig
- **taal:** Nederlands met technische termen in het Engels
- **tagline:** Sovereign Infrastructure.

## EmberForge iconen

**Soort:** assetfamilie

**Identifier:** `emberforge-iconen`

### Doel

Ordent de native producticonen als één samenhangende merkgebonden familie.

### Eigenschappen

- **assets:** emberforge-icon-dashboard, emberforge-icon-identity, emberforge-icon-terminal, emberforge-icon-assets
- **merk:** emberforge
- **type:** iconen

## EmberForge merkassets

**Soort:** assetfamilie

**Identifier:** `emberforge-merkassets`

### Doel

Ordent het native merkteken en woordmerk als één reproduceerbare merkfamilie.

### Eigenschappen

- **assets:** emberforge-merkteken, emberforge-woordmerk
- **merk:** emberforge
- **type:** merk

## EmberForge Vector Node

**Soort:** asset

**Identifier:** `emberforge-vector-node`

### Doel

Herbruikbaar technisch lijnornament voor native EmberForge vectorproducten.

### Eigenschappen

- **formaat:** svg
- **lijn:** currentColor
- **lijndikte:** 2
- **lijneinde:** round
- **lijnverbinding:** round
- **paden:** M32 6 L38 24 L56 32 L38 40 L32 58 L26 40 L8 32 L26 24 Z, M32 22 L42 32 L32 42 L22 32 Z
- **rol:** ornament
- **toegankelijkheid:** decoratief
- **viewbox:** 0 0 64 64
- **vulling:** none

## EmberForge Lichtschijf

**Soort:** asset

**Identifier:** `emberforge-light-disc`

### Doel

Levert een neutrale gevulde vectorvorm voor expliciet gecomponeerde wallpaperlichtvelden.

### Eigenschappen

- **formaat:** svg
- **lijn:** none
- **paden:** M500 20 A480 480 0 1 0 500 980 A480 480 0 1 0 500 20 Z
- **rol:** ornament
- **toegankelijkheid:** decoratief
- **viewbox:** 0 0 1000 1000
- **vulling:** currentColor

## EmberForge Dashboard Icon

**Soort:** asset

**Identifier:** `emberforge-icon-dashboard`

### Doel

Herkenbaar lijnicoon voor het EmberForge dashboardproduct.

### Eigenschappen

- **familie:** emberforge-iconen
- **formaat:** svg
- **label:** Dashboard
- **lijn:** currentColor
- **lijndikte:** 1.5
- **lijneinde:** round
- **lijnverbinding:** round
- **paden:** M4 4 L10 4 L10 10 L4 10 Z, M14 4 L20 4 L20 10 L14 10 Z, M4 14 L10 14 L10 20 L4 20 Z, M14 14 L20 14 L20 20 L14 20 Z
- **rol:** icoon
- **toegankelijkheid:** informatief
- **variant:** dashboard
- **viewbox:** 0 0 24 24
- **vulling:** none

## EmberForge Identity Icon

**Soort:** asset

**Identifier:** `emberforge-icon-identity`

### Doel

Herkenbaar lijnicoon voor identiteit en toegang.

### Eigenschappen

- **familie:** emberforge-iconen
- **formaat:** svg
- **label:** Identity
- **lijn:** currentColor
- **lijndikte:** 1.5
- **lijneinde:** round
- **lijnverbinding:** round
- **paden:** M12 3 C15 3 17 5 17 8 C17 11 15 13 12 13 C9 13 7 11 7 8 C7 5 9 3 12 3 Z, M4 21 C4 17 7 15 12 15 C17 15 20 17 20 21
- **rol:** icoon
- **toegankelijkheid:** informatief
- **variant:** identity
- **viewbox:** 0 0 24 24
- **vulling:** none

## EmberForge Terminal Icon

**Soort:** asset

**Identifier:** `emberforge-icon-terminal`

### Doel

Herkenbaar lijnicoon voor de EmberForge terminal.

### Eigenschappen

- **familie:** emberforge-iconen
- **formaat:** svg
- **label:** Terminal
- **lijn:** currentColor
- **lijndikte:** 1.5
- **lijneinde:** round
- **lijnverbinding:** round
- **paden:** M4 5 L20 5 L20 19 L4 19 Z, M7 9 L10 12 L7 15, M12 15 L16 15
- **rol:** icoon
- **toegankelijkheid:** informatief
- **variant:** terminal
- **viewbox:** 0 0 24 24
- **vulling:** none

## EmberForge Assets Icon

**Soort:** asset

**Identifier:** `emberforge-icon-assets`

### Doel

Herkenbaar lijnicoon voor de native assetcatalogus.

### Eigenschappen

- **familie:** emberforge-iconen
- **formaat:** svg
- **label:** Assets
- **lijn:** currentColor
- **lijndikte:** 1.5
- **lijneinde:** round
- **lijnverbinding:** round
- **paden:** M12 3 L20 7 L20 17 L12 21 L4 17 L4 7 Z, M4 7 L12 11 L20 7, M12 11 L12 21
- **rol:** icoon
- **toegankelijkheid:** informatief
- **variant:** assets
- **viewbox:** 0 0 24 24
- **vulling:** none

## EmberForge merkteken

**Soort:** asset

**Identifier:** `emberforge-merkteken`

### Doel

Compact technisch merkteken waarin een gesmede rand, ember en aambeeld samenkomen.

### Eigenschappen

- **familie:** emberforge-merkassets
- **formaat:** svg
- **label:** EmberForge
- **lijn:** currentColor
- **lijndikte:** 2.5
- **lijneinde:** round
- **lijnverbinding:** round
- **paden:** M48 6 L78 22 L88 52 L72 82 L48 92 L24 82 L8 52 L18 22 Z, M48 18 C59 29 63 38 59 48 C57 54 52 58 48 62 C43 58 38 53 36 47 C33 39 38 31 44 25 C44 34 47 39 51 42 C54 34 53 26 48 18 Z, M26 62 H70 L64 70 H55 V80 H41 V70 H32 Z
- **rol:** logo
- **toegankelijkheid:** informatief
- **variant:** merkteken
- **viewbox:** 0 0 96 96
- **vulling:** none

## EmberForge woordmerk

**Soort:** asset

**Identifier:** `emberforge-woordmerk`

### Doel

Horizontaal technisch woordmerk voor brede EmberForge merkoppervlakken.

### Eigenschappen

- **familie:** emberforge-merkassets
- **formaat:** svg
- **label:** EmberForge
- **lijn:** currentColor
- **lijndikte:** 3
- **lijneinde:** round
- **lijnverbinding:** round
- **paden:** M12 16 V64 M12 16 H50 M12 40 H44 M12 64 H50, M66 64 V16 L86 42 L106 16 V64, M124 16 V64 M124 16 H148 C158 16 162 22 162 28 C162 34 158 40 148 40 H124 M148 40 C158 40 164 46 164 52 C164 59 159 64 148 64 H124, M182 16 V64 M182 16 H220 M182 40 H214 M182 64 H220, M238 64 V16 H258 C269 16 274 22 274 28 C274 36 269 40 258 40 H238 M256 40 L276 64, M296 64 V16 H334 M296 40 H328, M368 16 H384 C395 16 400 24 400 40 C400 56 395 64 384 64 H368 C357 64 352 56 352 40 C352 24 357 16 368 16 Z, M418 64 V16 H438 C449 16 454 22 454 28 C454 36 449 40 438 40 H418 M436 40 L456 64, M524 26 C519 19 512 16 500 16 H492 C481 16 476 24 476 40 C476 56 481 64 492 64 H510 C519 64 524 58 524 48 V40 H506, M542 16 V64 M542 16 H580 M542 40 H574 M542 64 H580
- **rol:** logo
- **toegankelijkheid:** informatief
- **variant:** woordmerk
- **viewbox:** 0 0 592 80
- **vulling:** none

## EmberForge Circle of Fifths

**Soort:** muziekcirkel

**Identifier:** `emberforge-circle-of-fifths`

### Doel

Publiceert twaalf majeurtoonsoorten, relatieve mineurtoonsoorten en voortekens als functionele gitaarreferentie.

### Eigenschappen

- **majeur:** C, G, D, A, E, B, F#/Gb, Db, Ab, Eb, Bb, F
- **mineur:** Am, Em, Bm, F#m, C#m, G#m, D#m/Ebm, Bbm, Fm, Cm, Gm, Dm
- **voortekens:** 0, 1#, 2#, 3#, 4#, 5#, 6#/6b, 5b, 4b, 3b, 2b, 1b

## EmberForge Wallpapers

**Soort:** wallpaperfamilie

**Identifier:** `emberforge-wallpapers`

### Doel

Ordent de expliciete ultrawide en desktop canvasformaten als één merkgebonden familie.

### Eigenschappen

- **merk:** emberforge
- **wallpapers:** emberforge-ultrawide-wallpaper, emberforge-desktop-wallpaper

## EmberForge Ultrawide Wallpaper

**Soort:** wallpaper

**Identifier:** `emberforge-ultrawide-wallpaper`

### Doel

Legt een rustige 3840 bij 1080 EmberForge wallpaper vast als reproduceerbaar beeldproduct.

### Eigenschappen

- **breedte:** 3840
- **canvas:** canvas
- **familie:** emberforge-wallpapers
- **formaat:** png
- **hoogte:** 1080
- **lagen:** emberforge-wallpaper-lichtlaag, emberforge-wallpaper-ornamentlaag, emberforge-wallpaper-muzieklaag, emberforge-wallpaper-merklaag
- **merk:** emberforge
- **variant:** ultrawide-3840x1080
- **wereld:** beckeringh-palace

## EmberForge Wallpaper Lichtlaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-wallpaper-lichtlaag`

### Doel

Componeert koelblauw hoofdlicht en maximaal twee begrensde warme accenten achter de muziekinformatie.

### Eigenschappen

- **plaatsingen:** emberforge-ultrawide-cool-light-outer, emberforge-ultrawide-cool-light-inner, emberforge-ultrawide-warm-light-outer, emberforge-ultrawide-warm-light-inner
- **rol:** ornament
- **wallpaper:** emberforge-ultrawide-wallpaper

## EmberForge Wallpaper Muzieklaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-wallpaper-muzieklaag`

### Doel

Draagt de functionele Circle of Fifths volledig binnen de veilige beeldmarge.

### Eigenschappen

- **plaatsingen:** emberforge-wallpaper-circle-of-fifths
- **rol:** illustratie
- **wallpaper:** emberforge-ultrawide-wallpaper

## EmberForge Wallpaper Ornamentlaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-wallpaper-ornamentlaag`

### Doel

Ordent twee rustige technische lijnornamenten binnen de canvasgrens.

### Eigenschappen

- **plaatsingen:** emberforge-vector-node-left, emberforge-vector-node-right
- **rol:** ornament
- **wallpaper:** emberforge-ultrawide-wallpaper

## EmberForge Wallpaper Merklaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-wallpaper-merklaag`

### Doel

Ordent het merkteken en woordmerk als afzonderlijke merkplaatsingen.

### Eigenschappen

- **plaatsingen:** emberforge-wallpaper-merkteken
- **rol:** merk
- **wallpaper:** emberforge-ultrawide-wallpaper

## EmberForge Vector Node Links

**Soort:** assetplaatsing

**Identifier:** `emberforge-vector-node-left`

### Doel

Plaatst het technische lijnornament met ruime marge links.

### Eigenschappen

- **asset:** emberforge-vector-node
- **breedte:** 840
- **dekking:** 0.14
- **fit:** contain
- **hoogte:** 840
- **kleur:** interaction
- **laag:** emberforge-wallpaper-ornamentlaag
- **x:** 120
- **y:** 120

## EmberForge Ultrawide Koel Licht Buiten

**Soort:** assetplaatsing

**Identifier:** `emberforge-ultrawide-cool-light-outer`

### Doel

Legt een brede, zachte koelblauwe lichtbasis achter de functionele muziekcirkel.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 1320
- **dekking:** 0.06
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 1080
- **kleur:** interaction
- **laag:** emberforge-wallpaper-lichtlaag
- **x:** 1260
- **y:** 0

## EmberForge Ultrawide Koel Licht Binnen

**Soort:** assetplaatsing

**Identifier:** `emberforge-ultrawide-cool-light-inner`

### Doel

Verdicht het koelblauwe licht rond de informatieringen zonder hun contrast te verminderen.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 1020
- **dekking:** 0.09
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 1020
- **kleur:** interaction
- **laag:** emberforge-wallpaper-lichtlaag
- **x:** 1410
- **y:** 30

## EmberForge Ultrawide Warm Licht Buiten

**Soort:** assetplaatsing

**Identifier:** `emberforge-ultrawide-warm-light-outer`

### Doel

Plaatst het eerste begrensde emberaccent onder de Circle of Fifths.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 720
- **dekking:** 0.08
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 480
- **kleur:** accent
- **laag:** emberforge-wallpaper-lichtlaag
- **x:** 1560
- **y:** 590

## EmberForge Ultrawide Warm Licht Binnen

**Soort:** assetplaatsing

**Identifier:** `emberforge-ultrawide-warm-light-inner`

### Doel

Concentreert het tweede en laatste emberaccent rond het centrale merkteken.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 420
- **dekking:** 0.14
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 360
- **kleur:** accent
- **laag:** emberforge-wallpaper-lichtlaag
- **x:** 1710
- **y:** 690

## EmberForge Vector Node Rechts

**Soort:** assetplaatsing

**Identifier:** `emberforge-vector-node-right`

### Doel

Plaatst het technische lijnornament symmetrisch rechts.

### Eigenschappen

- **asset:** emberforge-vector-node
- **breedte:** 840
- **dekking:** 0.14
- **fit:** contain
- **hoogte:** 840
- **kleur:** interaction
- **laag:** emberforge-wallpaper-ornamentlaag
- **x:** 2880
- **y:** 120

## EmberForge Wallpaper Merkteken

**Soort:** assetplaatsing

**Identifier:** `emberforge-wallpaper-merkteken`

### Doel

Plaatst het merkteken centraal binnen de ultrawide compositie.

### Eigenschappen

- **asset:** emberforge-merkteken
- **breedte:** 240
- **dekking:** 1
- **fit:** contain
- **hoogte:** 240
- **kleur:** accent
- **laag:** emberforge-wallpaper-merklaag
- **x:** 1800
- **y:** 420

## EmberForge Ultrawide Circle of Fifths

**Soort:** assetplaatsing

**Identifier:** `emberforge-wallpaper-circle-of-fifths`

### Doel

Plaatst de volledige functionele muziekcirkel centraal en zonder afsnijding.

### Eigenschappen

- **asset:** emberforge-circle-of-fifths
- **breedte:** 1020
- **dekking:** 1
- **fit:** contain
- **hoogte:** 1020
- **kleur:** interaction
- **laag:** emberforge-wallpaper-muzieklaag
- **x:** 1410
- **y:** 30

## EmberForge Desktop Wallpaper

**Soort:** wallpaper

**Identifier:** `emberforge-desktop-wallpaper`

### Doel

Legt een rustige 1900 bij 1200 EmberForge desktopwallpaper vast met eigen expliciete geometrie.

### Eigenschappen

- **breedte:** 1900
- **canvas:** canvas
- **familie:** emberforge-wallpapers
- **formaat:** png
- **hoogte:** 1200
- **lagen:** emberforge-desktop-lichtlaag, emberforge-desktop-ornamentlaag, emberforge-desktop-muzieklaag, emberforge-desktop-merklaag
- **merk:** emberforge
- **variant:** desktop-1900x1200
- **wereld:** beckeringh-palace

## EmberForge Desktop Lichtlaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-desktop-lichtlaag`

### Doel

Componeert eigen koelblauw hoofdlicht en twee begrensde warme accenten voor het desktopcanvas.

### Eigenschappen

- **plaatsingen:** emberforge-desktop-cool-light-outer, emberforge-desktop-cool-light-inner, emberforge-desktop-warm-light-outer, emberforge-desktop-warm-light-inner
- **rol:** ornament
- **wallpaper:** emberforge-desktop-wallpaper

## EmberForge Desktop Muzieklaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-desktop-muzieklaag`

### Doel

Draagt de functionele Circle of Fifths met een eigen desktopplaatsing.

### Eigenschappen

- **plaatsingen:** emberforge-desktop-circle-of-fifths
- **rol:** illustratie
- **wallpaper:** emberforge-desktop-wallpaper

## EmberForge Desktop Ornamentlaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-desktop-ornamentlaag`

### Doel

Ordent twee rustige technische lijnornamenten voor het 1900 bij 1200 canvas.

### Eigenschappen

- **plaatsingen:** emberforge-desktop-vector-node-left, emberforge-desktop-vector-node-right
- **rol:** ornament
- **wallpaper:** emberforge-desktop-wallpaper

## EmberForge Desktop Merklaag

**Soort:** wallpaperlaag

**Identifier:** `emberforge-desktop-merklaag`

### Doel

Ordent merkteken en woordmerk met eigen desktopplaatsingen.

### Eigenschappen

- **plaatsingen:** emberforge-desktop-merkteken
- **rol:** merk
- **wallpaper:** emberforge-desktop-wallpaper

## EmberForge Desktop Vector Node Links

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-vector-node-left`

### Doel

Plaatst het technische lijnornament met ruime marge links op het desktopcanvas.

### Eigenschappen

- **asset:** emberforge-vector-node
- **breedte:** 560
- **dekking:** 0.08
- **fit:** contain
- **hoogte:** 560
- **kleur:** interaction
- **laag:** emberforge-desktop-ornamentlaag
- **x:** 80
- **y:** 250

## EmberForge Desktop Koel Licht Buiten

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-cool-light-outer`

### Doel

Legt een brede koelblauwe lichtbasis achter de zelfstandig geplaatste desktopcirkel.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 1200
- **dekking:** 0.06
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 1200
- **kleur:** interaction
- **laag:** emberforge-desktop-lichtlaag
- **x:** 350
- **y:** 0

## EmberForge Desktop Koel Licht Binnen

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-cool-light-inner`

### Doel

Verdicht het koele licht binnen de desktopcompositie zonder automatische schaling.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 1000
- **dekking:** 0.09
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 1000
- **kleur:** interaction
- **laag:** emberforge-desktop-lichtlaag
- **x:** 450
- **y:** 100

## EmberForge Desktop Warm Licht Buiten

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-warm-light-outer`

### Doel

Plaatst het eerste begrensde emberaccent laag in de desktopcompositie.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 650
- **dekking:** 0.08
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 500
- **kleur:** accent
- **laag:** emberforge-desktop-lichtlaag
- **x:** 625
- **y:** 680

## EmberForge Desktop Warm Licht Binnen

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-warm-light-inner`

### Doel

Concentreert het tweede en laatste emberaccent rond het desktopmerkteken.

### Eigenschappen

- **asset:** emberforge-light-disc
- **breedte:** 360
- **dekking:** 0.14
- **effect:** radial-glow
- **fit:** contain
- **hoogte:** 340
- **kleur:** accent
- **laag:** emberforge-desktop-lichtlaag
- **x:** 770
- **y:** 790

## EmberForge Desktop Vector Node Rechts

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-vector-node-right`

### Doel

Plaatst het technische lijnornament met ruime marge rechts op het desktopcanvas.

### Eigenschappen

- **asset:** emberforge-vector-node
- **breedte:** 560
- **dekking:** 0.08
- **fit:** contain
- **hoogte:** 560
- **kleur:** interaction
- **laag:** emberforge-desktop-ornamentlaag
- **x:** 1260
- **y:** 250

## EmberForge Desktop Merkteken

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-merkteken`

### Doel

Plaatst het merkteken centraal binnen het desktopcanvas.

### Eigenschappen

- **asset:** emberforge-merkteken
- **breedte:** 240
- **dekking:** 1
- **fit:** contain
- **hoogte:** 240
- **kleur:** accent
- **laag:** emberforge-desktop-merklaag
- **x:** 830
- **y:** 480

## EmberForge Desktop Circle of Fifths

**Soort:** assetplaatsing

**Identifier:** `emberforge-desktop-circle-of-fifths`

### Doel

Plaatst de volledige functionele muziekcirkel op het 1900 bij 1200 canvas.

### Eigenschappen

- **asset:** emberforge-circle-of-fifths
- **breedte:** 1200
- **dekking:** 1
- **fit:** contain
- **hoogte:** 1100
- **kleur:** interaction
- **laag:** emberforge-desktop-muzieklaag
- **x:** 350
- **y:** 50

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

## Forge Terminal Appearance

**Soort:** appearance

**Identifier:** `forge-terminal-appearance`

### Doel

Statisch terminalvenster op het diepste Forge oppervlak.

### Eigenschappen

- **accent:** interaction
- **body-style:** body
- **border:** regular
- **caption-style:** caption
- **foreground:** foreground
- **heading-style:** heading
- **label-style:** label
- **material:** field
- **motion:** slow
- **offset:** rest
- **outline:** outline
- **radius:** medium
- **shadow:** high
- **spacing:** none

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

## Forge Terminal Accessibility

**Soort:** toegankelijkheid

**Identifier:** `forge-terminal-accessibility`

### Doel

Benoemt een statische terminalweergave als niet-interactieve groep.

### Eigenschappen

- **disabled:** niet-van-toepassing
- **focus:** geen
- **naambron:** label
- **rol:** groep
- **toetsenbord:** geen

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

## Forge Terminal

**Soort:** component

**Identifier:** `forge-terminal`

### Doel

Statische terminalweergave met vensterchrome, systeemvelden en prompt.

### Eigenschappen

- **anatomie:** label, venstertitel, vensterknoppen, tabs, actieve-tab, markering, gebruiker, host, sleutels, waarden, pad, prompt, cursor
- **appearance:** forge-terminal-appearance
- **rol:** terminal
- **toegankelijkheid:** forge-terminal-accessibility

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

## NordForge Neofetch

**Soort:** variant

**Identifier:** `forge-terminal-neofetch`

### Doel

Statische EmberForge OS systeemidentiteit uit de terminalbron.

### Eigenschappen

- **appearance:** forge-terminal-appearance
- **component:** forge-terminal

## Primary Button

**Soort:** componentvoorbeeld

**Identifier:** `forge-button-primary-example`

### Doel

Primair sign in voorbeeld uit het aangeleverde componentscherm.

### Eigenschappen

- **actietype:** submit
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
- **invoertype:** email
- **label:** Username or email
- **variant:** forge-input-default
- **waarde:** erik@thb1home.nl

## Password Input

**Soort:** componentvoorbeeld

**Identifier:** `forge-input-password-example`

### Doel

Wachtwoordveld voor de EmberForge login productsurface.

### Eigenschappen

- **component:** forge-input
- **invoertype:** password
- **label:** Password
- **variant:** forge-input-default
- **waarde:** not-a-secret

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

## EmberForge Terminal

**Soort:** componentvoorbeeld

**Identifier:** `forge-terminal-neofetch-example`

### Doel

Statische bronweergave van de EmberForge OS terminal zonder shelluitvoering of actuele telemetrie.

### Eigenschappen

- **actieve-tab:** ~/emberforge
- **component:** forge-terminal
- **cursor:** ▍
- **gebruiker:** thb1
- **host:** emberforge
- **label:** EmberForge terminal systeemoverzicht
- **markering:** ✦
- **pad:** ~
- **prompt:** $
- **sleutels:** OS, Host, Uptime, Shell, Resolution, WM, Icons, Terminal, CPU, GPU, Memory, Disk, Cluster
- **tabs:** ~/emberforge, k9s, +
- **variant:** forge-terminal-neofetch
- **vensterknoppen:** sluiten, minimaliseren, maximaliseren
- **venstertitel:** thb1@emberforge: ~ — wezterm — 120×32
- **waarden:** EmberForge OS · 6.6.12-ember, emberforge (k3s control-plane), 5 days, 14 hours, 22 mins, zsh 5.9, 1920×1080, i3 · NordForge theme, Tela-circle, wezterm 20240203, AMD Ryzen 9 5950X (16) @ 4.9GHz, NVIDIA RTX A4000, 32.1 GiB / 64.0 GiB, 412 GiB / 2.0 TiB (Longhorn), homelab · 12 nodes · 98% healthy

## Primitieven

**Soort:** referentiesectie

**Identifier:** `forge-reference-primitives`

### Doel

Palet, typografie, typeschaal, materiaal, randen, radius, schaduw, motion, spacing en art direction met hun opgeloste waarden.

### Eigenschappen

- **rol:** primitieven

## Tokens

**Soort:** referentiesectie

**Identifier:** `forge-reference-tokens`

### Doel

Herbruikbare ontwerpwaarden met hun type, referentie en normatieve bedoeling.

### Eigenschappen

- **rol:** tokens

## Componenttoestanden

**Soort:** referentiesectie

**Identifier:** `forge-reference-states`

### Doel

De expliciete mapping van rust, hover, focus, pressed en disabled naar appearances.

### Eigenschappen

- **rol:** toestanden

## Voorbeelden

**Soort:** referentiesectie

**Identifier:** `forge-reference-examples`

### Doel

Productgedragen voorbeeldinhoud voor iedere gemigreerde EmberForge componentvariant.

### Eigenschappen

- **rol:** voorbeelden

## Toegankelijkheidscontracten

**Soort:** referentiesectie

**Identifier:** `forge-reference-accessibility`

### Doel

Naam, rol, waarde, fout, disabled, focus en toetsenbordgedrag per component.

### Eigenschappen

- **rol:** toegankelijkheid

## Wereld en identiteit

**Soort:** informatiegebied

**Identifier:** `palace-world`

### Doel

De digitale wereld, haar merk en haar reproduceerbare bronassets.

### Eigenschappen

- **inhoud:** beckeringh-palace, emberforge-merkassets, emberforge-vector-node, emberforge-circle-of-fifths
- **leesvolgorde:** 1
- **navigatie:** forge-dashboard-html, forge-dashboard-grafana, emberforge-svg-asset-catalog-html, emberforge-vector-node-svg, emberforge-merkteken-svg, emberforge-woordmerk-svg
- **soorten:** wereld, merk, assetfamilie, asset, muziekcirkel
- **toegankelijkheidslabel:** Wereld en identiteit, overzicht van wereld, merk, assetfamilies en bronassets

## Forge ontwerpsysteem

**Soort:** informatiegebied

**Identifier:** `forge-design-system`

### Doel

De ontwerpprimitieven, tokens en componentcontracten van de Forge-identiteit.

### Eigenschappen

- **inhoud:** forge, forge-materials, forge-panel, forge-button, forge-input, forge-status, forge-app-tile, forge-stat-card, forge-button-accessibility, forge-button-primary-example, forge-input-error-example, forge-status-running-example, forge-app-tile-isms-example, forge-stat-card-nodes-example, forge-reference-primitives
- **leesvolgorde:** 2
- **navigatie:** forge-design-system-reference-html, css-components, css-tokens, json-tokens
- **soorten:** kleur, palet, typografie, typeschaal, materiaal, border, radius, shadow, motion, spacing, thema, appearance, token, component, variant, componentvoorbeeld, toegankelijkheid, referentiesectie
- **toegankelijkheidslabel:** Forge ontwerpsysteem, overzicht van ontwerpprimitieven en componenten

## Productfamilie

**Soort:** informatiegebied

**Identifier:** `palace-product-family`

### Doel

De composities, layouts en uitvoerproducten die uit dezelfde wereld worden gegenereerd.

### Eigenschappen

- **inhoud:** forge-dashboard, forge-dashboard-ultrawide, emberforge-homelab-dashboard, emberforge-homelab-dashboard-responsive, emberforge-wallpapers, emberforge-ultrawide-wallpaper, emberforge-desktop-wallpaper, emberforge-homelab-dashboard-html, emberforge-homelab-dashboard-grafana, emberforge-ultrawide-wallpaper-png, emberforge-desktop-wallpaper-png, project-status-html, forge-design-system-reference-html, emberforge-svg-asset-catalog-html
- **leesvolgorde:** 3
- **navigatie:** emberforge-homelab-dashboard-html, emberforge-homelab-dashboard-grafana, emberforge-ultrawide-wallpaper-png, emberforge-ultrawide-wallpaper-manifest, emberforge-desktop-wallpaper-png, emberforge-desktop-wallpaper-manifest, project-status-html, project-status-grafana
- **soorten:** homepagegebied, compositie, componentinstantie, layout, region, wallpaperfamilie, wallpaper, wallpaperlaag, assetplaatsing, product, renderdoel
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

## EmberForge Homelab

**Soort:** compositie

**Identifier:** `emberforge-homelab-dashboard`

### Doel

Operationeel overzicht van clustercapaciteit, workloadstatus en homelab applicaties.

### Eigenschappen

- **instanties:** homelab-stat-nodes, homelab-stat-health, homelab-stat-cpu, homelab-stat-memory, homelab-status-running, homelab-status-pending, homelab-status-failed, homelab-status-healthy, homelab-app-isms, homelab-app-cv

## Nodes

**Soort:** componentinstantie

**Identifier:** `homelab-stat-nodes`

### Doel

Aantal actieve clusternodes.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-stat-card-nodes-example

## Cluster Health

**Soort:** componentinstantie

**Identifier:** `homelab-stat-health`

### Doel

Actuele gezondheid van het cluster.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-stat-card-health-example

## CPU Usage

**Soort:** componentinstantie

**Identifier:** `homelab-stat-cpu`

### Doel

Actueel CPU gebruik.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-stat-card-cpu-example

## Memory

**Soort:** componentinstantie

**Identifier:** `homelab-stat-memory`

### Doel

Actueel geheugengebruik.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-stat-card-memory-example

## Running

**Soort:** componentinstantie

**Identifier:** `homelab-status-running`

### Doel

Aantal actieve workloads.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-status-running-example

## Pending

**Soort:** componentinstantie

**Identifier:** `homelab-status-pending`

### Doel

Aantal wachtende workloads.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-status-pending-example

## Failed

**Soort:** componentinstantie

**Identifier:** `homelab-status-failed`

### Doel

Aantal gefaalde workloads.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-status-failed-example

## Healthy

**Soort:** componentinstantie

**Identifier:** `homelab-status-healthy`

### Doel

Samengevatte clustergezondheid.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-status-info-example

## ISMS Challenger

**Soort:** componentinstantie

**Identifier:** `homelab-app-isms`

### Doel

Homelab applicatie voor Information Security Management.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-app-tile-isms-example

## CV Tool

**Soort:** componentinstantie

**Identifier:** `homelab-app-cv`

### Doel

Homelab applicatie voor consultant CV beheer.

### Eigenschappen

- **compositie:** emberforge-homelab-dashboard
- **voorbeeld:** forge-app-tile-cv-example

## EmberForge Homelab Responsive

**Soort:** layout

**Identifier:** `emberforge-homelab-dashboard-responsive`

### Doel

Ordent statistieken, statussen en applicaties op desktop en compact scherm.

### Eigenschappen

- **columns:** 4
- **compact-columns:** 2
- **regions:** homelab-stat-nodes-region, homelab-stat-health-region, homelab-stat-cpu-region, homelab-stat-memory-region, homelab-status-running-region, homelab-status-pending-region, homelab-status-failed-region, homelab-status-healthy-region, homelab-app-isms-region, homelab-app-cv-region
- **responsive-breakpoint:** 960
- **rows:** 3
- **type:** grid

## Nodes statistiek

**Soort:** region

**Identifier:** `homelab-stat-nodes-region`

### Doel

Eerste statistiekpositie.

### Eigenschappen

- **column:** 1
- **column-span:** 1
- **compact-order:** 1
- **instantie:** homelab-stat-nodes
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 1
- **row-span:** 1

## Gezondheid statistiek

**Soort:** region

**Identifier:** `homelab-stat-health-region`

### Doel

Tweede statistiekpositie.

### Eigenschappen

- **column:** 2
- **column-span:** 1
- **compact-order:** 2
- **instantie:** homelab-stat-health
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 1
- **row-span:** 1

## CPU statistiek

**Soort:** region

**Identifier:** `homelab-stat-cpu-region`

### Doel

Derde statistiekpositie.

### Eigenschappen

- **column:** 3
- **column-span:** 1
- **compact-order:** 3
- **instantie:** homelab-stat-cpu
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 1
- **row-span:** 1

## Geheugen statistiek

**Soort:** region

**Identifier:** `homelab-stat-memory-region`

### Doel

Vierde statistiekpositie.

### Eigenschappen

- **column:** 4
- **column-span:** 1
- **compact-order:** 4
- **instantie:** homelab-stat-memory
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 1
- **row-span:** 1

## Running status

**Soort:** region

**Identifier:** `homelab-status-running-region`

### Doel

Eerste statuspositie.

### Eigenschappen

- **column:** 1
- **column-span:** 1
- **compact-order:** 5
- **instantie:** homelab-status-running
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 2
- **row-span:** 1

## Pending status

**Soort:** region

**Identifier:** `homelab-status-pending-region`

### Doel

Tweede statuspositie.

### Eigenschappen

- **column:** 2
- **column-span:** 1
- **compact-order:** 6
- **instantie:** homelab-status-pending
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 2
- **row-span:** 1

## Failed status

**Soort:** region

**Identifier:** `homelab-status-failed-region`

### Doel

Derde statuspositie.

### Eigenschappen

- **column:** 3
- **column-span:** 1
- **compact-order:** 7
- **instantie:** homelab-status-failed
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 2
- **row-span:** 1

## Healthy status

**Soort:** region

**Identifier:** `homelab-status-healthy-region`

### Doel

Vierde statuspositie.

### Eigenschappen

- **column:** 4
- **column-span:** 1
- **compact-order:** 8
- **instantie:** homelab-status-healthy
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 2
- **row-span:** 1

## ISMS applicatie

**Soort:** region

**Identifier:** `homelab-app-isms-region`

### Doel

Eerste applicatiepositie.

### Eigenschappen

- **column:** 1
- **column-span:** 2
- **compact-order:** 9
- **instantie:** homelab-app-isms
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 3
- **row-span:** 1

## CV applicatie

**Soort:** region

**Identifier:** `homelab-app-cv-region`

### Doel

Tweede applicatiepositie.

### Eigenschappen

- **column:** 3
- **column-span:** 2
- **compact-order:** 10
- **instantie:** homelab-app-cv
- **layout:** emberforge-homelab-dashboard-responsive
- **row:** 3
- **row-span:** 1

## EmberForge Homelab Dashboard

**Soort:** product

**Identifier:** `emberforge-homelab-dashboard-html`

### Doel

Responsief homelab overzicht van statistieken, statussen en applicaties.

### Eigenschappen

- **backend:** html
- **compositie:** emberforge-homelab-dashboard
- **layout:** emberforge-homelab-dashboard-responsive
- **mode:** interactive
- **pad:** output/products/emberforge-homelab-dashboard.html
- **wereld:** beckeringh-palace

## EmberForge Homelab Dashboard Grafana

**Soort:** product

**Identifier:** `emberforge-homelab-dashboard-grafana`

### Doel

Het native homelab overzicht als importeerbaar Grafana dashboard genereren.

### Eigenschappen

- **backend:** grafana
- **compositie:** emberforge-homelab-dashboard
- **layout:** emberforge-homelab-dashboard-responsive
- **mode:** interactive
- **pad:** output/products/emberforge-homelab-dashboard.grafana.json
- **wereld:** beckeringh-palace

## EmberForge Sign In

**Soort:** compositie

**Identifier:** `emberforge-keycloak-login`

### Doel

Rustige native login surface voor de EmberForge Keycloak entree.

### Eigenschappen

- **instanties:** keycloak-login-identity, keycloak-login-password, keycloak-login-submit
- **rol:** login-formulier

## Username or email

**Soort:** componentinstantie

**Identifier:** `keycloak-login-identity`

### Doel

Identiteitsveld voor de EmberForge login.

### Eigenschappen

- **compositie:** emberforge-keycloak-login
- **voorbeeld:** forge-input-default-example

## Password

**Soort:** componentinstantie

**Identifier:** `keycloak-login-password`

### Doel

Wachtwoordveld voor de EmberForge login.

### Eigenschappen

- **compositie:** emberforge-keycloak-login
- **voorbeeld:** forge-input-password-example

## Sign In

**Soort:** componentinstantie

**Identifier:** `keycloak-login-submit`

### Doel

Primaire submitactie van de EmberForge login.

### Eigenschappen

- **compositie:** emberforge-keycloak-login
- **voorbeeld:** forge-button-primary-example

## EmberForge Keycloak Login Responsive

**Soort:** layout

**Identifier:** `emberforge-keycloak-login-responsive`

### Doel

Ordent identiteit, wachtwoord en submitactie als compact loginformulier.

### Eigenschappen

- **columns:** 1
- **compact-columns:** 1
- **regions:** keycloak-login-identity-region, keycloak-login-password-region, keycloak-login-submit-region
- **responsive-breakpoint:** 640
- **rows:** 3
- **type:** grid

## Login identiteit

**Soort:** region

**Identifier:** `keycloak-login-identity-region`

### Doel

Eerste formulierpositie.

### Eigenschappen

- **column:** 1
- **column-span:** 1
- **compact-order:** 1
- **instantie:** keycloak-login-identity
- **layout:** emberforge-keycloak-login-responsive
- **row:** 1
- **row-span:** 1

## Login wachtwoord

**Soort:** region

**Identifier:** `keycloak-login-password-region`

### Doel

Tweede formulierpositie.

### Eigenschappen

- **column:** 1
- **column-span:** 1
- **compact-order:** 2
- **instantie:** keycloak-login-password
- **layout:** emberforge-keycloak-login-responsive
- **row:** 2
- **row-span:** 1

## Login submit

**Soort:** region

**Identifier:** `keycloak-login-submit-region`

### Doel

Derde formulierpositie.

### Eigenschappen

- **column:** 1
- **column-span:** 1
- **compact-order:** 3
- **instantie:** keycloak-login-submit
- **layout:** emberforge-keycloak-login-responsive
- **row:** 3
- **row-span:** 1

## EmberForge Keycloak Login

**Soort:** product

**Identifier:** `emberforge-keycloak-login-html`

### Doel

De native EmberForge login surface zonder authenticatieconfiguratie genereren.

### Eigenschappen

- **backend:** html
- **compositie:** emberforge-keycloak-login
- **layout:** emberforge-keycloak-login-responsive
- **mode:** interactive
- **pad:** output/products/emberforge-keycloak-login.html
- **wereld:** beckeringh-palace

## EmberForge Terminal

**Soort:** compositie

**Identifier:** `emberforge-terminal`

### Doel

Statische EmberForge OS terminalweergave met bronvoorbeeldwaarden.

### Eigenschappen

- **instanties:** emberforge-terminal-session
- **rol:** terminal-sessie

## NordForge neofetch

**Soort:** componentinstantie

**Identifier:** `emberforge-terminal-session`

### Doel

Statisch systeemoverzicht zonder uitvoerbare shell of actuele telemetrie.

### Eigenschappen

- **compositie:** emberforge-terminal
- **voorbeeld:** forge-terminal-neofetch-example

## EmberForge Terminal Stack

**Soort:** layout

**Identifier:** `emberforge-terminal-stack`

### Doel

Plaatst de statische terminal als één zelfstandige productsurface.

### Eigenschappen

- **direction:** vertical
- **regions:** emberforge-terminal-region
- **type:** stack

## Terminalsessie

**Soort:** region

**Identifier:** `emberforge-terminal-region`

### Doel

Enige inhoudsregio van de EmberForge terminal productsurface.

### Eigenschappen

- **instantie:** emberforge-terminal-session
- **layout:** emberforge-terminal-stack

## EmberForge Terminal

**Soort:** product

**Identifier:** `emberforge-terminal-html`

### Doel

De geverifieerde terminal surface statisch genereren zonder shelluitvoering of actuele telemetrie.

### Eigenschappen

- **backend:** html
- **compositie:** emberforge-terminal
- **layout:** emberforge-terminal-stack
- **mode:** static
- **pad:** output/products/emberforge-terminal.html
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

## EmberForge Design System Referentie

**Soort:** compositie

**Identifier:** `forge-design-system-reference-composition`

### Doel

Ordent de volledige designsystem referentie als één productinhoud.

### Eigenschappen

- **instanties:** forge-design-system-reference-content

## EmberForge ontwerpcontract

**Soort:** componentinstantie

**Identifier:** `forge-design-system-reference-content`

### Doel

Navigeerbare referentie voor het opgeloste EmberForge ontwerpsysteem.

### Eigenschappen

- **component:** forge-panel
- **compositie:** forge-design-system-reference-composition
- **navigatie:** css-components, css-tokens, json-tokens
- **variant:** forge-panel-compact

## EmberForge Referentie Stack

**Soort:** layout

**Identifier:** `forge-design-system-reference-stack`

### Doel

Plaatst de samenhangende designsystem referentie in één verticale productregio.

### Eigenschappen

- **direction:** vertical
- **regions:** forge-design-system-reference-region
- **type:** stack

## Designsystem referentieregio

**Soort:** region

**Identifier:** `forge-design-system-reference-region`

### Doel

Enige inhoudsregio van het EmberForge designsystem referentieproduct.

### Eigenschappen

- **instantie:** forge-design-system-reference-content
- **layout:** forge-design-system-reference-stack

## EmberForge Design System Referentie

**Soort:** product

**Identifier:** `forge-design-system-reference-html`

### Doel

Tokens, primitives, componenttoestanden, voorbeelden en toegankelijkheidscontracten als één navigeerbaar product.

### Eigenschappen

- **backend:** html
- **compositie:** forge-design-system-reference-composition
- **inhoud:** design-system
- **layout:** forge-design-system-reference-stack
- **mode:** static
- **pad:** output/products/components.html
- **referentiesecties:** forge-reference-primitives, forge-reference-tokens, forge-reference-states, forge-reference-examples, forge-reference-accessibility
- **wereld:** beckeringh-palace

## EmberForge SVG Asset Catalog

**Soort:** compositie

**Identifier:** `emberforge-svg-asset-catalog-composition`

### Doel

Ordent alle native SVG assets als één expliciet catalogusproduct.

### Eigenschappen

- **instanties:** emberforge-svg-asset-catalog-content

## Native SVG assets

**Soort:** componentinstantie

**Identifier:** `emberforge-svg-asset-catalog-content`

### Doel

Navigeerbare previews en contractmetadata van alle getypeerde SVG assets.

### Eigenschappen

- **component:** forge-panel
- **compositie:** emberforge-svg-asset-catalog-composition
- **variant:** forge-panel-compact

## EmberForge SVG Asset Catalog Stack

**Soort:** layout

**Identifier:** `emberforge-svg-asset-catalog-stack`

### Doel

Plaatst de volledige native SVG assetcatalogus in één verticale productregio.

### Eigenschappen

- **direction:** vertical
- **regions:** emberforge-svg-asset-catalog-region
- **type:** stack

## SVG assetcatalogusregio

**Soort:** region

**Identifier:** `emberforge-svg-asset-catalog-region`

### Doel

Enige inhoudsregio van het EmberForge SVG assetcatalogusproduct.

### Eigenschappen

- **instantie:** emberforge-svg-asset-catalog-content
- **layout:** emberforge-svg-asset-catalog-stack

## EmberForge SVG Asset Catalog

**Soort:** product

**Identifier:** `emberforge-svg-asset-catalog-html`

### Doel

Alle getypeerde SVG assets als één navigeerbaar en reproduceerbaar catalogusproduct.

### Eigenschappen

- **assets:** emberforge-vector-node, emberforge-light-disc, emberforge-icon-dashboard, emberforge-icon-identity, emberforge-icon-terminal, emberforge-icon-assets, emberforge-merkteken, emberforge-woordmerk
- **backend:** html
- **compositie:** emberforge-svg-asset-catalog-composition
- **inhoud:** asset-catalog
- **layout:** emberforge-svg-asset-catalog-stack
- **mode:** static
- **pad:** output/products/assets.html
- **wereld:** beckeringh-palace

## Beckeringh Palace

**Soort:** compositie

**Identifier:** `beckeringh-palace-homepage-composition`

### Doel

Toegangspoort tot de digitale wereld, het ontwerpsysteem, de native assetcatalogus, de EmberForge productsurfaces en de actuele projectstatus.

### Eigenschappen

- **instanties:** homepage-intro, homepage-world, homepage-design-system, homepage-svg-assets, homepage-project-status, homepage-keycloak, homepage-terminal

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
- **navigatie:** forge-design-system-reference-html
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
- **focusvolgorde:** 4
- **kernboodschap:** Voortgang en vervolgstappen komen uit dezelfde normatieve projectstatus.
- **leesvolgorde:** 5
- **navigatie:** project-status-html
- **navigatiegedrag:** volledige-kaart
- **rol:** route
- **variant:** forge-panel-route

## SVG assetcatalogus

**Soort:** homepagegebied

**Identifier:** `homepage-svg-assets-area`

### Doel

Bekijk de getypeerde vectorassets en hun reproduceerbare artifacts.

### Eigenschappen

- **component:** forge-panel
- **componentrol:** routekaart
- **focusvolgorde:** 3
- **kernboodschap:** Veilige padgeometrie, contractmetadata en SVG artifacts komen uit hetzelfde BAT model.
- **leesvolgorde:** 4
- **navigatie:** emberforge-svg-asset-catalog-html
- **navigatiegedrag:** volledige-kaart
- **rol:** route
- **variant:** forge-panel-route

## Keycloak login

**Soort:** homepagegebied

**Identifier:** `homepage-keycloak-area`

### Doel

Open de native EmberForge login productsurface.

### Eigenschappen

- **component:** forge-panel
- **componentrol:** routekaart
- **focusvolgorde:** 5
- **kernboodschap:** Email, wachtwoord en submitsemantiek zonder authenticatieclaim.
- **leesvolgorde:** 6
- **navigatie:** emberforge-keycloak-login-html
- **navigatiegedrag:** volledige-kaart
- **rol:** route
- **variant:** forge-panel-route

## Terminal

**Soort:** homepagegebied

**Identifier:** `homepage-terminal-area`

### Doel

Open de statische EmberForge terminal productsurface.

### Eigenschappen

- **component:** forge-panel
- **componentrol:** routekaart
- **focusvolgorde:** 6
- **kernboodschap:** Een bronbewezen systeemoverzicht zonder shelluitvoering of actuele telemetrie.
- **leesvolgorde:** 7
- **navigatie:** emberforge-terminal-html
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

## SVG assetcatalogus

**Soort:** componentinstantie

**Identifier:** `homepage-svg-assets`

### Doel

Bekijk de getypeerde vectorassets en hun reproduceerbare artifacts.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-svg-assets-area

## Projectstatus

**Soort:** componentinstantie

**Identifier:** `homepage-project-status`

### Doel

Volg de actuele voortgang, onderbouwing en eerstvolgende milestone.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-project-status-area

## Keycloak login

**Soort:** componentinstantie

**Identifier:** `homepage-keycloak`

### Doel

Open de native EmberForge login productsurface.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-keycloak-area

## Terminal

**Soort:** componentinstantie

**Identifier:** `homepage-terminal`

### Doel

Open de statische EmberForge terminal productsurface.

### Eigenschappen

- **compositie:** beckeringh-palace-homepage-composition
- **homepagegebied:** homepage-terminal-area

## Beckeringh Palace Homepage Grid

**Soort:** layout

**Identifier:** `beckeringh-palace-homepage-grid`

### Doel

Ordent de homepage entree en zes productroutes in een responsief grid.

### Eigenschappen

- **columns:** 6
- **compact-columns:** 1
- **regions:** homepage-intro-region, homepage-world-region, homepage-design-system-region, homepage-svg-assets-region, homepage-project-status-region, homepage-keycloak-region, homepage-terminal-region
- **responsive-breakpoint:** 960
- **rows:** 3
- **type:** grid

## Homepage entree

**Soort:** region

**Identifier:** `homepage-intro-region`

### Doel

Brede entree tot Beckeringh Palace.

### Eigenschappen

- **column:** 1
- **column-span:** 6
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
- **column-span:** 2
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

- **column:** 3
- **column-span:** 2
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

- **column:** 1
- **column-span:** 2
- **compact-order:** 5
- **instantie:** homepage-project-status
- **layout:** beckeringh-palace-homepage-grid
- **row:** 3
- **row-span:** 1

## SVG assetcatalogusroute

**Soort:** region

**Identifier:** `homepage-svg-assets-region`

### Doel

Route naar de native SVG assetcatalogus.

### Eigenschappen

- **column:** 5
- **column-span:** 2
- **compact-order:** 4
- **instantie:** homepage-svg-assets
- **layout:** beckeringh-palace-homepage-grid
- **row:** 2
- **row-span:** 1

## Keycloak route

**Soort:** region

**Identifier:** `homepage-keycloak-region`

### Doel

Route naar de native EmberForge login productsurface.

### Eigenschappen

- **column:** 3
- **column-span:** 2
- **compact-order:** 6
- **instantie:** homepage-keycloak
- **layout:** beckeringh-palace-homepage-grid
- **row:** 3
- **row-span:** 1

## Terminalroute

**Soort:** region

**Identifier:** `homepage-terminal-region`

### Doel

Route naar de statische EmberForge terminal productsurface.

### Eigenschappen

- **column:** 5
- **column-span:** 2
- **compact-order:** 7
- **instantie:** homepage-terminal
- **layout:** beckeringh-palace-homepage-grid
- **row:** 3
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

## EmberForge Vector Node SVG

**Soort:** product

**Identifier:** `emberforge-vector-node-svg`

### Doel

Genereert het native technische lijnornament als veilig SVG product.

### Eigenschappen

- **asset:** emberforge-vector-node
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-vector-node.svg
- **wereld:** beckeringh-palace

## EmberForge Lichtschijf SVG

**Soort:** product

**Identifier:** `emberforge-light-disc-svg`

### Doel

Genereert de neutrale native lichtschijf als veilig en herbruikbaar SVG product.

### Eigenschappen

- **asset:** emberforge-light-disc
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-light-disc.svg
- **wereld:** beckeringh-palace

## EmberForge Dashboard Icon SVG

**Soort:** product

**Identifier:** `emberforge-icon-dashboard-svg`

### Doel

Genereert het native dashboardicoon als veilig SVG product.

### Eigenschappen

- **asset:** emberforge-icon-dashboard
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-icon-dashboard.svg
- **wereld:** beckeringh-palace

## EmberForge Identity Icon SVG

**Soort:** product

**Identifier:** `emberforge-icon-identity-svg`

### Doel

Genereert het native identity icoon als veilig SVG product.

### Eigenschappen

- **asset:** emberforge-icon-identity
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-icon-identity.svg
- **wereld:** beckeringh-palace

## EmberForge Terminal Icon SVG

**Soort:** product

**Identifier:** `emberforge-icon-terminal-svg`

### Doel

Genereert het native terminalicoon als veilig SVG product.

### Eigenschappen

- **asset:** emberforge-icon-terminal
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-icon-terminal.svg
- **wereld:** beckeringh-palace

## EmberForge Assets Icon SVG

**Soort:** product

**Identifier:** `emberforge-icon-assets-svg`

### Doel

Genereert het native assetcatalogusicoon als veilig SVG product.

### Eigenschappen

- **asset:** emberforge-icon-assets
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-icon-assets.svg
- **wereld:** beckeringh-palace

## EmberForge merkteken SVG

**Soort:** product

**Identifier:** `emberforge-merkteken-svg`

### Doel

Genereert het native EmberForge merkteken als veilig SVG product.

### Eigenschappen

- **asset:** emberforge-merkteken
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-merkteken.svg
- **wereld:** beckeringh-palace

## EmberForge woordmerk SVG

**Soort:** product

**Identifier:** `emberforge-woordmerk-svg`

### Doel

Genereert het native EmberForge woordmerk als veilig SVG product.

### Eigenschappen

- **asset:** emberforge-woordmerk
- **backend:** svg
- **inhoud:** asset
- **mode:** static
- **pad:** output/products/emberforge-woordmerk.svg
- **wereld:** beckeringh-palace

## EmberForge Ultrawide Wallpaper Manifest

**Soort:** product

**Identifier:** `emberforge-ultrawide-wallpaper-manifest`

### Doel

Publiceert canvas, formaat, lagen en assetplaatsingen als machineleesbaar contractproduct.

### Eigenschappen

- **backend:** wallpaper-manifest
- **inhoud:** wallpaper
- **mode:** static
- **pad:** output/products/emberforge-ultrawide.wallpaper.json
- **wallpaper:** emberforge-ultrawide-wallpaper
- **wereld:** beckeringh-palace

## EmberForge Ultrawide Wallpaper PNG

**Soort:** product

**Identifier:** `emberforge-ultrawide-wallpaper-png`

### Doel

Rendert het opgeloste native wallpapercontract als deterministisch 3840 bij 1080 beeldartifact.

### Eigenschappen

- **backend:** wallpaper-png
- **inhoud:** wallpaper
- **mode:** static
- **pad:** output/products/emberforge-ultrawide.png
- **wallpaper:** emberforge-ultrawide-wallpaper
- **wereld:** beckeringh-palace

## EmberForge Desktop Wallpaper Manifest

**Soort:** product

**Identifier:** `emberforge-desktop-wallpaper-manifest`

### Doel

Publiceert het zelfstandige 1900 bij 1200 wallpapercontract als familievariant.

### Eigenschappen

- **backend:** wallpaper-manifest
- **inhoud:** wallpaper
- **mode:** static
- **pad:** output/products/emberforge-desktop.wallpaper.json
- **wallpaper:** emberforge-desktop-wallpaper
- **wereld:** beckeringh-palace

## EmberForge Desktop Wallpaper PNG

**Soort:** product

**Identifier:** `emberforge-desktop-wallpaper-png`

### Doel

Rendert de zelfstandige 1900 bij 1200 EmberForge familievariant.

### Eigenschappen

- **backend:** wallpaper-png
- **inhoud:** wallpaper
- **mode:** static
- **pad:** output/products/emberforge-desktop.png
- **wallpaper:** emberforge-desktop-wallpaper
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