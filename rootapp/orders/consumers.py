import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrdersAdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'orders_admin'

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket (pas utilisé ici, mais utile si besoin)
    async def receive(self, text_data):
        pass

    # Receive message from group
    async def send_new_order(self, event):
        # Envoyer les données vers le client WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_order',
            'message': event['message'],
        }))
