/**
 * Bitfinex Funding Ticker（資金市場行情）
 * GET /v2/ticker/fSYMBOL （如 /v2/ticker/fUSD）
 * 回應格式：陣列 [FRR, BID, BID_PERIOD, BID_SIZE, ASK, ASK_PERIOD, ASK_SIZE, ...]
 */
export type BitfinexFundingTicker = [
  number,      // 0: FRR - Flash Return Rate（閃電回報率）
  number,      // 1: BID - 最高借出利率（年化）
  number,      // 2: BID_PERIOD - 最高借出期限（天）
  number,      // 3: BID_SIZE - 最高借出總額
  number,      // 4: ASK - 最低借入利率（年化）
  number,      // 5: ASK_PERIOD - 最低借入期限（天）
  number,      // 6: ASK_SIZE - 最低借入總額
  number,      // 7: DAILY_CHANGE - 日變化
  number,      // 8: DAILY_CHANGE_RELATIVE - 日變化百分比
  number,      // 9: LAST_PRICE - 最後成交價
  number,      // 10: VOLUME - 成交量
  number,      // 11: HIGH - 最高價
  number,      // 12: LOW - 最低價
  number,      // 13: placeholder
  number,      // 14: placeholder
  number,      // 15: FRR_AMOUNT_AVAILABLE - FRR 可用金額
]

/**
 * Bitfinex Funding Ticker 物件格式（便於使用）
 */
export interface BitfinexFundingTickerObject {
  symbol: string
  frr: number                    // Flash Return Rate（閃電回報率）
  bid: number                    // 最高借出利率
  bidPeriod: number              // 最高借出期限
  bidSize: number                // 最高借出總額
  ask: number                    // 最低借入利率
  askPeriod: number              // 最低借入期限
  askSize: number                // 最低借入總額
  dailyChange: number            // 日變化
  dailyChangeRelative: number    // 日變化百分比
  lastPrice: number              // 最後成交價
  volume: number                 // 成交量
  high: number                   // 最高價
  low: number                    // 最低價
  frrAmountAvailable: number     // FRR 可用金額
}

/**
 * Bitfinex Funding Book（資金訂單簿）
 * GET /v2/book/fSYMBOL/P0?len=25
 * 回應：陣列的陣列 [[RATE, PERIOD, COUNT, AMOUNT], ...]
 */
export type BitfinexFundingBookEntry = [
  number,      // 0: RATE - 利率（日利率，需乘以 365 得年化）
  number,      // 1: PERIOD - 期限（天）
  number,      // 2: COUNT - 該價位的訂單數
  number       // 3: AMOUNT - 總金額（正數=放貸，負數=借入）
]

/**
 * Bitfinex Funding Book 回應
 */
export type BitfinexFundingBook = BitfinexFundingBookEntry[]

/**
 * Bitfinex Funding Book 物件格式（便於使用）
 */
export interface BitfinexFundingBookEntryObject {
  rate: number         // 日利率
  period: number       // 期限（天）
  count: number        // 訂單數量
  amount: number       // 總金額
}

/**
 * Bitfinex Funding Stats
 * GET /v2/stats1/{Key}:{Size}:{Symbol}:{Section}/hist
 */
export type BitfinexFundingStats = [
  number,      // 0: MTS - 時間戳
  number       // 1: VALUE - 統計值
]
