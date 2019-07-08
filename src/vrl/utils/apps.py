from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "vrl.utils"

    def ready(self):
        from . import checks  # noqa
