# ADR-0002: Backends falen expliciet bij niet-realiseerbare beeldintentie

- ID: `ADR-0002`
- Titel: Backends falen expliciet bij niet-realiseerbare beeldintentie
- Status: geaccepteerd
- Datum: 2026-08-15
- Beslissingsdocument: dit document

## Context

De PNG-wallpaperrenderer (`compiler/wallpaper_png_renderer.py`) kan
uitsluitend vlakke kleur tekenen, optioneel met een radiale falloff-gloed op
een gevuld asset. Geen gradients, blur, textuur of antialiasing.

Zolang een backend een niet-ondersteunde beeldintentie zonder foutmelding
zou vereenvoudigen tot wat hij wél kan, bepaalt de renderer stilzwijgend
welke art direction BAT überhaupt kan uitdrukken. De afhankelijkheidsrichting
keert dan om: het implementatiedetail (de renderer) dicteert het
domeinvocabulaire (BAT), in plaats van andersom.

Gevonden door forge-architect bij validatie van de agent-werkwijze
(2026-08-15).

## Besluit

Een backend die een gedeclareerde BAT-beeldintentie niet volledig kan
realiseren, weigert expliciet met een diagnose. Stille vereenvoudiging is
nooit toegestaan, ook niet wanneer het resultaat er "goed genoeg" uitziet.

Concreet voor de wallpaperrenderer: het `effect`-veld op een assetplaatsing
wordt al bij BAT-validatie begrensd tot `WALLPAPER_EFFECTS` (`solid`,
`radial-glow`, met de bijbehorende `BP4387`/`BP4388`-diagnostiek in
`compiler/wallpaper_products.py`). De renderer zelf herhaalt die
exhaustiviteit onafhankelijk: ieder `effect` dat de renderer bereikt en niet
expliciet is afgehandeld, leidt tot een `ValueError`, nooit tot een impliciete
val-through naar vlak gedrag. Dat maakt de renderer zelf verdedigd tegen
toekomstige drift tussen `WALLPAPER_EFFECTS` en de daadwerkelijke
renderimplementatie, ook al is die drift vandaag door de BAT-validatie al
uitgesloten.

Uitbreiding van de renderercapaciteit zelf (gradients, textuur,
antialiasing) is een aparte milestone onder "Compiler en reproduceerbaarheid",
niet onder "Visuele wereld en art direction". De art direction blijft
BAT-intentie; de rendercapaciteit is compilerinfrastructuur die dat intentie
al dan niet kan realiseren.

## Gevolgen

- Renderergrenzen blijven expliciet zichtbaar in `project/status.json`, onder
  het `remaining`-veld van "Compiler en reproduceerbaarheid".
- Een toekomstige, rijkere beeldintentie in BAT die de huidige renderer niet
  kan tekenen, faalt de build in plaats van een verarmde wallpaper te
  produceren.
- Iedere nieuwe backend-implementatie (huidig of toekomstig) volgt hetzelfde
  patroon: exhaustieve afhandeling van elk mogelijk BAT-intentieveld, met een
  expliciete fout voor de rest.
