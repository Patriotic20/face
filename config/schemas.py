from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    user_id: str | None = None
    time: datetime
    camera_type: str
    ip_address: str | None = None

class EnterEvent(BaseModel):
    user_id: str | None = None
    enter_time: datetime

class ExitEvent(BaseModel):
    user_id: str | None = None
    exit_time: datetime