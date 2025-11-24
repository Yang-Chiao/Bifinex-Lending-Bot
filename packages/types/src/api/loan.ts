import { Loan, LoanStatus } from '../entities/loan'
import { PaginatedResponse } from '../common/pagination'

/**
 * 成交記錄列表響應
 */
export type LoanListResponse = PaginatedResponse<Loan>

/**
 * 成交記錄查詢參數
 */
export interface LoanQueryParams {
  status?: LoanStatus
  startDate?: string
  endDate?: string
}

