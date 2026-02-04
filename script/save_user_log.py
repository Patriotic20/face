from app.models.user.model import User
from app.models.user_logs.model import UserLogs
from config.db_helper import db_helper
from config.schemas import Event
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta, datetime



async def save_log(event: Event):
    async with db_helper.session_getter() as session:
        if event.camera_type == "enter":
            return await create_user_log(session, event)
        elif event.camera_type == "exit":
            return await update_user_log(session, event)
        return False


async def create_user_log(session: AsyncSession, event: Event):
    stmt = (
        select(UserLogs)
        .where(UserLogs.user_id == int(event.user_id))
        .order_by(UserLogs.enter_time.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    user_log_data = result.scalars().first()

    # If no log exists or the last log has an exit_time or is too old, create new
    if not user_log_data or user_log_data.exit_time is not None:
        new_log = UserLogs(
            user_id=int(event.user_id),
            enter_time=event.time
        )
        session.add(new_log)
        await session.commit()
        return True

    # Logic for duplicate entry checks (10 mins etc) could go here if needed
    # For now, if active session exists (no exit_time), we check if it is old?
    # Keeping it simple based on request: create if enter
    
    # If active session exists, maybe we update enter_time if it's recent? 
    # Or strict create? 
    # "create if enter"
    
    # The user provided code had logic about 10 minutes and dates. 
    # Re-implementing simplified logic or preserving relevant parts:
    
    if user_log_data.enter_time + timedelta(minutes=10) < event.time:
         new_log = UserLogs(
            user_id=int(event.user_id),
            enter_time=event.time
        )
         session.add(new_log)
         await session.commit()
         return True
    
    # Same day check
    if user_log_data.enter_time.date() < event.time.date():
         new_log = UserLogs(
            user_id=int(event.user_id),
            enter_time=event.time
        )
         session.add(new_log)
         await session.commit()
         return True

    return False


async def update_user_log(session: AsyncSession, event: Event):
    stmt = (
        select(UserLogs)
        .where(UserLogs.user_id == int(event.user_id))
        .order_by(UserLogs.enter_time.desc())
        .limit(1)
    )
    result = await session.execute(stmt)
    user_log_data = result.scalars().first()

    if not user_log_data:
        return False
    
    # If already exited, cannot exit again? Or update exit time?
    # "create if enter, if exit update_userlog"
    # Assuming update the latest active log.
    
    if user_log_data.exit_time is not None:
         # No active session to close.
         # Maybe create a new one with exit time? Or ignore?
         # User instructions implied simple update.
         return False
    
    user_log_data.exit_time = event.time
    await session.commit()
    return True