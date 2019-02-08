from django.conf.urls import url
from django.urls import include, path

from zds_schema import routers
from zds_schema.schema import SchemaView

from vrl.selectielijst.api.viewsets import ProcesTypeViewSet

from .viewsets import CommunicatieKanaalViewSet

router = routers.DefaultRouter()
router.register('communicatiekanalen', CommunicatieKanaalViewSet)
router.register('procestypen', ProcesTypeViewSet)


# TODO: the EndpointEnumerator seems to choke on path and re_path

urlpatterns = [
    url(r'^v(?P<version>\d+)/', include([

        # API documentation
        url(r'^schema/openapi(?P<format>\.json|\.yaml)$',
            SchemaView.without_ui(cache_timeout=None),
            name='schema-json'),
        url(r'^schema/$',
            SchemaView.with_ui('redoc', cache_timeout=None),
            name='schema-redoc'),

        # actual API
        url(r'^', include(router.urls)),

        # should not be picked up by drf-yasg
        path('', include('zds_schema.api.urls')),
    ])),
]
