from channels.generic.websocket import AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
from djangochannelsrestframework.decorators import action


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        print('connection ses')

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(self)

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
