import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time notifications
    """

    async def connect(self):
        """
        Called when the websocket is handshaking as part of initial connection.
        """
        self.user = self.scope["user"]

        # Reject connection if user is not authenticated
        if not self.user.is_authenticated:
            await self.close()
            return

        # Create a unique room name for this user
        self.room_group_name = f"notifications_{self.user.id}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        # Send initial connection success message
        await self.send(
            text_data=json.dumps(
                {"type": "connection_established", "message": "Connected to notifications"}
            )
        )

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave room group
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        """
        Called when we get a message from the WebSocket client.
        """
        try:
            data = json.loads(text_data)
            message_type = data.get("type")

            if message_type == "ping":
                # Respond to ping with pong to keep connection alive
                await self.send(text_data=json.dumps({"type": "pong"}))

        except json.JSONDecodeError:
            await self.send(
                text_data=json.dumps({"type": "error", "message": "Invalid JSON"})
            )

    async def notification_message(self, event):
        """
        Called when a notification is sent to the group.
        Sends the notification to the WebSocket.
        """
        notification_data = event["notification"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"type": "notification", "notification": notification_data}
            )
        )

    async def unread_count_update(self, event):
        """
        Called when unread count needs to be updated.
        """
        count = event["count"]

        # Send unread count update to WebSocket
        await self.send(
            text_data=json.dumps({"type": "unread_count", "count": count})
        )
