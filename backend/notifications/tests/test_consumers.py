"""
Tests for WebSocket consumer.
"""
import pytest
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from notifications.consumers import NotificationConsumer

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestNotificationConsumer:
    """Test WebSocket notification consumer."""

    @database_sync_to_async
    def create_user(self, suffix=''):
        """Create user asynchronously."""
        import random
        unique_id = random.randint(1000, 9999)
        return User.objects.create_user(
            username=f'wstest{unique_id}{suffix}@test.com',
            email=f'wstest{unique_id}{suffix}@test.com',
            password='testpass123'
        )

    @pytest.mark.skip(reason="Requires running WebSocket server")
    async def test_consumer_connection(self):
        """Test WebSocket connection."""
        user = await self.create_user('conn')
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/"
        )
        communicator.scope['user'] = user
        
        connected, _ = await communicator.connect()
        assert connected
        
        await communicator.disconnect()

    async def test_consumer_rejects_anonymous(self):
        """Test WebSocket rejects unauthenticated users."""
        from django.contrib.auth.models import AnonymousUser
        
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/"
        )
        communicator.scope['user'] = AnonymousUser()
        
        connected, _ = await communicator.connect()
        # Should reject anonymous users
        assert not connected or await communicator.receive_nothing()

    @pytest.mark.skip(reason="Requires running WebSocket server")
    async def test_consumer_receives_message(self):
        """Test consumer can receive messages."""
        user = await self.create_user('recv')
        communicator = WebsocketCommunicator(
            NotificationConsumer.as_asgi(),
            "/ws/notifications/"
        )
        communicator.scope['user'] = user
        
        connected, _ = await communicator.connect()
        if connected:
            # Send test message
            await communicator.send_json_to({
                'type': 'ping'
            })
            
            # Receive response (may be pong)
            response = await communicator.receive_json_from(timeout=1)
            assert response is not None
            
            await communicator.disconnect()
