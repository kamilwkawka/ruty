

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import users.routing
from ruty.middleware import TokenAuthMiddleware


application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            users.routing.websocket_urlpatterns
        )
    )
})