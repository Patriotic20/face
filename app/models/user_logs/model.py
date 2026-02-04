from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime

from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.user.model import User

class UserLogs(Base):
    __tablename__ = "user_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    
    # Defaults to the current time when the row is created
    enter_time: Mapped[Optional[datetime]] 
    exit_time: Mapped[Optional[datetime]]

    # Relationship back to user
    user: Mapped["User"] = relationship(
        "User",
        back_populates="logs"
    )
    
    def __str__(self):
        return self.user.first_name