import {
  Button,
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  Input,
  Badge,
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  StatCard,
  StrategyCard,
  LoanHistoryTable,
  RateDisplay,
} from '../src'
import type { Strategy, Loan } from '@trading-robots/types'
import { DollarSign, TrendingUp, Activity } from 'lucide-react'

// Mock data
const mockStrategy: Strategy = {
  id: '1',
  userId: 'user1',
  strategyType: 'market-follow',
  isActive: true,
  params: {
    minRate: 0.01,
    maxRate: 0.1,
    amount: 1000,
  },
  createdAt: '2024-01-15T10:30:00Z',
  updatedAt: '2024-03-20T14:20:00Z',
}

const mockLoans: Loan[] = [
  {
    id: '1',
    userId: 'user1',
    offerId: 'offer1',
    amount: 1000,
    currency: 'USD',
    rate: 0.0365,
    period: 7,
    startDate: '2024-03-01',
    endDate: '2024-03-08',
    earnings: 7.15,
    status: 'completed',
    createdAt: '2024-03-01T09:00:00Z',
    updatedAt: '2024-03-08T09:00:00Z',
  },
  {
    id: '2',
    userId: 'user1',
    offerId: 'offer2',
    amount: 2000,
    currency: 'USD',
    rate: 0.042,
    period: 14,
    startDate: '2024-03-10',
    endDate: '2024-03-24',
    earnings: 32.27,
    status: 'active',
    createdAt: '2024-03-10T10:30:00Z',
    updatedAt: '2024-03-10T10:30:00Z',
  },
]

function App() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold">Trading Robots UI Components</h1>
          <p className="text-gray-600">
            所有組件的視覺展示 - @trading-robots/ui
          </p>
        </div>

        {/* Buttons */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Buttons</h2>
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-wrap gap-4">
                <Button variant="default">Default</Button>
                <Button variant="destructive">Destructive</Button>
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
                <Button variant="link">Link</Button>
              </div>
              <div className="flex flex-wrap gap-4 mt-4">
                <Button size="sm">Small</Button>
                <Button size="default">Default</Button>
                <Button size="lg">Large</Button>
                <Button size="icon">
                  <TrendingUp className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Badges */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Badges</h2>
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-wrap gap-4">
                <Badge variant="default">Default</Badge>
                <Badge variant="success">Success</Badge>
                <Badge variant="warning">Warning</Badge>
                <Badge variant="danger">Danger</Badge>
                <Badge variant="outline">Outline</Badge>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Input */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Input</h2>
          <Card>
            <CardContent className="pt-6 space-y-4">
              <Input placeholder="Enter text..." />
              <Input type="email" placeholder="Email address" />
              <Input type="number" placeholder="Amount" />
              <Input disabled placeholder="Disabled input" />
            </CardContent>
          </Card>
        </section>

        {/* Card */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Card</h2>
          <Card>
            <CardHeader>
              <CardTitle>Card Title</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                This is a card component with header and content. You can add any
                content here.
              </p>
            </CardContent>
          </Card>
        </section>

        {/* Dialog */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Dialog</h2>
          <Card>
            <CardContent className="pt-6">
              <Dialog>
                <DialogTrigger asChild>
                  <Button>Open Dialog</Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Dialog Title</DialogTitle>
                  </DialogHeader>
                  <p className="text-gray-600">
                    This is a dialog component. It can be used for modals,
                    confirmations, or forms.
                  </p>
                  <div className="flex justify-end gap-2 mt-4">
                    <Button variant="outline">Cancel</Button>
                    <Button>Confirm</Button>
                  </div>
                </DialogContent>
              </Dialog>
            </CardContent>
          </Card>
        </section>

        {/* StatCard */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">StatCard (業務組件)</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <StatCard
              title="Total Earnings"
              value={1234.56}
              format="currency"
              change={0.15}
              icon={<DollarSign className="h-4 w-4" />}
            />
            <StatCard
              title="Average Rate"
              value={0.0365}
              format="percent"
              change={-0.05}
              icon={<TrendingUp className="h-4 w-4" />}
            />
            <StatCard
              title="Active Loans"
              value={12}
              format="number"
              icon={<Activity className="h-4 w-4" />}
            />
          </div>
        </section>

        {/* RateDisplay */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">RateDisplay (業務組件)</h2>
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-wrap gap-8">
                <RateDisplay rate={0.0365} label="Small" size="sm" />
                <RateDisplay
                  rate={0.0365}
                  label="Medium"
                  size="md"
                  showTrend
                  trend="up"
                />
                <RateDisplay
                  rate={0.0245}
                  label="Large"
                  size="lg"
                  showTrend
                  trend="down"
                />
              </div>
            </CardContent>
          </Card>
        </section>

        {/* StrategyCard */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">StrategyCard (業務組件)</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <StrategyCard
              strategy={mockStrategy}
              onEdit={(id) => alert(`Edit strategy: ${id}`)}
              onToggle={(id, isActive) =>
                alert(`Toggle strategy: ${id} to ${isActive}`)
              }
            />
            <StrategyCard
              strategy={{ ...mockStrategy, id: '2', isActive: false }}
              onEdit={(id) => alert(`Edit strategy: ${id}`)}
              onToggle={(id, isActive) =>
                alert(`Toggle strategy: ${id} to ${isActive}`)
              }
            />
          </div>
        </section>

        {/* LoanHistoryTable */}
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">LoanHistoryTable (業務組件)</h2>
          <Card>
            <CardContent className="pt-6">
              <LoanHistoryTable loans={mockLoans} />
            </CardContent>
          </Card>
        </section>

        {/* Footer */}
        <div className="text-center text-gray-500 py-8">
          <p>@trading-robots/ui - Plan 3 完成 ✅</p>
        </div>
      </div>
    </div>
  )
}

export default App

