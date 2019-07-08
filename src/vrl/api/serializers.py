from rest_framework import serializers

from vrl.datamodel.models import CommunicatieKanaal, ResultaattypeOmschrijvingGeneriek


class CommunicatieKanaalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommunicatieKanaal
        fields = ("url", "naam", "omschrijving")
        extra_kwargs = {"url": {"lookup_field": "uuid"}}


class ResultaattypeOmschrijvingGeneriekSerializer(
    serializers.HyperlinkedModelSerializer
):
    class Meta:
        model = ResultaattypeOmschrijvingGeneriek
        fields = ("url", "omschrijving", "definitie", "opmerking")
        extra_kwargs = {"url": {"lookup_field": "uuid"}}
