from rest_framework import serializers

from vrl.datamodel.models import CommunicatieKanaal


class CommunicatieKanaalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CommunicatieKanaal
        fields = ("url", "naam", "omschrijving")
        extra_kwargs = {"url": {"lookup_field": "uuid",}}
