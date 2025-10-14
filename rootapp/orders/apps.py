from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rootapp.orders'

    def ready(self):
        import rootapp.orders.signals
