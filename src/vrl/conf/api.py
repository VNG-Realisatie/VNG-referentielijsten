import os

from vng_api_common.conf.api import *  # noqa - imports white-listed

API_VERSION = "0.6.0"

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK[
    "DEFAULT_PAGINATION_CLASS"
] = "rest_framework.pagination.PageNumberPagination"
REST_FRAMEWORK["PAGE_SIZE"] = 100

DOCUMENTATION_INFO_MODULE = "vrl.api.schema"

SPECTACULAR_SETTINGS = BASE_SPECTACULAR_SETTINGS.copy()
SPECTACULAR_SETTINGS.update(
    {
        "SERVERS": [{"url": "https://referentielijsten-api.test.vng.cloud/api/v1"}],
        # todo remove this line below when deploying to production
        "SORT_OPERATION_PARAMETERS": False,
    }
)
SPECTACULAR_EXTENSIONS = [
    "vng_api_common.extensions.fields.duration.DurationFieldExtension",
    "vng_api_common.extensions.fields.history_url.HistoryURLFieldExtension",
    "vng_api_common.extensions.fields.hyperlink_identity.HyperlinkedIdentityFieldExtension",
    "vng_api_common.extensions.fields.many_related.ManyRelatedFieldExtension",
    "vng_api_common.extensions.fields.read_only.ReadOnlyFieldExtension",
    "vng_api_common.extensions.filters.query.FilterExtension",
    "vng_api_common.extensions.serializers.gegevensgroep.GegevensGroepExtension",
]

SELF_REPO = "VNG-Realisatie/VNG-referentielijsten"
SELF_BRANCH = os.getenv("SELF_BRANCH") or API_VERSION

GITHUB_API_SPEC = f"https://raw.githubusercontent.com/{SELF_REPO}/{SELF_BRANCH}/src/openapi.yaml"  # noqa
