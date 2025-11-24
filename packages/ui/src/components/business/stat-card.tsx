import * as React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { cn, formatCurrency, formatPercent } from '@/lib/utils'
import { TrendingUp, TrendingDown } from 'lucide-react'

export interface StatCardProps {
  title: string
  value: number
  format?: 'currency' | 'percent' | 'number'
  change?: number // 變化百分比
  icon?: React.ReactNode
  className?: string
}

export function StatCard({
  title,
  value,
  format = 'number',
  change,
  icon,
  className,
}: StatCardProps) {
  const formatValue = () => {
    switch (format) {
      case 'currency':
        return formatCurrency(value)
      case 'percent':
        return formatPercent(value)
      default:
        return value.toLocaleString()
    }
  }

  const isPositive = change !== undefined && change >= 0

  return (
    <Card className={cn('', className)}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-600">
          {title}
        </CardTitle>
        {icon && <div className="text-gray-400">{icon}</div>}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formatValue()}</div>
        {change !== undefined && (
          <div
            className={cn(
              'flex items-center text-xs mt-1',
              isPositive ? 'text-green-600' : 'text-red-600'
            )}
          >
            {isPositive ? (
              <TrendingUp className="h-3 w-3 mr-1" />
            ) : (
              <TrendingDown className="h-3 w-3 mr-1" />
            )}
            <span>
              {isPositive ? '+' : ''}
              {formatPercent(Math.abs(change), 1)} from last period
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  )
}


