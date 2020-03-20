from rest_framework import serializers

from ..models import ProcesType


class ProcesTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcesType
        fields = (
            "url",
            "nummer",
            "naam",
            "omschrijving",
            "toelichting",
            "procesobject",
        )
        extra_kwargs = {"url": {"lookup_field": "uuid",}}
