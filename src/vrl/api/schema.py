from django.conf import settings

__all__ = [
    "TITLE",
    "DESCRIPTION",
    "CONTACT",
    "LICENSE",
    "VERSION",
]

DESCRIPTION = """
Een API om referentielijstwaarden en de gemeentelijke selectielijst te
benaderen.

## Selectielijst

De [Gemeentelijke Selectielijst](https://vng.nl/selectielijst) is relevant
in het kader van archivering.

**Zaakgericht werken**

Bij het configureren van zaaktypes (en resultaattypes) in de catalogus API
refereren een aantal resources naar resources binnen de Selectielijst API. Het
gaat dan om de `ProcesType` en `Resultaat` resources.

## Referentielijsten

Referentielijsten bevat een standaardset aan waarden. Deze waarden zijn net té
dynamisch om in een enum opgenomen te worden, maar er is wel behoefte om deze
landelijk te standaardiseren. Een voorbeeld hiervan is de set aan mogelijke
communicatiekanalen.

## Autorisatie

Deze APIs zijn alleen-lezen, en behoeven geen autorisatie.

## Inhoud

De inhoud wordt beheerd door VNG Realisatie. Om de inhoud van
referentielijsten bij te werken, contacteer dan VNG Realisatie via e-mail of
op Github.

De inhoud van de Gemeentelijke Selectielijst wordt geïmporteerd vanuit de
gepubliceerde Excel-bestanden.
"""


TITLE = f"{settings.PROJECT_NAME} API"

VERSION = settings.API_VERSION
CONTACT = {
    "email": "standaarden.ondersteuning@vng.nl",
    "url": "https://github.com/VNG-Realisatie/VNG-referentielijsten",
}
LICENSE = {"name": "EUPL 1.2", "url": "https://opensource.org/licenses/EUPL-1.2"}
