"""
Auth API 測試

驗證 API 響應格式符合 @trading-robots/types 定義
"""

import pytest
from fastapi.testclient import TestClient

def test_register(client: TestClient):
    """測試註冊 - 驗證統一響應格式"""
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "confirmPassword": "testpass123"  # 包含 confirmPassword
        }
    )
    assert response.status_code == 200
    
    # 驗證統一響應格式
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert "message" in data
    
    # 驗證 User 數據格式（camelCase）
    user = data["data"]
    assert "id" in user
    assert "email" in user
    assert "role" in user
    assert "createdAt" in user  # camelCase
    assert "updatedAt" in user  # camelCase
    assert "isActive" in user   # camelCase

def test_login(client: TestClient):
    """測試登入 - 驗證 LoginResponse 格式"""
    # 先註冊
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "pass123456",
            "confirmPassword": "pass123456"
        }
    )
    
    # 登入
    response = client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "pass123456"}
    )
    assert response.status_code == 200
    
    # 驗證統一響應格式
    data = response.json()
    assert data["success"] is True
    
    # 驗證 LoginResponse 格式
    login_data = data["data"]
    assert "accessToken" in login_data   # camelCase
    assert "refreshToken" in login_data  # camelCase（與 Plan 1 一致）
    assert "user" in login_data
    
    # 驗證 User 格式
    user = login_data["user"]
    assert "createdAt" in user
    assert "isActive" in user

def test_register_duplicate_email(client: TestClient):
    """測試重複註冊 - 驗證錯誤響應格式"""
    email = "duplicate@example.com"
    
    # 第一次註冊
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "pass123", "confirmPassword": "pass123"}
    )
    
    # 第二次註冊（應該失敗）
    response = client.post(
        "/api/auth/register",
        json={"email": email, "password": "pass123", "confirmPassword": "pass123"}
    )
    
    # 驗證錯誤響應格式
    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert "code" in data["error"]
    assert "message" in data["error"]

