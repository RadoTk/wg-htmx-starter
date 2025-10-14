from django.urls import path
from rootapp.orders.consumers import OrdersAdminConsumer

websocket_urlpatterns = [
    path("ws/admin/orders/", OrdersAdminConsumer.as_asgi()),
]
