# World Bible

Beckeringh Palace is een soeverein thuisdatacenter, verbeeld als kasteel boven
de grond en smederij eronder. Dit document legt de kamers van die wereld vast:
wat iedere kamer betekent, welke functie ze draagt, en welk deel daarvan al
een echt BAT-product is versus nog puur narratief.

Bron: Erik's eigen wereldkaart (2026-08-15), een illustratie die de bedoelde
"centrale vastlegging" toont waaruit opmaak en betekenis voor het hele systeem
zouden moeten volgen. Dit document is de eerste stap om die kaart in BAT-taal
te vertalen: benoemen wat er is, voordat er nieuwe native objectsoorten voor
worden ontworpen.

## Tagline

**Beckeringh Palace — A Sovereign Home Datacenter**

> Where technology is forged with purpose, protected by design, and built to
> endure.

## Boven de grond: het Paleis

Het zichtbare kasteel is de bestuurs- en toegangslaag: waar je het systeem
overziet, bewaakt en van buitenaf bereikt.

### The Great Hall — Dashboards, Overview & Command Center

Het hart van het bovengrondse paleis, hoogste torenspits. Overzicht en
besturing. Correspondeert met het bestaande **Forge Dashboard**
(`forge-dashboard-html`, `forge-dashboard-grafana`): wereld- en
identiteitsoverzicht, ontwerpsysteem, productfamilie.

### The Observatory — Monitoring, Metrics & Alerting

De toren met het observatorium, uitkijkend over de bergen. Waar de Great Hall
overzicht en besturing biedt (wat is de toestand nu, en wat kun je erop
doen), kijkt de Observatory continu en meldt wanneer iets afwijkt: meten,
signaleren, waarschuwen, zonder zelf te besturen. Dit is nu een expliciet
benoemd product: `compositie emberforge-observatory` (voorheen
`emberforge-homelab-dashboard`), gerenderd naar `emberforge-observatory-html`
en `emberforge-observatory-grafana` — vier statistiekkaarten, vier statussen,
twee app-tegels. Zelfde correspondentieniveau als de Great Hall met Forge
Dashboard: geen nieuwe native objectsoort, want er is geen berekening die het
generieke `compositie`/`component`/`layout`/`product`-pad niet al uitdrukt
(ontwerpregel 1 vraagt daar niet om). Kleuren en typografie komen automatisch
mee via dezelfde generieke component→appearance→thema-keten die ook Great
Hall en de rest van het designsysteem draagt — geen aparte styling nodig.
Het waarschuwingsdeel (alerting, escalatie) blijft wel volledig narratief;
daar bestaat nog geen enkele representatie.

### The Harbor — External Connections & Integrations

De haven met watermolen, waar het paleis de buitenwereld raakt. Water dat
binnenkomt en weer vertrekt is de beeldtaal voor data die het systeem in en
uit stroomt: koppelingen met diensten buiten Beckeringh Palace zelf. Nog
geen BAT-product. Er is nu al iets dat functioneel op een Harbor lijkt — de
Figma-syncplugin praat met een externe wereld (Figma Desktop) — maar dat
werk hoort vandaag bij `compiler`/`figma`, niet bij een eigen kamer; als er
meer van dat soort externe koppelingen bijkomen, is dedupliceren met de
Harbor een latere, expliciete beslissing, geen automatisme.

### The Archive — Documentation, Git & Knowledge

Bewaart kennis en herkomst. Dit is waar **Second Brain** en
**Information Management** (zie `docs/world-model.md`) narratief thuishoren:
ideeën, besluiten en documentatie vastleggen, verbinden, terugvinden. Git
(deze repository, `erikjjpost/beckeringh-palace`) is de feitelijke Archive.

### The Gatehouse — Security, Access & Network Control

De poort naar het paleis, aan het water. Toegang, identiteit, netwerkregie.
Nog geen eigen BAT-product; Keycloak-login (`emberforge-keycloak-login-html`)
is de dichtstbijzijnde bestaande productsurface.

### Entrance to EmberForge

De poort tussen boven en onder: "het hart van onze infrastructuur." De
letterlijke overgang van het zichtbare paleis naar de ondergrondse smederij.

## Onder de grond: EmberForge

**EmberForge — Compute. Orchestrate. Empower.**

De smederij is de operationele en compute-laag: waar werk daadwerkelijk
gebeurt. Dit is ook het bestaande native merk `emberforge` in BAT — de
identiteit die nu al de wallpapers, het designsysteem en de SVG-assetfamilies
draagt.

### The Library — AI Services, LLMs & RAG Systems

AI-diensten en kennissystemen. Narratief het tegenhangerdeel van de
bestaande, aan Second Brain gekoppelde **The Library**-representatie in
`docs/world-model.md` — daar is Library de representatie van Second Brain
zelf (het bewaarde weten); hier, in de smederij, is Library de plek waar dat
weten wordt *uitgevoerd*: modellen die draaien, embeddings die worden
opgevraagd, retrieval dat plaatsvindt. Kort gezegd: de Archive/Second Brain
boven de grond bewaart wat er geweten wordt, de Library onder de grond is
waar het werkend wordt gemaakt. Twee verschillende rollen die toevallig
dezelfde naam dragen; bij verdere uitwerking moet dat ontdubbeld worden,
bijvoorbeeld door de ondergrondse rol een eigen naam te geven.

