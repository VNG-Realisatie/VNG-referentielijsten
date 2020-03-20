from rest_framework import viewsets

from ..models import ProcesType
from .serializers import ProcesTypeSerializer


class ProcesTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Ontsluit de selectielijst procestypen.

    Procestypen worden gerefereerd in zaaktypecatalogi - bij het configureren
    van een zaaktype wordt aangegeven welk procestype van toepassing is, zodat
    het archiefregime van zaken bepaald kan worden.

    Zie https://vng.nl/files/vng/20170706-selectielijst-gemeenten-intergemeentelijke-organen-2017.pdf
    voor de bron van de inhoud.
    """

    queryset = ProcesType.objects.order_by("nummer")
    serializer_class = ProcesTypeSerializer
    lookup_field = "uuid"
    pagination_class = None
