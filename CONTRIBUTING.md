# Contributing

## Kernregels

- Werk altijd via een branch en pull request.
- `main` moet valide en genereerbaar blijven.
- Agents leveren voorstellen en wijzigen het architectuurmodel niet zonder goedkeuring.
- Architectuur- en organisatielagen blijven onafhankelijk van modelprovider en modelnaam.

## Lokale controle

```bash
python tools/validate.py
python tools/generate.py
```
