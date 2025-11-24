# Code Review 檢查清單

本文檔提供 Code Review 時的檢查清單。

## 代碼風格

### Python 風格

- [ ] 使用 Black 格式化代碼
- [ ] 遵循 PEP 8 規範
- [ ] 函數和類別有清晰的文檔字串
- [ ] 變數命名清晰且有意義

### 檢查方式

```bash
# 使用 Black 檢查
black --check app/

# 使用 flake8 檢查
flake8 app/
```

## 類型一致性

### Schema 定義

- [ ] 所有 Schema 使用 camelCase（透過 alias）
- [ ] 添加 `🔗 對應 TypeScript` 註解
- [ ] 使用 `Field()` 設定驗證規則

**範例：**
```python
class UserResponse(BaseModel):
    """
    🔗 對應 TypeScript: User
    """
    createdAt: datetime = Field(..., alias="created_at")
    isActive: bool = Field(..., alias="is_active")
```

### API 響應格式

- [ ] 所有 API 使用 `ApiResponse<T>` 包裝
- [ ] 使用 `success_response()` 或 `error_response()` 便捷函數
- [ ] 錯誤響應包含 `code` 和 `message`

**範例：**
```python
# ✅ 正確
@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(...):
    return success_response(data=login_data)

# ❌ 錯誤
@router.post("/login")
def login(...):
    return {"access_token": token}  # 沒有包裝
```

## 功能性

### 業務邏輯

- [ ] Service 層實作正確
- [ ] 錯誤處理完整
- [ ] 邊界條件處理（空值、極值等）

### 資料庫操作

- [ ] 使用事務處理（commit/rollback）
- [ ] 避免 N+1 查詢問題
- [ ] 使用適當的索引

## 安全性

### 認證和授權

- [ ] 需要認證的 API 使用 `get_current_user` 依賴
- [ ] 密碼使用 bcrypt 雜湊
- [ ] API Key 加密存儲

### 輸入驗證

- [ ] 所有輸入都經過 Pydantic Schema 驗證
- [ ] 防止 SQL 注入（使用 ORM）
- [ ] 防止 XSS（FastAPI 自動處理）

## 效能

### 查詢優化

- [ ] 使用 `joinedload` 或 `selectinload` 避免 N+1
- [ ] 適當使用索引
- [ ] 分頁查詢（避免一次載入過多資料）

### 快取

- [ ] 考慮是否需要快取（Redis）
- [ ] Token 驗證結果可快取

## Git 提交規範

### 提交訊息格式

```
<type>: <subject>

<body>
```

**類型：**
- `feat:` 新功能
- `fix:` 修復 bug
- `docs:` 文檔更新
- `refactor:` 重構
- `test:` 測試相關
- `chore:` 構建/工具相關

**範例：**
```
feat: add strategy API endpoints

- Add POST /api/strategies endpoint
- Add GET /api/strategies endpoint
- Add tests for strategy API
```

### 分支命名

- `feature/` 新功能
- `fix/` 修復 bug
- `docs/` 文檔更新

## 測試

### 測試覆蓋率

- [ ] 新功能有對應的測試
- [ ] 測試驗證響應格式（ApiResponse + camelCase）
- [ ] 測試邊界條件和錯誤情況

### 測試品質

- [ ] 測試名稱清晰描述測試內容
- [ ] 測試獨立（不依賴其他測試）
- [ ] 使用 fixture 減少重複代碼

## 文檔

### 代碼註解

- [ ] 函數有文檔字串
- [ ] 複雜邏輯有註解說明
- [ ] Schema 有類型對照註解

### 文檔更新

- [ ] 新 API 更新 API_DESIGN.md（如需要）
- [ ] 新類型更新 TYPE_MAPPING.md（如需要）
- [ ] README 更新（如需要）

## Code Review 流程

1. **創建 PR**：確保分支名稱和提交訊息符合規範
2. **自動檢查**：CI/CD 運行測試和 linting
3. **人工 Review**：使用本檢查清單
4. **修改和重新提交**：根據反饋修改
5. **合併**：通過後合併到主分支

## 常見問題

### Q: Schema 應該使用 snake_case 還是 camelCase？

**A:** Schema 欄位名稱使用 camelCase（透過 alias），對應前端 TypeScript 類型。

### Q: 什麼時候應該返回錯誤響應而不是拋出異常？

**A:** 業務邏輯錯誤使用 `error_response()`，系統錯誤（如資料庫連接失敗）拋出異常。

### Q: 如何確保類型一致性？

**A:** 
1. 參考 `TYPE_MAPPING.md`
2. 檢查 TypeScript 類型定義
3. 運行測試驗證響應格式

## 參考資源

- [類型對照](./TYPE_MAPPING.md)
- [API 設計規範](./API_DESIGN.md)
- [開發指南](./DEVELOPMENT.md)

