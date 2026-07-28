# Conventie voor ontwerpbesluiten

Architectuurbesluiten die de domeingrens, compilerketen of productcontracten
duurzaam veranderen, krijgen een herkenbaar besluitrecord.

## Minimale metadata

Ieder besluitrecord bevat:

- een oplopend ID in de vorm `ADR-0001`;
- een korte titel;
- status: `voorgesteld`, `geaccepteerd`, `vervangen` of `afgewezen`;
- datum in de vorm `JJJJ-MM-DD`;
- context en het probleem;
- het besluit;
- gevolgen en relevante beperkingen;
- een verwijzing naar het vervangende besluit wanneer de status `vervangen`
  is.

Een bestaand normatief document mag zelf het besluitrecord zijn. Een los
ADR-bestand is alleen nodig wanneer het besluit niet helder in zo'n document
thuishoort. `docs/world-model.md` is `ADR-0001`.

## Wijzigingsregel

Een geaccepteerd besluit wordt niet stilzwijgend herschreven wanneer de
richting verandert. Maak dan een nieuw besluitrecord en markeer het oude record
als vervangen.

## Mijlpaallogboek

`docs/product-model.md` bevat het bestaande mijlpaallogboek van het
productcontract. Daarom houdt dit project geen afzonderlijke `CHANGELOG.md`
bij. Pull requests en Git vormen het wijzigingslogboek; besluitrecords leggen
alleen duurzame architectuurkeuzes vast.
