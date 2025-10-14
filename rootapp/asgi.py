from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import os
import dotenv
import rootapp.routing

dotenv.load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 
                      os.getenv("DJANGO_SETTINGS_MODULE", 
                                "rootapp.settings.base"))

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            rootapp.routing.websocket_urlpatterns
        )
    ),
})
