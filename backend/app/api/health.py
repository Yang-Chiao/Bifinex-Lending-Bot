"""
Health Check API

簡單的健康檢查端點
"""

from fastapi import APIRouter
from app.schemas.common import ApiResponse, success_response

router = APIRouter()

@router.get("/health", response_model=ApiResponse[dict])
def health_check():
    """
    健康檢查端點
    
    對應 TypeScript API：GET /api/health
    """
    return success_response(
        data={"status": "healthy"},
        message="Service is running"
    )

