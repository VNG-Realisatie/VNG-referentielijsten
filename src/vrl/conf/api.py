from vng_api_common.conf.api import *  # noqa - imports white-listed

API_VERSION = "1.0.0-alpha"

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()
REST_FRAMEWORK[
    "DEFAULT_PAGINATION_CLASS"
] = "rest_framework.pagination.PageNumberPagination"
REST_FRAMEWORK["PAGE_SIZE"] = 100

SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()
SWAGGER_SETTINGS.update(
    {
        "DEFAULT_INFO": "vrl.api.schema.info",
        "SECURITY_DEFINITIONS": {},
        "DEFAULT_FIELD_INSPECTORS": BASE_SWAGGER_SETTINGS["DEFAULT_FIELD_INSPECTORS"][
            1:
        ],
    }
)
