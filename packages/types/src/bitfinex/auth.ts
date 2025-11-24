/**
 * Bitfinex API 認證相關類型
 */

/**
 * Bitfinex API 認證標頭
 */
export interface BitfinexAuthHeaders {
  'bfx-apikey': string
  'bfx-signature': string
  'bfx-nonce': string
}

/**
 * Bitfinex API Key 權限
 */
export interface BitfinexApiKeyPermissions {
  account: boolean           // 帳戶資訊
  orders: boolean           // 訂單管理
  funding: boolean          // 資金管理
  settings: boolean         // 設定
  wallets: boolean          // 錢包操作
}

/**
 * Bitfinex 錯誤回應
 * [ERROR_CODE, "error", ERROR_MESSAGE]
 */
export type BitfinexErrorResponse = [
  string,      // 0: ERROR - 通常是 "error"
  number,      // 1: CODE - 錯誤代碼
  string       // 2: MESSAGE - 錯誤訊息
]

/**
 * Bitfinex 成功通知
 * [MTS, TYPE, MESSAGE_ID, null, NOTIFY_INFO, CODE, STATUS, TEXT]
 */
export type BitfinexNotification = [
  number,      // 0: MTS - 時間戳
  string,      // 1: TYPE - 通知類型（如 'on-req', 'oc-req'）
  number,      // 2: MESSAGE_ID
  null,        // 3: placeholder
  any[],       // 4: NOTIFY_INFO - 通知詳情
  number,      // 5: CODE - 狀態碼
  string,      // 6: STATUS - 狀態（SUCCESS/ERROR/FAILURE）
  string       // 7: TEXT - 文字訊息
]

/**
 * Bitfinex Rate Limit 資訊
 */
export interface BitfinexRateLimitInfo {
  'x-ratelimit-limit': number        // 速率限制
  'x-ratelimit-remaining': number    // 剩餘請求數
  'x-ratelimit-reset': number        // 重置時間（Unix timestamp）
}

