from rest_framework import viewsets

from vrl.datamodel.models import CommunicatieKanaal

from .serializers import CommunicatieKanaalSerializer


class CommunicatieKanaalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Raadpleeg de lijst van communicatiekanalen.
    """

    queryset = CommunicatieKanaal.objects.order_by("naam")
    serializer_class = CommunicatieKanaalSerializer
    lookup_field = "uuid"
