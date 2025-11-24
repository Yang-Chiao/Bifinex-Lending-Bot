from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # 資料庫配置
    DATABASE_URL: str = "postgresql://user:password@localhost/bitfinex_lending"
    
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # API Key 加密用的 Key（必須是 32 bytes base64）
    ENCRYPTION_KEY: str = "your-32-byte-base64-encryption-key"
    
    # Bitfinex API 配置
    BITFINEX_API_URL: str = "https://api.bitfinex.com/v2"
    BITFINEX_API_VERSION: str = "v2"
    
    # CORS 配置
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # 應用配置
    PROJECT_NAME: str = "Bitfinex Lending Bot"
    API_V1_STR: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
