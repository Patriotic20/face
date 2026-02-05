from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime
from app.models.user_log.model import UserLogs
from .schemas import UserListRequest
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
from config.db_helper import db_helper


class UserLogsRepository:


    async def user_logs_list(self, session: AsyncSession, data: UserListRequest) -> list[UserLogs]:
        stmt = (
            select(UserLogs)
            .limit(data.limit)
            .offset(data.offset)
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_latest(self, session: AsyncSession, after_time: datetime) -> list[UserLogs]:
        stmt = select(UserLogs).where(
            (UserLogs.enter_time > after_time) | ((UserLogs.exit_time != None) & (UserLogs.exit_time > after_time))
        ).order_by(desc(UserLogs.enter_time))
        result = await session.execute(stmt)
        return result.scalars().all()


    async def websocket_logs(self, websocket: WebSocket) -> list[UserLogs]:
        await websocket.accept()
        last_check_time = datetime.now()
        try:
            while True:
                async with db_helper.session_factory() as session:
                    new_logs = await self.get_latest(session, last_check_time)
                    if new_logs:
                        last_check_time = datetime.now()
                        data = [
                            UserLogsRead.model_validate(log).model_dump(mode='json') 
                            for log in new_logs
                        ]
                        await websocket.send_json(data)
                await asyncio.sleep(2)
        except WebSocketDisconnect:
            print("WebSocket disconnected")
        except Exception as e:
            print(f"WebSocket error: {e}")
            try:
                await websocket.close()
            except:
                pass



get_user_logs_repository = UserLogsRepository()

