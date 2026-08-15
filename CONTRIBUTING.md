# Contributing to Beckeringh Palace

## Hoofdregel

`main` moet altijd valide en reproduceerbaar zijn. Wijzigingen worden via een branch en pull request aangeboden. Nooit rechtstreeks op `main` committen.

Dit is ook technisch afgedwongen: branch protection op `main` vereist een pull request en een groene `validate`-check, inclusief voor repo-admins. Directe pushes en force-pushes naar `main` worden door GitHub geweigerd.

Voor coding agents is `AGENTS.md` het bindende werkcontract: branchconventies (`agent/<milestone-id>-<slug>`, `fix/<slug>`), publicatieroute, conflictregels en verplichte `project/status.json`-evidence staan daar volledig uitgewerkt.

## Werkwijze

1. Maak een branch vanaf `main` volgens de conventie in `AGENTS.md`.
2. Wijzig de normatieve BAT-bron (`architectuur/*.bp`) of de juiste compilerlaag onder `compiler/`. Afgeleide bestanden onder `output/` worden nooit handmatig ontworpen.
3. Werk bij iedere wijziging `project/status.json` waarheidsgetrouw bij.
4. Voer de volledige controle uit:

```bash
python tools/bp.py check --pre-commit
```

5. Commit uitsluitend samenhangende wijzigingen.
6. Draai `python tools/bp.py check` (zonder vlag) op de schone werkboom om reproduceerbaarheid te bevestigen.
7. Open een pull request en merge pas na groene CI en, waar van toepassing, expliciete goedkeuring.

## Bron en output

- `architectuur/*.bp` (BAT) is de enige normatieve bron voor producten.
- `project/status.json` bevat de normatieve projectvoortgang.
- `output/` bevat reproduceerbare, gegenereerde representaties.
- `PROJECT_STATUS.md` is de gegenereerde, leesbare projectstatus.
- Handmatige wijzigingen in `output/` zijn niet toegestaan; pas de bron of de renderer aan.
- Handmatige wijzigingen in `PROJECT_STATUS.md` zijn niet toegestaan.
- CI weigert pull requests die `project/status.json` niet actualiseren.

## Architectuurregels

- BAT blijft de enige normatieve bron; renderers lezen geen handmatig onderhouden productbestanden (zie `docs/world-model.md`, ontwerpregel 3).
- Kernobjecten blijven onafhankelijk van specifieke AI-providers.
- Dubbele informatie wordt vermeden; afgeleide informatie wordt gegenereerd.
- Conflicten in `output/` worden nooit handmatig opgelost: rebase en regenereer (zie `AGENTS.md`).
