# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
import json

from asgiref.sync import async_to_sync
from .serializers import MessageSerializers
from .models import Message
from rest_framework.renderers import JSONRenderer
class ChatConsumer(WebsocketConsumer):

    def new_message(self,data):
        ...
    def fetch_message(self,data):
        qs=Message.last_message(self)
        message_json=self.message_serializer(qs)
        content={
            'message':eval(message_json)
        }

    def message_serializer(self,qs):
        serialized=MessageSerializers(qs,many=True)
        content=JSONRenderer().render(serialized.data)
        return content

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()


    commands={
        "new_message":new_message,
        "fetch_message":fetch_message
    }


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message',None)
        command=text_data_json['command']
        self.commands[command](self,message)

        # Send message to room group
    def send_to_chat_message(self,message):            
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]  
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))