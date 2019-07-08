from rest_framework import viewsets

from ..models import ProcesType, Resultaat
from .filters import ResultaatFilter
from .serializers import ProcesTypeSerializer, ResultaatSerializer


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


class ResultaatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Ontsluit de selectielijst resultaten.

    Bij een procestype horen meerdere mogelijke resultaten, al dan niet
    generiek/specifiek. Bij het configureren van een resultaattype in het ZTC
    wordt aangegeven welke selectielijstklasse van toepassing is, wat een
    referentie is naar een item van deze resource.

    Zie https://vng.nl/files/vng/20170706-selectielijst-gemeenten-intergemeentelijke-organen-2017.pdf
    voor de bron van de inhoud.
    """

    queryset = Resultaat.objects.tree_order()
    serializer_class = ResultaatSerializer
    lookup_field = "uuid"
    filterset_class = ResultaatFilter
