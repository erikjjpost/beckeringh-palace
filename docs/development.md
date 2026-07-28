# Development

## Vereisten

- Git
- Python 3.12 of hoger

Er zijn voor de huidige vertical slice geen externe Python-packages nodig.

## Volledige controle

```bash
python tools/bp.py check
```

Dit commando voert achtereenvolgens uit:

1. modelvalidatie;
2. BAT compilatie;
3. product en documentatiegeneratie;
4. generatie van de projectstatus;
5. unit tests;
6. controle op gewijzigde én nieuwe bestanden.

Een succesvolle controle eindigt met:

```text
RESULTAAT: GELDIG EN REPRODUCEERBAAR
```

## Losse commando's

```bash
python tools/validate.py
PYTHONDONTWRITEBYTECODE=1 python tools/compile_bat.py
python tools/generate.py
python tools/render_status.py
python -m unittest discover -s tests -v
```

Gebruik losse commando's alleen voor ontwikkeling. Voor commits en pull requests is `python tools/bp.py check` de norm.

## Continuous integration

`.github/workflows/validate.yml` voert bij iedere pull request dezelfde
kwaliteitsketen uit als lokaal. De workflow:

1. vereist een wijziging in `project/status.json`;
2. valideert het bronmodel;
3. compileert BAT;
4. genereert producten, documentatie en projectstatus;
5. draait de gerichte productslicetest en de volledige regressiesuite;
6. weigert de wijziging wanneer generatie de werkboom wijzigt of nieuwe
   bestanden achterlaat.

De workflow draait met Python 3.12 en `PYTHONDONTWRITEBYTECODE=1`, zodat
Python-cachebestanden de reproduceerbaarheidscontrole niet vervuilen.
