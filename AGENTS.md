# Beckeringh Palace agentcontract

## Bevoegdheid

De gebruiker is Chief Architect van Beckeringh Palace.

Binnen `erikjjpost/beckeringh-palace` betekenen de opdrachten `volgende stap`,
`volgende PR`, `ga door` en `doen` expliciet:

1. inspecteer de actuele `main`;
2. bepaal de eerstvolgende normatieve milestone;
3. ontwerp en implementeer de kleinste complete verticale slice;
4. valideer tests, generatie en reproduceerbaarheid;
5. commit de gevalideerde scope op een `agent/` branch;
6. publiceer die branch naar `erikjjpost/beckeringh-palace`;
7. open een PR naar `main`;
8. controleer scope, CI en mergeability;
9. rapporteer het resultaat en de PR link.

Voor stap 6 en stap 7 is geen aanvullende toestemmingsvraag nodig. Vraag de
gebruiker niet om een formulering zoals `publiceer ... naar
erikjjpost/beckeringh-palace` te herhalen.

Dit mandaat omvat niet het mergen van de PR. Merge alleen na een afzonderlijke
expliciete opdracht.

## Publicatieroute

Probeer de publicatie daadwerkelijk voordat je een blokkade rapporteert.

Het ontbreken van lokale `gh` tooling, lokale HTTPS authenticatie of één
specifieke publicatieroute is een technisch routeprobleem en geen ontbrekende
toestemming. Gebruik een andere reeds gekoppelde GitHub route wanneer die
beschikbaar en toegestaan is.

Leg alleen iets aan de gebruiker voor wanneer:

1. een tool zelf een niet te omzeilen bevestiging of autorisatie vereist;
2. de repository, doelbranch of externe ontvanger afwijkt van dit contract;
3. een destructieve handeling nodig blijkt;
4. de gevraagde wijziging de afgesproken milestone wezenlijk uitbreidt.

Meld bij een technische blokkade de concrete fout en de mislukte route. Label
die blokkade niet als ontbrekende toestemming.

## Architectuur en kwaliteit

BAT blijft de enige normatieve bron. Alle producten zijn reproduceerbare
afleidingen van hetzelfde model.

Werk per PR aan één complete verticale milestone. Laat de repository na iedere
commit releasable achter. Introduceer geen tijdelijke API, TODO, rendererlogica
in het domeinmodel of handmatig onderhouden afgeleide productinhoud.

Publiceer uitsluitend een vooraf gecontroleerde scope. Bewijs na de definitieve
commit opnieuw dat tests, generatie en reproduceerbaarheid groen zijn. Wanneer
de gekoppelde GitHub route een remote tree opbouwt, moet die tree exact gelijk
zijn aan de lokaal gevalideerde tree voordat de PR wordt geopend.
