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
2. outputgeneratie;
3. unit tests;
4. controle op gewijzigde én nieuwe bestanden.

Een succesvolle controle eindigt met:

```text
RESULTAAT: GELDIG EN REPRODUCEERBAAR
```

## Losse commando's

```bash
python tools/validate.py
python tools/generate.py
python -m unittest discover -s tests -v
```

Gebruik losse commando's alleen voor ontwikkeling. Voor commits en pull requests is `python tools/bp.py check` de norm.
