from django.urls import path
from rootapp.orders.consumers import OrdersNotificationAdminConsumer

websocket_urlpatterns = [
    path("ws/admin/orders/", OrdersNotificationAdminConsumer.as_asgi()),
]
