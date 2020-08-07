from vng_api_common.filtersets import FilterSet

from ..models import ProcesType, Resultaat


class ResultaatFilter(FilterSet):
    class Meta:
        model = Resultaat
        fields = ("proces_type",)


class ProcesTypeFilter(FilterSet):
    class Meta:
        model = ProcesType
        fields = ("jaar",)
