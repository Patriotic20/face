import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import settings
from script.connect import HikiVisionConnection

CAMERAS = [
    {
        "device_ip": "192.168.88.101",
        "username": settings.hikvision.username,
        "password": settings.hikvision.password,
        "camera_type": "enter"
    },
    {
        "device_ip": "192.168.88.102",
        "username": settings.hikvision.username,
        "password": settings.hikvision.password,
        "camera_type": "exit"
    },
    {
        "device_ip": "192.168.88.103",
        "username": settings.hikvision.username,
        "password": settings.hikvision.password,
        "camera_type": "enter"
    },
    {
        "device_ip": "192.168.88.104",
        "username": settings.hikvision.username,
        "password": settings.hikvision.password,
        "camera_type": "exit"
    },
    {
        "device_ip": "192.168.88.105",
        "username": settings.hikvision.username,
        "password": settings.hikvision.password,
        "camera_type": "enter"
    },
    {
        "device_ip": "192.168.88.106",
        "username": settings.hikvision.username,
        "password": settings.hikvision.password,
        "camera_type": "exit"
    }
]

async def main():
    tasks = []
    print(f"Starting connection to {len(CAMERAS)} cameras...")
    for cam_conf in CAMERAS:
        conn = HikiVisionConnection(
            device_ip=cam_conf["device_ip"],
            username=cam_conf["username"],
            password=cam_conf["password"],
            camera_type=cam_conf["camera_type"]
        )
        tasks.append(asyncio.create_task(conn.stream_events()))
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())