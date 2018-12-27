from django.contrib import admin

from .models import CommunicatieKanaal


@admin.register(CommunicatieKanaal)
class CommunicatieKanaalAdmin(admin.ModelAdmin):
    list_display = ('naam', 'omschrijving')
    search_fields = ('naam', 'omschrijving')
    ordering = ('naam',)
