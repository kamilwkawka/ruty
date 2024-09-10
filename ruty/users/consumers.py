import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Group, Message
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'group_{self.group_id}'

        is_member = await self.is_user_in_group(self.scope['user'], self.group_id)
        if not is_member:
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        if message:
            user = self.scope['user']
            saved_message = await self.save_message(user, self.group_id, message)
            serialized_message = MessageSerializer(saved_message).data

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': serialized_message
                }
            )
    
    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def is_user_in_group(self, user, group_id):
        try:
            group = Group.objects.get(id=group_id)
            return group.members.filter(user=user).exists()
        except Group.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, user, group_id, content):
        group = Group.objects.get(id=group_id)
        return Message.objects.create(user=user, group=group, content=content)
    