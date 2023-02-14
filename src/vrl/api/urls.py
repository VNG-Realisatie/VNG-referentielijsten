from django.conf.urls import url
from django.urls import include, path

from vng_api_common import routers
from vng_api_common.views import SchemaViewAPI, SchemaViewRedoc

from vrl.selectielijst.api.viewsets import ProcesTypeViewSet, ResultaatViewSet

from .viewsets import (
    CommunicatieKanaalViewSet,
    ResultaattypeOmschrijvingGeneriekViewSet,
)

router = routers.DefaultRouter()
router.register("communicatiekanalen", CommunicatieKanaalViewSet)
router.register("resultaattypeomschrijvingen", ResultaattypeOmschrijvingGeneriekViewSet)
router.register("procestypen", ProcesTypeViewSet)
router.register("resultaten", ResultaatViewSet)

urlpatterns = [
    url(
        r"^v(?P<version>\d+)/",
        include(
            [
                url(
                    r"^schema/openapi.yaml",
                    SchemaViewAPI.as_view(),
                    name="schema",
                ),
                url(
                    r"^schema/",
                    SchemaViewRedoc.as_view(url_name="schema-redoc"),
                    name="schema-redoc",
                ),
                # actual API
                url(r"^", include(router.urls)),
                # should not be picked up by drf-spectacular
                path("", include("vng_api_common.api.urls")),
                path("", include("vng_api_common.notifications.api.urls")),
            ]
        ),
    )
]
