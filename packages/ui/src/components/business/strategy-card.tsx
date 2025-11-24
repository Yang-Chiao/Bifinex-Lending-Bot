import type { Strategy } from '@trading-robots/types'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Badge } from '../ui/badge'
import { Button } from '../ui/button'
import { formatDate } from '@/lib/utils'

export interface StrategyCardProps {
  strategy: Strategy
  onEdit?: (id: string) => void
  onToggle?: (id: string, isActive: boolean) => void
}

export function StrategyCard({ strategy, onEdit, onToggle }: StrategyCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="text-lg">{strategy.strategyType}</CardTitle>
        <Badge variant={strategy.isActive ? 'success' : 'default'}>
          {strategy.isActive ? 'Active' : 'Inactive'}
        </Badge>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Created:</span>
            <span>{formatDate(strategy.createdAt)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Updated:</span>
            <span>{formatDate(strategy.updatedAt)}</span>
          </div>
        </div>
        <div className="flex gap-2 mt-4">
          {onEdit && (
            <Button variant="outline" size="sm" onClick={() => onEdit(strategy.id)}>
              Edit
            </Button>
          )}
          {onToggle && (
            <Button
              variant={strategy.isActive ? 'destructive' : 'default'}
              size="sm"
              onClick={() => onToggle(strategy.id, !strategy.isActive)}
            >
              {strategy.isActive ? 'Disable' : 'Enable'}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

