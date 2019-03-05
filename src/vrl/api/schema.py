from django.conf import settings

from drf_yasg import openapi

info = openapi.Info(
    title="Referentielijsten API",
    default_version=settings.API_VERSION,
    description="Een API om referentielijstwaarden te benaderen",
    contact=openapi.Contact(
        email="support@maykinmedia.nl",
        url="https://github.com/maykinmedia/vng-referentielijsten"
    ),
    license=openapi.License(
        name="EUPL 1.2",
        url='https://opensource.org/licenses/EUPL-1.2'
    ),
)
