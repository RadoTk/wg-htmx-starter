from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Order)
def notify_new_order_via_websocket(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'orders_admin',
            {
                'type': 'send_new_order',
                'message': 'Nouvelle commande reçue ! Cliquez ici pour la charger.',
            }
        )
