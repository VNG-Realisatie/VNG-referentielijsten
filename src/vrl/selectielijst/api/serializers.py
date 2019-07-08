from rest_framework import serializers
from vng_api_common.serializers import add_choice_values_help_text

from ..constants import Procestermijnen
from ..models import ProcesType, Resultaat


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
        extra_kwargs = {"url": {"lookup_field": "uuid"}}


class ResultaatSerializer(serializers.ModelSerializer):
    proces_type = serializers.HyperlinkedRelatedField(
        view_name="procestype-detail", lookup_field="uuid", read_only=True
    )
    procestermijn_weergave = serializers.CharField(
        source="get_procestermijn_display", read_only=True
    )

    class Meta:
        model = Resultaat
        fields = (
            "url",
            "proces_type",
            "nummer",
            "volledig_nummer",
            "generiek",
            "specifiek",
            "naam",
            "omschrijving",
            "herkomst",
            "waardering",
            "procestermijn",
            "procestermijn_weergave",
            "bewaartermijn",
            "toelichting",
            "algemeen_bestuur_en_inrichting_organisatie",
            "bedrijfsvoering_en_personeel",
            "publieke_informatie_en_registratie",
            "burgerzaken",
            "veiligheid",
            "verkeer_en_vervoer",
            "economie",
            "onderwijs",
            "sport_cultuur_en_recreatie",
            "sociaal_domein",
            "volksgezonheid_en_milieu",
            "vhrosv",
            "heffen_belastingen",
            "alle_taakgebieden",
            "procestermijn_opmerking",
        )
        extra_kwargs = {"url": {"lookup_field": "uuid"}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(Procestermijnen)
        self.fields["procestermijn"].help_text = value_display_mapping
