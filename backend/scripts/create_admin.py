"""創建管理員用戶"""
from app.core.database import SessionLocal
from app.services.auth import create_user
from app.models.user import UserRole

def create_admin(email: str, password: str):
    db = SessionLocal()
    try:
        user = create_user(db, email, password)
        user.role = UserRole.ADMIN
        db.commit()
        print(f"✅ Admin user created: {email}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <email> <password>")
        sys.exit(1)
    create_admin(sys.argv[1], sys.argv[2])

