# Contributing to Beckeringh Palace

## Hoofdregel

`main` moet altijd valide en reproduceerbaar zijn. Wijzigingen worden via een branch en pull request aangeboden.

## Werkwijze

1. Maak een branch vanaf `main`.
2. Wijzig eerst het normatieve model.
3. Werk bij iedere milestone `project/status.json` bij.
4. Genereer afgeleide output opnieuw.
5. Voer de volledige controle uit:

```bash
python tools/bp.py check
```

6. Commit uitsluitend samenhangende wijzigingen.
7. Open een pull request en merge pas na groene CI.

## Bron en output

- `model/`, `organisation/` en `proposals/` bevatten normatieve bronobjecten.
- `project/status.json` bevat de normatieve projectvoortgang.
- `output/` bevat reproduceerbare, gegenereerde representaties.
- `PROJECT_STATUS.md` is de gegenereerde, leesbare projectstatus.
- Handmatige wijzigingen in `output/` zijn niet toegestaan; pas de bron of generator aan.
- Handmatige wijzigingen in `PROJECT_STATUS.md` zijn niet toegestaan.
- CI weigert pull requests die `project/status.json` niet actualiseren.

## Architectuurregels

- Agents wijzigen het normatieve model niet rechtstreeks.
- Goedgekeurde voorstellen gaan vooraf aan modelwijzigingen.
- Kernobjecten blijven onafhankelijk van specifieke AI-providers.
- Dubbele informatie wordt vermeden; afgeleide informatie wordt gegenereerd.
