# Idee — Lokale 1-bit taalmodellen met BitNet

Bron: <https://github.com/microsoft/BitNet> (verkend op 2026-10-11).

## Wat het is

bitnet.cpp is het officiële inference-framework van Microsoft voor 1-bit
taalmodellen, waarin elk gewicht −1, 0 of +1 is (BitNet b1.58). Licentie: MIT.

- Modellen: BitNet b1.58 2B-4T als officieel taalmodel, BitNet-embedding 0.6B
  en 270M sinds juli 2026, plus communitymodellen zoals Falcon3, Falcon-E en
  Llama3-8B-1.58.
- Hardware: x86- en ARM-CPU's en een GPU-kernel. NPU staat gepland.
- Claims van Microsoft: op CPU 1,4 tot 6,2 keer sneller en 55 tot 82% minder
  energie dan F16-inference.
- Bouwketen: Python 3.10+, CMake 3.22+ en clang 18+, gebouwd via
  `setup_env.py`.

## Grens met de normatieve keten

BAT blijft de enige normatieve bron. Een taalmodel mag daarom nooit onderdeel
worden van `tools/bp.py check` of inhoud onder `output/` produceren:

1. modeluitvoer is niet bit-voor-bit reproduceerbaar over model, kernel en
   hardware heen;
2. een C++-build met modelbestanden van gigabytes verzwaart CI en maakt de
   netwerkloze keten afhankelijk van externe downloads;
3. het is geen milestone op de roadmap.

Dezelfde redenering sluit Figma MCP uit als productiedependency.

## Mogelijke rol buiten de keten

- **Voorstellen voor Architectuur Synchronisatie.** Een lokaal model kan
  notities uit de Second Brain lezen en een architectuurvoorstel in BAT
  voorbereiden (zie `architectuur-synchronisatie.md`). Het voorstel doorloopt
  daarna de gewone validatie, architectuurreview en menselijke goedkeuring.
  Er gaan geen gegevens naar een externe dienst.
- **Zoeken op betekenis in de documentatie.** De embeddingmodellen kunnen een
  lokale index bouwen over `docs/` en de World Bible, als werkhulpmiddel en
  niet als product.
- **Schrijfhulp.** Concepten voor wereldteksten, waarbij een mens kiest en het
  resultaat in BAT vastlegt.

## Open vragen

- Is de kwaliteit van een 2B-model genoeg om geldige BAT-syntaxis voor te
  stellen, of is een groter communitymodel nodig?
- Leggen we de grens "taalmodellen alleen buiten de normatieve keten" vast in
  een ADR voordat er een milestone voor Architectuur Synchronisatie komt?
- Waar komen de modelbestanden te staan, buiten de repository en buiten CI?
