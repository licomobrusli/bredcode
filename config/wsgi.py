"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings
print("WSGI/ASGI DEBUG Mode:", settings.DEBUG)

import logging
logger = logging.getLogger(__name__)
logger.debug('Docker container started - logging system initialized.')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
