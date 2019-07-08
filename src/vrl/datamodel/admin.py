from django.contrib import admin

from .models import CommunicatieKanaal, ResultaattypeOmschrijvingGeneriek


@admin.register(CommunicatieKanaal)
class CommunicatieKanaalAdmin(admin.ModelAdmin):
    list_display = ("naam", "omschrijving")
    search_fields = ("naam", "omschrijving")
    ordering = ("naam",)


@admin.register(ResultaattypeOmschrijvingGeneriek)
class ResultaattypeOmschrijvingGeneriekAdmin(admin.ModelAdmin):
    list_display = ("omschrijving", "definitie", "uuid")
    search_fields = ("omschrijving", "definitie", "opmerking", "uuid")
