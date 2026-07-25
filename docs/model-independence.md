# Modelonafhankelijkheid

Rollen, taken, contracten en bevoegdheden zijn onderdeel van de architectuur. Concrete taalmodellen en providers zijn vervangbare implementaties.

Providerspecifieke logica hoort uitsluitend in een toekomstige adapterlaag en niet in `model/` of `organisation/`.
