"""初始化資料庫"""
from app.core.database import engine
from app.models.base import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized")

if __name__ == "__main__":
    init_db()

