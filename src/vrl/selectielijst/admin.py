from django.contrib import admin

from .models import ProcesType


@admin.register(ProcesType)
class ProcesTypeAdmin(admin.ModelAdmin):
    list_display = ('nummer', 'naam', 'omschrijving', 'uuid')
    ordering = ('nummer',)
    search_fields = ('nummer', 'naam', 'omschrijving')
