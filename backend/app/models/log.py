"""
Log Model

用於記錄系統操作日誌
"""

from sqlalchemy import Column, String, Text, Enum, ForeignKey
import enum
from app.models.base import BaseModel

class LogLevel(str, enum.Enum):
    """日誌級別"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"

class Log(BaseModel):
    """
    日誌實體
    
    用於記錄系統操作、錯誤等
    """
    __tablename__ = "logs"
    
    user_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    level = Column(Enum(LogLevel), nullable=False)
    message = Column(Text, nullable=False)
    details = Column(Text, nullable=True)  # JSON 字串

