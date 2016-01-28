"""
Django settings for django_schema_explorer project.

For more information on this file and
for the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/topics/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '975(23i72w9n)4rn)=26%ch)xio4694zw(f!zfsh#q_rp(3uv@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

from django_schema_explorer.local_settings import DATABASES, ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = (
    'apps.schema',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR,'templates'),
)


ROOT_URLCONF = 'django_schema_explorer.urls'

WSGI_APPLICATION = 'django_schema_explorer.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# Custom settings

# Hidden models 
EXCLUDE_LIST=('DbTables',
              'TableFields',

)

URL_ROOT='schema.example.com'

TABLE_DESCRIPTION_MODEL='DbTables'

FIELD_DESCRIPTION_MODEL='TableFields'
