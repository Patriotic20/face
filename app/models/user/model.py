from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from typing import Optional, List, TYPE_CHECKING
from ..base import Base


if TYPE_CHECKING:
    from app.modules.user_logs.model import UserLogs

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(50)) 
    image_path: Mapped[Optional[str]] = mapped_column(String(255))
    passport_serial: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    status: Mapped[bool] = mapped_column(Boolean, default=None, nullable=True)

    # Relationship to logs
    logs: Mapped[List["UserLogs"]] = relationship(
        "UserLogs",
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    
    
    def __str__(self):
        return self.first_name