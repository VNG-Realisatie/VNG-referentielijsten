import os
import warnings

from .base import *

#
# Standard Django settings.
#

DEBUG = False

ADMINS = ()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vrl',
        # The database account jenkins/jenkins is always present for testing.
        'USER': 'jenkins',
        'PASSWORD': 'jenkins',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Empty for the default port. For testing, we use the following ports
        # for different databases. The default port is set to the latest
        # Debian stable database version.
        #
        # PostgreSQL 9.3: 5433
        # PostgreSQL 9.4: 5434  (and port 5432, the default port)
        # PostgreSQL 9.5: 5435
        # PostgreSQL 9.6: 5436
        'PORT': '',
        'TEST': {
            'NAME': 'test_vrl_{}_{}'.format(
                os.getenv('JOB_NAME', default='').lower().rsplit('/', 1)[-1],
                os.getenv('BUILD_NUMBER', default='0'),
            )
        }
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

LOGGING['loggers'].update({
    'django': {
        'handlers': ['django'],
        'level': 'WARNING',
        'propagate': True,
    },
})

#
# Custom settings
#

# Show active environment in admin.
ENVIRONMENT = 'jenkins'

#
# Django-axes
#
AXES_BEHIND_REVERSE_PROXY = False  # Required to allow FakeRequest and the like to work correctly.

# in memory cache and django-axes don't get along.
# https://django-axes.readthedocs.io/en/latest/configuration.html#known-configuration-problems
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'axes_cache': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

AXES_CACHE = 'axes_cache'

#
# Jenkins settings
#
INSTALLED_APPS += [
    'django_jenkins',
]
PROJECT_APPS = [app for app in INSTALLED_APPS if app.startswith('vrl.')]
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.run_pep8',
)

# THOU SHALT NOT USE NAIVE DATETIMES
warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields',
)
