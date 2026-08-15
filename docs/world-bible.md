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

De toren met het observatorium, uitkijkend over de bergen. Meet, signaleert,
waarschuwt. Nog geen eigen BAT-product; Grafana-dashboards
(`emberforge-homelab-dashboard`) dekken een deel van deze functie zonder dat
de kamer zelf al benoemd is.

### The Archive — Documentation, Git & Knowledge

Bewaart kennis en herkomst. Dit is waar **Second Brain** en
**Information Management** (zie `docs/world-model.md`) narratief thuishoren:
ideeën, besluiten en documentatie vastleggen, verbinden, terugvinden. Git
(deze repository, `erikjjpost/beckeringh-palace`) is de feitelijke Archive.

### The Gatehouse — Security, Access & Network Control

De poort naar het paleis, aan het water. Toegang, identiteit, netwerkregie.
Nog geen eigen BAT-product; Keycloak-login (`emberforge-keycloak-login-html`)
is de dichtstbijzijnde bestaande productsurface.

### The Harbor — External Connections & Integrations

De haven met watermolen, waar het paleis de buitenwereld raakt. Externe
koppelingen. Nog geen BAT-product.

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
zelf; hier, in de smederij, is Library de plek waar AI-diensten draaien. Twee
verschillende dingen die toevallig dezelfde naam dragen; bij verdere
uitwerking moet dat ontdubbeld worden.

### The Workshop — Development, CI/CD & Automation

Waar gebouwd en geautomatiseerd wordt. Correspondeert met de agentwerkwijze
uit `AGENTS.md`: branches, pull requests, de `validate`-CI-check.

### The Vault — Secrets, Identity & Certificate Authority

Geheimen, identiteit, certificaten. Strikt gescheiden van de rest, zoals ook
`AGENTS.md` en de bredere Erik-regels (geen credentials in code of commits)
al afdwingen — dat gedrag bestaat dus al, alleen nog niet onder deze naam.

### The Forge Hall — Kubernetes Cluster & Orchestration

De smidshal zelf: orkestratie. Naamgenoot van het beverembleem
(`emberforge-beaver`, smidshamer en aambeeld) en van `thema forge` in BAT.
Correspondeert met het K3s-cluster.

### The Machine Hall — Proxmox, VMs & Bare Metal

Fysieke en gevirtualiseerde machines.

### The Waterworks — Storage, Backups & Data Reservoirs

Opslag en back-ups, gevoed door dezelfde waterval-beeldtaal als de haven
boven de grond.

### Circle of Fifths — Harmony in Systems. Balance in Design.

Het middelpunt van de ondergrondse smederij, letterlijk en figuurlijk. Dit is
al een volledig native BAT-object: `muziekcirkel emberforge-circle-of-fifths`,
gerenderd in beide wallpaperformaten. De enige kamer in deze kaart die al
volledig als reproduceerbaar BAT-product bestaat.

## Wat al BAT is, wat nog narratief is

| Kamer | BAT-status |
|---|---|
| Great Hall | bestaand product (Forge Dashboard) |
| Circle of Fifths | bestaand native object (`muziekcirkel`) |
| Entrance to EmberForge / EmberForge zelf | bestaand native merk (`emberforge`) |
| Archive | narratief (Second Brain-tekst in `world-model.md`), geen eigen product |
| Gatehouse | gedeeltelijk (Keycloak-login-product), geen eigen kamer-object |
| Observatory, Harbor, Library, Workshop, Vault, Forge Hall, Machine Hall, Waterworks | uitsluitend narratief, geen BAT-product of -object |

## Wat dit document niet doet

Dit is beschrijvend narratief, geen native BAT-objectsoort. Geen van de
kamers hierboven wordt hiermee automatisch een `wereld`, `product` of ander
native object — dat vereist een aparte, expliciete beslissing per kamer
(ontwerpregel 1 in `docs/world-model.md`: een native objectsoort moet
aantoonbaar nodig zijn voor minstens één productrenderer). Dit document geeft
wel de kaart waarmee die vervolgbeslissingen kunnen worden genomen.
