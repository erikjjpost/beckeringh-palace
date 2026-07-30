# Architectuur

Beckeringh Palace is een product- en ontwerpcompiler: een normatief World Model wordt gevalideerd en omgezet in reproduceerbare representaties.

```text
World Model + Organisatie + Voorstellen
                  ↓
              Compiler
                  ↓
        Semantisch World Model
                  ↓
              Renderers
                  ↓
Markdown / Mermaid / SVG / PNG / HTML / Grafana / Figma
```

De productcompiler groeit langs de volgende normatieve keten:

```text
BAT
 ↓
World
 ↓
Theme
 ↓
ResolvedTheme
 ↓
Appearance
 ↓
Components
 ↓
Accessibility
 ↓
Variants
 ↓
Composition
 ↓
Products
 ↓
Renderers
```

Native layouts zijn onderdeel van het productmodel. Zij beschrijven uitsluitend
intentie. Zie [product-model.md](product-model.md) voor het contract van
`compositie`, `componentinstantie`, `layout`, `region`, `grid`, `stack`, `flow`
en `layer`.

De productcompiler lost een native compositie en layout vóór backendselectie
op. Backends ontvangen daardoor `ResolvedComposition` en `ResolvedLayout` via
de productcontext en vertalen deze naar hun eigen mechanisme. HTML vertaalt
native layouts naar browserpresentatie. De Grafana-backend vertaalt native
grid-layouts naar het klassieke, importeerbare dashboard JSON model met een
24-koloms `gridPos`. Het opgeloste native thema bepaalt de donkere of lichte
dashboardstijl. Component-, variant- en appearance-identiteit blijven in
paneelbeschrijvingen traceerbaar. Het domeinmodel bevat geen HTML-, CSS- of
Grafana-eigenschappen.

Productbackends kunnen tekst of bytes opleveren. De productcompiler behandelt
beide als dezelfde afgeleide artifactpayload. Tekstproducten worden met UTF-8
geschreven. Binaire producten worden bytegelijk geschreven. De native
wallpaperbackend gebruikt die grens om een PNG te produceren zonder een
bestandsconversie of handmatig onderhouden tussenartifact.

Voor wallpapers lost de productcompiler canvas, materiaalrollen, laagvolgorde,
plaatsingsgeometrie, fit, dekking en SVG assets vooraf op. De PNG backend
interpreteert alleen deze context. Zij bevat geen eigen assetgeometrie,
plaatsingstabel of kleurkeuze. De rasterisatie en PNG codering gebruiken
uitsluitend de Python standaardbibliotheek. De encoder schrijft een
geïndexeerde PNG waar mogelijk en legt geen tijdstempel vast.

HTML en Grafana tonen daarnaast dezelfde opgeloste dashboardidentiteit:
compositie, wereld, thema en BAT-generatiestatus. HTML rendert deze als een
responsieve productshell. Grafana rendert deze als een vaste Canvas-header
boven de native gridplaatsingen.

De normatieve projectstatus wordt als getypeerde `ProjectStatus` één keer
gevalideerd en door de productcompiler aan de gedeelde productcontext
toegevoegd. Backends krijgen daardoor dezelfde voortgang, milestones,
onderbouwing en resterend werk zonder zelf `project/status.json` te lezen of
eigen statuslogica toe te voegen. De totale voortgang is geen los opgeslagen
veld: de statuslaag berekent haar deterministisch uit de expliciete percentages
en gewichten van de productgebieden. Productcompilatie zonder aangeleverde status
blijft expliciet contextloos voor bestaande en externe compilatiepaden.

Native composities beschrijven de inhoud van een product onafhankelijk van de
layout. Zij ordenen benoemde componentinstanties en bevatten geen richting of
backendpresentatie. Daardoor blijven hergebruik van een component, identiteit
van een specifiek gebruik en plaatsing drie afzonderlijke verantwoordelijkheden.
Een product koppelt één compositie aan één layout. Iedere region plaatst
expliciet één instantie uit die compositie. De compositie bepaalt de
inhoudsvolgorde, instantie-identiteit, componentkeuze en zichtbare
instantienaam. De layout bepaalt uitsluitend de plaatsing en bewaart daarom
geen opgeloste componentidentiteit.

Native varianten beschrijven één expliciete appearance-afwijking voor exact één
component. Een interactieve variant kan daarnaast een volledige geordende
mapping voor rust, hover, focus, pressed en disabled dragen. Een
componentinstantie kiest zo'n variant alleen met een benoemde referentie. De
gekozen variant, effectieve rustappearance en stateappearances worden vóór
backendselectie opgelost en bevatten geen backendpresentatie.

