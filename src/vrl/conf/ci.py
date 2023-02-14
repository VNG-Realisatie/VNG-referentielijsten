import warnings

from .base import *

#
# Standard Django settings.
#

DEBUG = False

ADMINS = ()

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

LOGGING["loggers"].update(
    {"django": {"handlers": ["django"], "level": "WARNING", "propagate": True}}
)

#
# Custom settings
#

# Show active environment in admin.
ENVIRONMENT = "jenkins"

#
# Django-axes
#
AXES_BEHIND_REVERSE_PROXY = (
    False  # Required to allow FakeRequest and the like to work correctly.
)

# in memory cache and django-axes don't get along.
# https://django-axes.readthedocs.io/en/latest/configuration.html#known-configuration-problems
CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "axes_cache": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
}

AXES_CACHE = "axes_cache"

#
# Jenkins settings
#
INSTALLED_APPS += ["django_jenkins"]
PROJECT_APPS = [app for app in INSTALLED_APPS if app.startswith("vrl.")]
JENKINS_TASKS = ("django_jenkins.tasks.run_pylint", "django_jenkins.tasks.run_pep8")

# THOU SHALT NOT USE NAIVE DATETIMES
warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)
