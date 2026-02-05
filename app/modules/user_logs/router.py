from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_helper import db_helper
from .repository import get_user_logs_repository
from .schemas import UserLogsRead, UserListRequest


router = APIRouter(
    prefix="/logs",
    tags=["User Logs"]
)

@router.get("/", response_model=list[UserLogsRead])
async def get_logs(
    data: UserListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_user_logs_repository.get_user_logs_list(session, data)

@router.websocket("/ws")
async def websocket_logs(websocket: WebSocket):
    await get_user_logs_repository.websocket_logs(websocket)

