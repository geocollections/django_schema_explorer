"""
WSGI config for geokogud_schema project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_schema_explorer.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import django_schema_explorer.monitor
django_schema_explorer.monitor.start(interval=1.0)
