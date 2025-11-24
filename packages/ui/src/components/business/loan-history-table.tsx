import type { Loan } from '@trading-robots/types'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../ui/table'
import { Badge } from '../ui/badge'
import { formatCurrency, formatPercent, formatDate } from '@/lib/utils'

export interface LoanHistoryTableProps {
  loans: Loan[]
}

export function LoanHistoryTable({ loans }: LoanHistoryTableProps) {
  const getStatusVariant = (status: Loan['status']) => {
    switch (status) {
      case 'active':
        return 'success'
      case 'completed':
        return 'default'
      case 'cancelled':
        return 'danger'
      default:
        return 'outline'
    }
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Amount</TableHead>
          <TableHead>Rate</TableHead>
          <TableHead>Period</TableHead>
          <TableHead>Earnings</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Date</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {loans.map((loan) => (
          <TableRow key={loan.id}>
            <TableCell className="font-medium">
              {formatCurrency(loan.amount)}
            </TableCell>
            <TableCell>{formatPercent(loan.rate)}</TableCell>
            <TableCell>
              {formatDate(loan.startDate)} - {formatDate(loan.endDate)}
            </TableCell>
            <TableCell className="text-green-600 font-medium">
              {formatCurrency(loan.earnings)}
            </TableCell>
            <TableCell>
              <Badge variant={getStatusVariant(loan.status)}>
                {loan.status}
              </Badge>
            </TableCell>
            <TableCell className="text-gray-500 text-sm">
              {formatDate(loan.createdAt)}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}

