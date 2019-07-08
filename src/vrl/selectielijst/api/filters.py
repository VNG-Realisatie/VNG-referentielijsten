from vng_api_common.filtersets import FilterSet

from ..models import Resultaat


class ResultaatFilter(FilterSet):
    class Meta:
        model = Resultaat
        fields = ("proces_type",)
