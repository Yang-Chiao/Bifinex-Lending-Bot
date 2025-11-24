import { cn, formatPercent } from '@/lib/utils'

export interface RateDisplayProps {
  rate: number
  label?: string
  size?: 'sm' | 'md' | 'lg'
  showTrend?: boolean
  trend?: 'up' | 'down' | 'neutral'
  className?: string
}

export function RateDisplay({
  rate,
  label,
  size = 'md',
  showTrend = false,
  trend = 'neutral',
  className,
}: RateDisplayProps) {
  const sizeClasses = {
    sm: 'text-lg',
    md: 'text-2xl',
    lg: 'text-4xl',
  }

  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-900',
  }

  return (
    <div className={cn('flex flex-col', className)}>
      {label && (
        <span className="text-sm text-gray-600 mb-1">{label}</span>
      )}
      <span
        className={cn(
          'font-bold',
          sizeClasses[size],
          showTrend && trendColors[trend]
        )}
      >
        {formatPercent(rate)} APR
      </span>
    </div>
  )
}

