# Development

## Vereisten

- Git
- Python 3.12 of hoger

Er zijn voor de huidige vertical slice geen externe Python-packages nodig.
Ook de native PNG-rasterisatie en codering gebruiken uitsluitend de
standaardbibliotheek.

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

Met `python tools/bp.py check --pre-commit` draait dezelfde keten zonder de
controle op gewijzigde of nieuwe bestanden. Gebruik dat vóór een definitieve
commit, wanneer BAT-broncode bewust nog ongecommit staat; de standaardaanroep
zonder vlag blijft na de commit op een schone werkboom vereist.

## Losse commando's

```bash
python tools/validate.py
PYTHONDONTWRITEBYTECODE=1 python tools/compile_bat.py
python tools/render_status.py
python -m unittest discover -s tests -v
```

Gebruik losse commando's alleen voor ontwikkeling. Voor commits en pull requests is `python tools/bp.py check` de norm.

## Continuous integration

`.github/workflows/validate.yml` roept bij iedere push naar `main` en iedere
pull request letterlijk `python tools/bp.py check` aan, dezelfde gate als
lokaal. Er bestaat geen aparte CI-implementatie van de keten. De workflow:

1. vereist bij een pull request een wijziging in `project/status.json`;
2. draait `python tools/bp.py check`, dat modelvalidatie, BAT-compilatie,
   product- en documentatiegeneratie, projectstatusgeneratie, de volledige
   testsuite en de reproduceerbaarheidscontrole in die volgorde uitvoert.

`tools/bp.py` zet zelf `PYTHONDONTWRITEBYTECODE=1` voor iedere stap, zodat
Python-cachebestanden de reproduceerbaarheidscontrole niet vervuilen.
