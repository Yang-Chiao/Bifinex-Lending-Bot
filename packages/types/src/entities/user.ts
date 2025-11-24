/**
 * 用戶實體
 */
export interface User {
  id: string
  email: string
  role: UserRole
  createdAt: string
  updatedAt: string
  isActive: boolean
}

export type UserRole = 'admin' | 'user'

export interface UserProfile extends User {
  hasBitfinexApiKey: boolean
  strategiesCount: number
  totalEarnings: number
}

