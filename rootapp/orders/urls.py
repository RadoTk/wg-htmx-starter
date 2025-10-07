from django.urls import path
from . import views
from .views import order_create

app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name="order_create"),
    path('order/thanks/', views.order_thanks, name='order_thanks'),
]