Native toegankelijkheidscontracten beschrijven per component de semantische
rol, naambron, optionele waarde- en foutbron, disabled gedrag, focusdeelname en
toetsenbordgedrag. Zij bevatten geen HTML- of ARIA-velden. Dezelfde opgeloste
semantiek gaat naar componentvoorbeelden en productcomposities voordat een
backend haar naar native hostelementen of machineleesbare metadata vertaalt.

Een designsystem referentieproduct ordent vijf expliciete
`referentiesectie` objecten. De productcompiler lost primitives, tokens,
appearances, componenten, varianten, voorbeelden en toegankelijkheid één keer
backendonafhankelijk op. De HTML backend vertaalt deze resolved referentie naar
lokale sectienavigatie, feitelijke waarden, state previews en contracttabellen.
De sectievolgorde en zichtbare sectienamen komen uit BAT.

Native renderdoelen beschrijven één benoemde representatie met een expliciet
formaat en veilig relatief artifactpad. Het resolved contract blijft
backendonafhankelijk en kiest geen renderer impliciet op basis van een
bestandsformaat. De compiler koppelt ieder renderdoel via zijn expliciete id
aan één renderer en schrijft de uitkomst naar het gedeclareerde artifactpad.

BAT is geen algemene enterprise-architectuurtaal. ArchiMate en andere externe modellen worden uitsluitend via expliciete adapters gekoppeld. De domeingrens staat in [world-model.md](world-model.md).

## Ontwerpprincipes

### Elke representatie is afgeleid van het model

> Elke representatie is afgeleid van het model. Er bestaat geen handmatig onderhouden productdocumentatie.

Dit betekent concreet:

- overzichten worden niet handmatig in README-bestanden bijgehouden;
- Mermaid-diagrammen worden gegenereerd en niet rechtstreeks gewijzigd;
- SVG-, HTML-, Grafana- en Figma-representaties worden door renderers opgebouwd;
- gegenereerde artefacten zijn nooit de bron van waarheid;
- wijzigingen beginnen in BAT, het normatieve model of de compiler.

Mensen en AI wijzigen dus uitsluitend normatieve bronnen en compilercomponenten. Alle overige representaties worden opnieuw gecompileerd.

### De taal blijft domeinspecifiek

Een native BAT-concept moet nodig zijn om Beckeringh Palace-producten te specificeren of te renderen. Algemene enterprise-architectuurconcepten worden niet aan de kern toegevoegd. Hierdoor blijft BAT kleiner dan een architectuurmodelleertaal en gericht op reproduceerbare producten.

## Lagen

### Normatieve bron

- `architectuur/`: BAT-bronnen (`.bp`) tijdens de migratie naar het World Model.
- `model/`: bestaande capabilities, services, assets, relaties en representaties tijdens de migratie.
- `organisation/`: rollen, contracten en workflows.
- `proposals/`: gecontroleerde wijzigingen.

### Compiler tooling

- `compiler/`: parser, canonieke tussenrepresentatie, World Model, semantische analyse en renderers.
- `compiler/world_model.py`: normatieve catalogus en domeingrens van objectsoorten.
- `tools/validate.py`: controleert modelintegriteit en regels.
- `tools/compile_bat.py`: compileert BAT naar CIR en afgeleide output.
- `tools/generate.py`: genereert bestaande afgeleide representaties.
- `tools/bp.py`: voert de volledige kwaliteitsketen uit.

### Afgeleide output

- `output/bat/`: vanuit BAT gegenereerde CIR- en documentatie-output.
- `output/docs/`: gegenereerde documentatie.
- `output/diagrams/`: gegenereerde diagrambron.
- `output/products/`: de echte productartefacten:
  - `index.html`: de Beckeringh Palace homepage;
  - `forge-dashboard.html`, `emberforge-homelab-dashboard.html`,
    `emberforge-keycloak-login.html`, `emberforge-terminal.html` en
    `project-status.html`: HTML-producten;
  - `forge-dashboard.grafana.json`, `emberforge-homelab-dashboard.grafana.json`
    en `project-status.grafana.json`: importeerbare Grafana-dashboards;
  - `components.html`: statisch EmberForge designsystem referentieproduct;
  - `components.css`: afgeleide componentstijlen;
  - `tokens.json` en `tokens.css`: opgeloste ontwerptokens;
  - `emberforge-ultrawide.wallpaper.json`: opgelost wallpapercontract;
  - `emberforge-ultrawide.png`: native 3840 bij 1080 wallpaperbeeld.

Output wordt gecommit om deterministische regeneratie te kunnen controleren. Zij blijft afgeleid; rechtstreekse wijzigingen worden bij de volgende compilatie overschreven en gelden niet als modelwijziging.

Zie [product-runbook.md](product-runbook.md) voor bekijken, importeren,
snapshotverificatie en rollback.
