"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'server',
    'rest_framework',
    'rest_framework_swagger',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'server.middleware.CORSMiddleware',
)

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


# Templates
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Rest framework settings

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGINATE_BY': 10
}


# Avoid redirecting URLs that don't have trailing slashes

APPEND_SLASH = False


# Swagger (documentation module) settings

SWAGGER_SETTINGS = {
    "exclude_namespaces": [], # List URL namespaces to ignore
    "api_version": '0.1',  # Specify your API's version
    "api_path": "/",  # Specify the path to your API not a root level
    "enabled_methods": [  # Specify which methods to enable in Swagger UI
        'get',
        #'post',
        #'put',
        #'patch',
        #'delete'
    ],
    "api_key": '', # An API key
    "is_authenticated": False,  # Set to True to enforce user authentication,
    "is_superuser": False,  # Set to True to enforce admin only access
}


# Django auth LDAP

import ldap
from django_auth_ldap.config import LDAPSearch

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = os.environ['NU_LDAP_URL']
AUTH_LDAP_BIND_DN = 'cn=asgnulink,ou=pwcheck,dc=northwestern,dc=edu'
AUTH_LDAP_BIND_PASSWORD = os.environ['NU_LDAP_PASSWORD']
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
    'username': 'uid',
}
AUTH_LDAP_ALWAYS_UPDATE_USER = False
AUTH_LDAP_BASE_DN = 'dc=northwestern,dc=edu'
AUTH_LDAP_USER_SEARCH = LDAPSearch(AUTH_LDAP_BASE_DN,
    ldap.SCOPE_SUBTREE, '(uid=%(user)s)')


# Redirect logged-in users to their projects pages

LOGIN_URL = '/manage/login/'
LOGIN_REDIRECT_URL = '/manage/projects/'


# Configure logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {        
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {},
}


try:
    from local_settings import *
except ImportError:
    pass

if DEBUG:
    MIDDLEWARE_CLASSES += ('server.middleware.QueryCountDebugMiddleware',)
    LOGGING['loggers']['server.middleware'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
    }
