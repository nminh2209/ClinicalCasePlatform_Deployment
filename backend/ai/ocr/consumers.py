"""
WebSocket Consumer for OCR Progress Updates

Provides real-time progress updates to the frontend during OCR processing,
replacing HTTP polling with push-based notifications.

Usage:
    Frontend connects to: ws://host/ws/ocr/{job_id}/
    Receives JSON messages: {"page": 1, "total": 10, "status": "processing"}
"""

import json
import logging
from channels.generic.websocket import AsyncJsonWebsocketConsumer

logger = logging.getLogger(__name__)


class OCRProgressConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for OCR job progress updates.
    
    Groups are named by job_id so Celery tasks can send updates
    to specific clients watching that job.
    """
    
    async def connect(self):
        """Called when client connects to WebSocket."""
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.group_name = f"ocr_{self.job_id}"
        
        # Join the job-specific group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"WebSocket connected for OCR job: {self.job_id}")
        
        # Send initial connection confirmation
        await self.send_json({
            "type": "connected",
            "job_id": self.job_id,
            "message": "Listening for OCR progress updates"
        })
    
    async def disconnect(self, close_code):
        """Called when client disconnects."""
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected for OCR job: {self.job_id}")
    
    async def ocr_progress(self, event):
        """
        Handler for 'ocr.progress' messages from Celery tasks.
        
        Celery tasks send:
            async_to_sync(channel_layer.group_send)(
                f"ocr_{job_id}",
                {"type": "ocr.progress", "data": {...}}
            )
        """
        await self.send_json(event.get("data", {}))
    
    async def ocr_complete(self, event):
        """Handler for 'ocr.complete' messages when job finishes."""
        await self.send_json({
            "type": "complete",
            "status": "done",
            **event.get("data", {})
        })
    
    async def ocr_error(self, event):
        """Handler for 'ocr.error' messages on failure."""
        await self.send_json({
            "type": "error",
            "status": "failed",
            "error": event.get("error", "Unknown error")
        })


# Helper function for Celery tasks to send progress updates
def send_ocr_progress(job_id: str, page: int, total: int, status: str = "processing"):
    """
    Send OCR progress update via WebSocket.
    
    Call this from Celery tasks to push real-time updates.
    
    Example:
        send_ocr_progress(self.request.id, page=3, total=10, status="processing")
    """
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    channel_layer = get_channel_layer()
    if channel_layer is None:
        logger.warning("Channel layer not available - WebSocket updates disabled")
        return
    
    try:
        async_to_sync(channel_layer.group_send)(
            f"ocr_{job_id}",
            {
                "type": "ocr.progress",
                "data": {
                    "page": page,
                    "total": total,
                    "status": status,
                    "progress_percent": round((page / total) * 100) if total > 0 else 0
                }
            }
        )
    except Exception as e:
        logger.warning(f"Failed to send WebSocket progress: {e}")


def send_ocr_complete(job_id: str, tables: list = None, images: list = None):
    """Send OCR completion notification via WebSocket."""
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    
    try:
        async_to_sync(channel_layer.group_send)(
            f"ocr_{job_id}",
            {
                "type": "ocr.complete",
                "data": {
                    "tables": tables or [],
                    "images": images or [],
                    "table_count": len(tables or []),
                    "image_count": len(images or [])
                }
            }
        )
    except Exception as e:
        logger.warning(f"Failed to send WebSocket completion: {e}")
