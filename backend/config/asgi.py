"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/

Future Enhancement:
    This file will be updated to wrap Django Channels routing
    for WebSocket support (real-time POS updates, notifications).
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# TODO: Wrap with Channels routing for WebSocket support
# from channels.routing import ProtocolTypeRouter, URLRouter
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": URLRouter([...]),
# })
application = get_asgi_application()
