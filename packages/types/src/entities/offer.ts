export type OfferStatus = 
  | 'active'      // 活躍中
  | 'executed'    // 已成交
  | 'cancelled'   // 已取消
  | 'expired'     // 已過期

export interface Offer {
  id: string
  userId: string
  bitfinexOfferId: number  // Bitfinex 上的掛單 ID
  amount: number           // 金額
  rate: number            // 年化利率（小數，如 0.05 = 5%）
  duration: number        // 天數
  status: OfferStatus
  createdAt: string
  updatedAt: string
}