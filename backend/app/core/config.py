from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/trading_robots"

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Encryption (for API keys)
    ENCRYPTION_KEY: str = "your-fernet-key-here"

    # Bitfinex (測試用)
    BITFINEX_API_URL: str = "https://api.bitfinex.com/v2"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    # App
    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
