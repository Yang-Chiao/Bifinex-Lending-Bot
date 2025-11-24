/**
 * 錢包類型
 */
export type WalletType = 
  | 'exchange'   // 現貨錢包
  | 'margin'     // 保證金錢包
  | 'funding'    // 資金錢包

/**
 * Bitfinex Wallet 回應（陣列格式）
 * GET /v2/auth/r/wallets
 * 回應：陣列的陣列 [[WALLET_TYPE, CURRENCY, BALANCE, UNSETTLED_INTEREST, BALANCE_AVAILABLE], ...]
 */
export type BitfinexWalletResponse = [
  WalletType,  // 0: WALLET_TYPE - 錢包類型
  string,      // 1: CURRENCY - 幣種（如 'USD', 'BTC'）
  number,      // 2: BALANCE - 總餘額
  number,      // 3: UNSETTLED_INTEREST - 未結算利息
  number,      // 4: BALANCE_AVAILABLE - 可用餘額
  ...any[]     // 其他欄位
]

/**
 * Bitfinex Wallets 回應（多個錢包）
 */
export type BitfinexWalletsResponse = BitfinexWalletResponse[]

/**
 * Bitfinex Wallet 物件格式（便於使用）
 */
export interface BitfinexWallet {
  type: WalletType
  currency: string              // 幣種（如 'USD'）
  balance: number               // 總餘額
  unsettledInterest: number    // 未結算利息
  available: number             // 可用餘額
}

/**
 * Bitfinex Wallet Balance 更新通知（WebSocket）
 * 通過 WebSocket 接收的錢包餘額更新
 */
export interface BitfinexWalletUpdate {
  wallets: BitfinexWallet[]
}

/**
 * Bitfinex Wallet Transfer 請求
 * POST /v2/auth/w/transfer
 */
export interface BitfinexWalletTransferRequest {
  from: WalletType      // 源錢包
  to: WalletType        // 目標錢包
  currency: string      // 幣種
  amount: string        // 金額（字串格式）
}

/**
 * Bitfinex Wallet Transfer 回應
 */
export type BitfinexWalletTransferResponse = [
  number,      // 0: MTS - 時間戳
  string,      // 1: TYPE - 類型
  string,      // 2: MESSAGE - 訊息
  any,         // 3: placeholder
  [            // 4: WALLET SNAPSHOT - 錢包快照
    BitfinexWalletResponse,
    BitfinexWalletResponse
  ]
]
