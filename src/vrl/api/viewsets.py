from rest_framework import viewsets

from vrl.datamodel.models import (
    CommunicatieKanaal, ResultaattypeOmschrijvingGeneriek
)

from .serializers import (
    CommunicatieKanaalSerializer, ResultaattypeOmschrijvingGeneriekSerializer
)


class CommunicatieKanaalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Raadpleeg de lijst van communicatiekanalen.
    """
    queryset = CommunicatieKanaal.objects.order_by('naam')
    serializer_class = CommunicatieKanaalSerializer
    lookup_field = 'uuid'


class ResultaattypeOmschrijvingGeneriekViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Raadpleeg de generieke resultaattypeomschrijvingen.
    """
    queryset = ResultaattypeOmschrijvingGeneriek.objects.order_by('omschrijving')
    serializer_class = ResultaattypeOmschrijvingGeneriekSerializer
    lookup_field = 'uuid'
    pagination_class = None
