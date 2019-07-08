from django.contrib import admin

from .models import ProcesType, Resultaat


@admin.register(ProcesType)
class ProcesTypeAdmin(admin.ModelAdmin):
    list_display = ("nummer", "naam", "omschrijving", "uuid")
    ordering = ("nummer",)
    search_fields = ("nummer", "naam", "omschrijving")


@admin.register(Resultaat)
class ResultaatAdmin(admin.ModelAdmin):
    list_display = (
        "proces_type",
        "volledig_nummer",
        "naam",
        "is_generiek",
        "procestermijn",
        "bewaartermijn",
    )
    list_filter = ("proces_type", "generiek_resultaat")
    list_select_related = ("proces_type", "generiek_resultaat")
    search_fields = ("naam", "omschrijving")

    def get_queryset(self, request=None):
        base = super().get_queryset(request=request)
        return base.tree_order()

    def is_generiek(self, obj):
        return obj.generiek

    is_generiek.boolean = True
