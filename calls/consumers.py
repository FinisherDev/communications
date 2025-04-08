import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"call_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        try:
            print(f"Received raw message: {text_data}")  # Log raw message
            data = json.loads(text_data)  # Try to parse JSON
            print(f"Parsed JSON: {data}")  # Log parsed JSON
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")  # Log JSON errors
        await self.channel_layer.group_send(self.room_group_name, {"type": "signal", "message": data})

    async def signal(self, event):
        print("Testing: ", json.dumps(event["message"]))
        await self.send(text_data = json.dumps(event["message"]))