import { Offer, OfferStatus } from '../entities/offer'
import { PaginatedResponse } from '../common/pagination'

/**
 * 創建掛單請求
 */
export interface CreateOfferRequest {
  amount: number
  rate: number
  duration: number
}

/**
 * 更新掛單請求
 */
export interface UpdateOfferRequest {
  status?: OfferStatus
}

/**
 * 掛單列表響應
 */
export type OfferListResponse = PaginatedResponse<Offer>

