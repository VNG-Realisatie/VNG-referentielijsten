from zds_schema.filtersets import FilterSet

from ..models import Resultaat


class ResultaatFilter(FilterSet):
    class Meta:
        model = Resultaat
        fields = ('proces_type',)
