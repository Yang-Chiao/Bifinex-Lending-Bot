/**
 * Bitfinex Funding Offer 提交請求
 * POST /v2/auth/w/funding/offer/submit
 */
export interface BitfinexSubmitFundingOfferRequest {
  type: 'LIMIT' | 'FRRDELTAVAR'  // LIMIT=固定利率, FRRDELTAVAR=FRR動態利率
  symbol: string                  // 如 'fUSD'
  amount: string                  // 金額（字串格式）
  rate: string                    // 利率（字串格式，如 '0.0365' 表示 3.65% 年化）
  period: number                  // 期限（天數，2-120）
  flags?: number                  // 可選標記
}

/**
 * Bitfinex Funding Offer 回應（陣列格式）
 * Response: [ID, SYMBOL, MTS_CREATED, MTS_UPDATED, AMOUNT, AMOUNT_ORIG, TYPE, ..., FLAGS, STATUS, ...]
 */
export type BitfinexFundingOfferResponse = [
  number,      // 0: ID - Offer ID
  string,      // 1: SYMBOL - 如 'fUSD'
  number,      // 2: MTS_CREATED - 建立時間戳（毫秒）
  number,      // 3: MTS_UPDATED - 更新時間戳（毫秒）
  number,      // 4: AMOUNT - 當前金額
  number,      // 5: AMOUNT_ORIG - 原始金額
  string,      // 6: TYPE - 訂單類型
  number,      // 7: placeholder
  number,      // 8: placeholder
  number,      // 9: FLAGS - 標記
  string,      // 10: STATUS - 狀態（如 'ACTIVE', 'EXECUTED', 'PARTIALLY FILLED', 'CANCELED'）
  ...any[]     // 其他欄位
]

/**
 * Bitfinex Funding Credits（活躍放貸）
 * 陣列格式：[ID, SYMBOL, SIDE, MTS_CREATE, MTS_UPDATE, AMOUNT, FLAGS, STATUS, ...]
 */
export type BitfinexFundingCreditResponse = [
  number,      // 0: ID
  string,      // 1: SYMBOL
  number,      // 2: SIDE - 1=提供資金
  number,      // 3: MTS_CREATE
  number,      // 4: MTS_UPDATE
  number,      // 5: AMOUNT
  number,      // 6: FLAGS
  string,      // 7: STATUS
  ...any[]
]

/**
 * Bitfinex Funding Loans（活躍借貸）
 * 陣列格式
 */
export type BitfinexFundingLoanResponse = [
  number,      // 0: ID
  string,      // 1: SYMBOL
  number,      // 2: SIDE - -1=借入資金
  number,      // 3: MTS_CREATE
  number,      // 4: MTS_UPDATE
  number,      // 5: AMOUNT
  number,      // 6: FLAGS
  string,      // 7: STATUS
  ...any[]
]

/**
 * 取消 Funding Offer 請求
 * POST /v2/auth/w/funding/offer/cancel
 */
export interface BitfinexCancelFundingOfferRequest {
  id: number   // Offer ID
}
