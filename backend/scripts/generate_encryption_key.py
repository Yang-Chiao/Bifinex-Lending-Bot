#!/usr/bin/env python3
"""
生成用於加密 API Key 的 Fernet Key
"""
from cryptography.fernet import Fernet

if __name__ == "__main__":
    key = Fernet.generate_key()
    print("=" * 50)
    print("生成的加密 Key（複製到 .env 文件的 ENCRYPTION_KEY）:")
    print("=" * 50)
    print(key.decode())
    print("=" * 50)