### The Workshop — Development, CI/CD & Automation

Waar gebouwd en geautomatiseerd wordt. Correspondeert met de agentwerkwijze
uit `AGENTS.md`: een `agent/<milestone-id>-<slug>`- of `fix/<slug>`-branch,
een pull request, de verplichte groene `validate`-check op `main` (branch
protection, ook voor admins), en `bp.py check` als de ene keten die validatie,
compilatie, statusrender en de volledige testsuite bundelt. De Workshop is
dus geen metafoor voor iets dat nog moet komen — het is de kamer waarin dit
project zelf, letterlijk vandaag, werkt.

### The Vault — Secrets, Identity & Certificate Authority

Geheimen, identiteit, certificaten. Strikt gescheiden van de rest, zoals ook
`AGENTS.md` en de bredere Erik-regels (geen credentials in code of commits)
al afdwingen — dat gedrag bestaat dus al, alleen nog niet onder deze naam.
De grens met de Gatehouse is functioneel: de Gatehouse regelt wie van
*buiten* het paleis binnenkomt (toegang, netwerkregie); de Vault bewaart wat
er *binnen* geheim moet blijven (secrets, identiteitsmateriaal, certificaten)
zodra het systeem eenmaal is binnengelaten. Een certificate authority is nog
narratief; er is geen BAT-product dat er vandaag invulling aan geeft.

### The Forge Hall — Kubernetes Cluster & Orchestration

De smidshal zelf: orkestratie. Naamgenoot van het beverembleem
(`emberforge-beaver`, smidshamer en aambeeld) en van `thema forge` in BAT.
Correspondeert met het K3s-cluster: waar workloads daadwerkelijk draaien en
worden ingepland. Speelt onder de grond dezelfde rol als de Great Hall boven
de grond — het besturende middelpunt — maar dan operationeel: niet overzicht
tonen, maar het werk laten gebeuren.

### The Machine Hall — Proxmox, VMs & Bare Metal

Fysieke en gevirtualiseerde machines. Eén laag dieper dan de Forge Hall: waar
het K3s-cluster orkestreert, is de Machine Hall het fundament waar die
clusterknopen zelf op draaien — de hypervisor en het fysieke metaal eronder.
Orkestratie (Forge Hall) en het substraat waarop wordt georkestreerd (Machine
Hall) zijn zo twee te onderscheiden kamers, ook al liggen ze in de praktijk
op elkaar gestapeld.

### The Waterworks — Storage, Backups & Data Reservoirs

Opslag en back-ups, gevoed door dezelfde waterval-beeldtaal als de haven
boven de grond: wat door de Harbor naar binnen stroomt, komt uiteindelijk
hier tot rust. De Waterworks is de enige plek in de smederij waar
toestand *blijvend* mag bestaan — en dat is precies het spiegelbeeld van hoe
dit project zelf al werkt: alles in `output/` wordt gegenereerd, nooit
handmatig bewerkt, en conflicten daarin worden nooit opgelost maar altijd
herbouwd (`AGENTS.md`). De Waterworks is narratief waar die ene uitzondering
zou wonen: het reservoir dat *niet* zomaar herbouwbaar is en dus expliciete
back-up- en retentiezorg verdient.

### Circle of Fifths — Harmony in Systems. Balance in Design.

Het middelpunt van de ondergrondse smederij, letterlijk en figuurlijk. Dit is
al een volledig native BAT-object: `muziekcirkel emberforge-circle-of-fifths`,
gerenderd in beide wallpaperformaten. De enige kamer in deze kaart die al
volledig als reproduceerbaar BAT-product bestaat.

## Wat al BAT is, wat nog narratief is

| Kamer | BAT-status |
|---|---|
| Great Hall | bestaand product (Forge Dashboard) |
| Observatory | bestaand, expliciet benoemd product (`emberforge-observatory`), zelfde correspondentieniveau als Great Hall |
| Circle of Fifths | bestaand native object (`muziekcirkel`) |
| Entrance to EmberForge / EmberForge zelf | bestaand native merk (`emberforge`) |
| Archive | narratief (Second Brain-tekst in `world-model.md`), geen eigen product |
| Gatehouse | gedeeltelijk (Keycloak-login-product), geen eigen kamer-object |
| Harbor, Library, Workshop, Vault, Forge Hall, Machine Hall, Waterworks | narratief uitgewerkt (2026-08-21), nog geen BAT-product of -object |

## Wat dit document niet doet

Dit is beschrijvend narratief, geen native BAT-objectsoort. Geen van de
kamers hierboven wordt hiermee automatisch een `wereld`, `product` of ander
native object — dat vereist een aparte, expliciete beslissing per kamer
(ontwerpregel 1 in `docs/world-model.md`: een native objectsoort moet
aantoonbaar nodig zijn voor minstens één productrenderer). Dit document geeft
wel de kaart waarmee die vervolgbeslissingen kunnen worden genomen.
