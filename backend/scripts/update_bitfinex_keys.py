"""更新指定用戶的 Bitfinex API Key / Secret

用法（在 backend 目錄下執行）：

    python scripts/update_bitfinex_keys.py <email> <api_key> <api_secret>

注意：請不要把你的 API Key / Secret 貼到聊天視窗，只在本機終端機輸入。
"""

import sys

from app.core.database import SessionLocal
from app.core.security import encrypt_api_key
from app.models.user import User


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: python scripts/update_bitfinex_keys.py <email> <api_key> <api_secret>")
        sys.exit(1)

    email = sys.argv[1]
    api_key = sys.argv[2]
    api_secret = sys.argv[3]

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"❌ User not found: {email}")
            sys.exit(1)

        print(f"🔄 Updating Bitfinex credentials for user: {email}")
        user.bitfinex_api_key = encrypt_api_key(api_key)
        user.bitfinex_api_secret = encrypt_api_key(api_secret)

        db.commit()
        print("✅ Bitfinex API Key / Secret updated successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    main()


