// 策略類型
export type StrategyType = 
  | 'market_follow'  // 跟隨市場利率
  | 'ladder'         // 階梯式
  | 'fixed_rate'     // 固定利率

export interface Strategy {
  id: string
  userId: string
  strategyType: StrategyType
  params: StrategyParams      // 根據類型不同而不同
  isActive: boolean
  createdAt: string
  updatedAt: string
}

// 策略參數（聯合類型，根據 strategyType 決定）
export type StrategyParams = 
  | MarketFollowParams
  | LadderParams
  | FixedRateParams

// 跟隨市場利率策略參數
export interface MarketFollowParams {
  rateMultiplier: number  // 0.95 = 市場利率的 95%
  minRate: number         // 最低利率
  maxRate: number         // 最高利率
  duration: number        // 天數
}

// 階梯式策略參數
export interface LadderParams {
  levels: {
    amount: number        // 金額
    rate: number          // 利率
    duration: number      // 天數
  }[]
}

// 固定利率策略參數
export interface FixedRateParams {
  rate: number
  duration: number
}