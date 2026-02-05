from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from ..base import Base
import httpx
import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.user_logs.model import UserLogs

logger = logging.getLogger(__name__)

class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_ip: Mapped[str] = mapped_column(String(50), nullable=False, default="192.168.88.101")
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    camera_type: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=False)

    logs: Mapped[list["UserLogs"]] = relationship("UserLogs", back_populates="camera")

    async def check_connection(self) -> bool:
        """
        Checks connection to the camera.
        """
        url = f"http://{self.device_ip}/ISAPI/System/deviceInfo"
        auth = httpx.DigestAuth(self.username, self.password)
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url, auth=auth)
                if response.status_code == 200:
                    return True
                else:
                    logger.warning(f"Connection failed with status: {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Connection check error: {e}")
            return False

    def __str__(self):
        return f"{self.device_ip} ({self.camera_type})"
