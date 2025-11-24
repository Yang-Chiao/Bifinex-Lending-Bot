"""
SQLAlchemy Base Model

所有模型的基礎類別，提供共用欄位。
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class BaseModel(Base):
    """
    抽象基礎模型
    
    提供共用欄位：id, created_at, updated_at
    對應 TypeScript 中所有 Entity 的共同欄位
    """
    __abstract__ = True
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

