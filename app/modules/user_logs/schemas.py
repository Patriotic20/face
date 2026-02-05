from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserLogsRead(BaseModel):
    id: int
    user_id: int
    camera_id: int
    enter_time: Optional[datetime]
    exit_time: Optional[datetime]

class UserListRequest(BaseModel):
    page: int = 1
    limit: int = 10

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit

class UserListResponse(BaseModel):
    total: int
    page: int
    limit: int
    logs: list[UserLogsRead]