import { User } from '../entities/user'

/**
 * 登入請求
 */
export interface LoginRequest {
  email: string
  password: string
}

/**
 * 登入響應
 */
export interface LoginResponse {
  accessToken: string
  refreshToken: string
  user: User
}

/**
 * 註冊請求
 */
export interface RegisterRequest {
  email: string
  password: string
  confirmPassword: string
}

