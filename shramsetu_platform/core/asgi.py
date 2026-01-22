"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()
# settings.py

STATIC_URL = 'static/'

# Add this to tell Django where your files are
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'services/static'),
]
