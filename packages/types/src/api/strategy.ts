import { Strategy, StrategyParams, StrategyType } from '../entities/strategy'
import { PaginatedResponse } from '../common/pagination'

export interface CreateStrategyRequest {
  strategyType: StrategyType
  params: StrategyParams
  isActive?: boolean
}

export interface UpdateStrategyRequest {
  params?: StrategyParams
  isActive?: boolean
}

export type StrategyListResponse = PaginatedResponse<Strategy>

