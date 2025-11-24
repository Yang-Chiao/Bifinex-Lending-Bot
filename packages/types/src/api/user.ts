import { User, UserProfile } from '../entities/user'

/**
 * 更新用戶請求
 */
export interface UpdateUserRequest {
  email?: string
  isActive?: boolean
}

/**
 * 用戶列表響應
 */
export interface UserListResponse {
  users: User[]
  total: number
}

/**
 * 用戶詳情響應
 */
export interface UserDetailResponse {
  user: UserProfile
}

