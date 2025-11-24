export type LoanStatus = 
  | 'active'      // 進行中
  | 'completed'   // 已完成
  | 'cancelled'   // 已取消

export interface Loan {
  id: string
  userId: string
  offerId: string              // 關聯的掛單 ID
  bitfinexLoanId: number       // Bitfinex 上的成交 ID
  amount: number
  rate: number
  startDate: string            // 開始日期
  endDate: string             // 結束日期
  earnings: number            // 收益
  status: LoanStatus
  createdAt: string
}