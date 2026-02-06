import asyncio
import httpx
import os
from datetime import datetime
import json
from config.schemas import Event
from config.db_helper import db_helper
from app.models.camera.model import Camera
import logging
from sqlalchemy import update

logger = logging.getLogger(__name__)


class HikiVisionConnection:
    def __init__(self, device_ip: str , username:str, password:str ,camera_type: str, camera_id: int):
        self.device_ip = device_ip
        self.username = username
        self.password = password
        self.url = f"http://{self.device_ip}/ISAPI/Event/notification/alertStream?format=json"
        self.boundary = b"--MIME_boundary"
        self.camera_type = camera_type
        self.camera_id = camera_id
        

    async def connection_stream(self):
        """Connect to Hikvision device and yield each multipart 'part' as bytes."""
        auth = httpx.DigestAuth(self.username, self.password)

        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("GET", self.url, auth=auth) as response:
                if response.status_code != 200:
                    logger.error(f"Failed to connect: {response.status_code}")
                    await self.update_camera_status(False)
                    return

                logger.info(f"Connected to {self.device_ip}. Waiting for events...")
                await self.update_camera_status(True)

                buffer = b""
                async for chunk in response.aiter_bytes():
                    buffer += chunk
                    while True:
                        boundary_index = buffer.find(self.boundary)
                        if boundary_index == -1:
                            break

                        part = buffer[:boundary_index]
                        buffer = buffer[boundary_index + len(self.boundary):]
                        part = part.lstrip(b"\r\n")

                        if part.strip():
                            yield part

    def save_image(self, image_bytes: bytes):
        """Save image to images/ with timestamp and update user log."""
        os.makedirs("images", exist_ok=True)
        filename = f"images/{datetime.now():%Y%m%d_%H%M%S_%f}.jpg"
        with open(filename, "wb") as f:
            f.write(image_bytes)

        logger.info(f"Image saved: {filename}")
        return filename

    async def process_part(self, part: bytes):
        """Process one part of the multipart stream."""
        header_end = part.find(b"\r\n\r\n")
        if header_end == -1:
            return

        headers_raw = part[:header_end].decode(errors="ignore")
        content = part[header_end + 4:]

        if "application/json" in headers_raw:
            try:
                json_data = json.loads(content.decode(errors="ignore"))
                event_type = json_data.get("eventType")
                ip_address = json_data.get("ipAddress")
                dt = json_data.get("dateTime")

                if event_type == "AccessControllerEvent":
                    name = json_data.get("AccessControllerEvent", {}).get("employeeNoString")
                    person = name if name else "unknown"
                    
                    if person == "unknown":
                        pass
                    else:
                        event = Event(
                            user_id=person, 
                            time=dt,
                            camera_type=self.camera_type,
                            ip_address=ip_address
                            )
                        # Instead of calling save_log directly, use repo
                        async with db_helper.session_factory() as session:
                            repo = UserLogsRepository(session)
                            await repo.save_log(event=event)
                        
                        logger.info(f"Published AccessControllerEvent: {event.model_dump()}, data: {json_data}")

                elif event_type == "Non-AccessControllerEvent":
                    logger.info(f"Ignored Non-AccessControllerEvent: {json_data}")

                else:
                    logger.warning(f"Unknown event type: {event_type}, data: {json_data}")

            except Exception as e:
                logger.error(f"Failed to parse JSON: {e}", exc_info=True)

        # elif "image/jpeg" in headers_raw:
        #     self.save_image(content)
        else:
            logger.warning("Unknown content type in part")


    async def stream_events(self):
        """Main loop: read parts from the stream and process them. Includes reconnection logic."""
        while True:
            try:
                logger.info(f"Attempting to connect to {self.device_ip}...")
                async for part in self.connection_stream():
                    await self.process_part(part)
            except (httpx.ConnectError, httpx.ReadError) as e:
                logger.error(f"Connection to {self.device_ip} failed: {e}")
                await self.update_camera_status(False)
                logger.info(f"Retrying connection in 30 seconds...")
                await asyncio.sleep(30)
            except Exception as e:
                logger.error(f"Unhandled streaming error from {self.device_ip}: {e}", exc_info=True)
                await self.update_camera_status(False)
                logger.info(f"Retrying connection in 30 seconds...")
                await asyncio.sleep(30)

    async def update_camera_status(self, status: bool):
        """Update camera status in the database."""
        try:
            async with db_helper.session_factory() as session:
                stmt = (
                    update(Camera)
                    .where(Camera.id == self.camera_id)
                    .values(status=status)
                )
                await session.execute(stmt)
                await session.commit()
                # logger.info(f"Updated camera {self.device_ip} status to {status}")
        except Exception as e:
            logger.error(f"Failed to update camera status for {self.device_ip}: {e}")