import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime, timedelta


from .models import Message, Conversation
from user.models import User
from .serializers import GetMessageSerializer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.sender_id = self.scope["url_route"]["kwargs"]["sender_id"]
        self.room_group_name = f"chat{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from websocket
    def receive(self, text_data=None, bytes_data=None):
        # parse json data into dictionary object
        text_data_json = json.loads(text_data)

        # send message to room group
        chat_type = {"type": "chat_message"}
        return_dict = {**chat_type, **text_data_json}
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, return_dict)

    # Receive message from room group
    def chat_message(self, event):
        text_data_json = event.copy()
        text_data_json.pop("type")
        message_text, attachment = (
            text_data_json["message"],
            text_data_json.get("attachment"),
        )

        conversation = Conversation.objects.get(id=str(self.room_name))
        sender = User.objects.get(id=self.sender_id)

        # to avoid duplicate messages
        time_threshold = datetime.now() - timedelta(minutes=1)
        similar_messages = Message.objects.filter(
            text=message_text,
            sender=sender,
            created_at__gte=time_threshold,
        )

        # if not similar_messages.exists():
        message = Message.objects.create(
            sender=sender,
            text=message_text,
            conversation=conversation,
        )
        serializer = GetMessageSerializer(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps(serializer.data))
        # else:
        #     serializer = GetMessageSerializer(similar_messages.first())
        #     # Send message to WebSocket
        #     self.send(text_data=json.dumps(serializer.data))


chat_consumer_asgi = ChatConsumer.as_asgi()
