from app.models.user.model import User
from app.models.camera.model import Camera
from app.models.user_logs.model import UserLogs
from config.db_helper import db_helper
from config.schemas import Event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta, datetime



async def save_log(event: Event):
    async with db_helper.session_factory() as session:
        if event.camera_type in ["enter", "exit"]:
            return await handle_user_log(session, event)
        return False


async def get_camera_by_ip(session: AsyncSession, ip_address: str | None) -> Camera | None:
    if not ip_address:
         return None
    stmt = select(Camera).where(Camera.device_ip == ip_address)
    result = await session.execute(stmt)
    return result.scalars().first()


async def handle_user_log(session: AsyncSession, event: Event):
    camera = await get_camera_by_ip(session, event.ip_address)
    
    if not camera:
        # Fallback or error if camera not found. 
        # Since camera_id is required, we might skip or log error.
        # But per requirements we need to correct code. 
        # Making assumption: if no camera, we can't save legally if FK is strict.
        # Let's try to proceed? No, that will raise DB error.
        print(f"Camera with ip {event.ip_address} not found. Cannot save log.")
        return False

    stmt = (
        select(UserLogs)
        .where(UserLogs.user_id == int(event.user_id))
        .order_by(UserLogs.enter_time.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    user_log_data = result.scalars().first()

    if event.camera_type == "enter":
         # Logic for create new or verify duplicate
         # Check if recent entry exists
         if user_log_data and user_log_data.exit_time is None:
              # Active session exists.
              if user_log_data.enter_time + timedelta(minutes=10) > event.time:
                   # Too soon, ignore
                   return False
              
              # Otherwise, maybe close old one? Or just create new one?
              # Simplest: create new one if the old one is "stale" or force close it?
              # Original code:
              # if user_log_data.exit_time is not None: create new
              # if active session...
              
              # Let's stick to: Create new if no active session or active session is old.
              pass

         new_log = UserLogs(
            user_id=int(event.user_id),
            enter_time=event.time,
            camera_id=camera.id
         )
         session.add(new_log)
         await session.commit()
         return True
    
    elif event.camera_type == "exit":
        if user_log_data and user_log_data.exit_time is None:
            user_log_data.exit_time = event.time
            # user_log_data.camera_id = camera.id # Optional: update camera on exit? usually enter camera matters or both. 
            # But we only have one camera_id column. It's usually 'enter_camera_id'. 
            # If we want exit camera, we'd need exit_camera_id.
            # So just update time.
            await session.commit()
            return True
        else:
             # No active session to exit.
             return False
    
    return False



