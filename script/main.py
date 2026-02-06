import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from script.connect import HikiVisionConnection
from config.db_helper import db_helper
from app.models.camera.model import Camera
from sqlalchemy import select

async def main():
    async with db_helper.session_factory() as session:
        stmt = select(Camera)
        result = await session.execute(stmt)
        cameras = result.scalars().all()

    if not cameras:
        print("No cameras found in database.")
        return

    tasks = []
    print(f"Starting connection to {len(cameras)} cameras...")
    for cam in cameras:
        # Assuming username/password logic:
        # If camera has credentials in DB, use them. 
        # But connect.py logic in prev version used settings.hikvision.username 
        # if the dict relied on it. BUT Camera model has username/password cols.
        # We should use what is in the model.
        
        conn = HikiVisionConnection(
            device_ip=cam.device_ip,
            username=cam.username,
            password=cam.password,
            camera_type=cam.camera_type,
            camera_id=cam.id
        )
        tasks.append(asyncio.create_task(conn.stream_events()))
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())