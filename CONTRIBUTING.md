# Contributing to Beckeringh Palace

## Hoofdregel

`main` moet altijd valide en reproduceerbaar zijn. Wijzigingen worden via een branch en pull request aangeboden.

## Werkwijze

1. Maak een branch vanaf `main`.
2. Wijzig eerst het normatieve model.
3. Genereer afgeleide output opnieuw.
4. Voer de volledige controle uit:

```bash
python tools/bp.py check
```

5. Commit uitsluitend samenhangende wijzigingen.
6. Open een pull request en merge pas na groene CI.

## Bron en output

- `model/`, `organisation/` en `proposals/` bevatten normatieve bronobjecten.
- `output/` bevat reproduceerbare, gegenereerde representaties.
- Handmatige wijzigingen in `output/` zijn niet toegestaan; pas de bron of generator aan.

## Architectuurregels

- Agents wijzigen het normatieve model niet rechtstreeks.
- Goedgekeurde voorstellen gaan vooraf aan modelwijzigingen.
- Kernobjecten blijven onafhankelijk van specifieke AI-providers.
- Dubbele informatie wordt vermeden; afgeleide informatie wordt gegenereerd.
