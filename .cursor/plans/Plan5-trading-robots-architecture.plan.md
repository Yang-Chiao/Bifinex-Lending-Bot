<!-- 76a17ffa-be37-4472-b601-1954698ec85b a0618a81-456f-4ec8-b09e-eeb062fc155c -->
# Plan 5: Website 產品官網

## 🎯 目標

建立產品宣傳網站，吸引用戶註冊並導向 Backstage 用戶後台。

## 📅 時程

**Week 2-3** - 預計 2-3 天完成（可與 Plan 4 並行）

## 📋 依賴關係

✅ 需要先完成：

- **Plan 1: 核心基礎設施**
- **Plan 2: Backend 架構**（至少 Auth API 完成）
- **Plan 3: UI 組件庫**

---

## 🏗️ 目錄結構

```
apps/website/
├── app/
│   ├── (marketing)/          # Marketing 頁面群組
│   │   ├── layout.tsx        # Marketing 布局
│   │   ├── page.tsx          # 首頁
│   │   ├── features/
│   │   │   └── page.tsx      # 功能介紹頁
│   │   ├── pricing/
│   │   │   └── page.tsx      # 定價頁面
│   │   └── about/
│   │       └── page.tsx      # 關於我們
│   │
│   ├── auth/                 # 認證頁面
│   │   ├── login/
│   │   │   └── page.tsx      # 登入頁
│   │   └── register/
│   │       └── page.tsx      # 註冊頁
│   │
│   ├── api/                  # API Routes
│   │   └── register/
│   │       └── route.ts      # 註冊 API 轉發
│   │
│   ├── components/           # 網站組件
│   │   ├── Hero.tsx
│   │   ├── Features.tsx
│   │   ├── CTA.tsx
│   │   ├── Testimonials.tsx
│   │   ├── PricingCards.tsx
│   │   ├── Footer.tsx
│   │   └── Navbar.tsx
│   │
│   ├── layout.tsx            # 根布局
│   ├── globals.css           # 全域樣式
│   └── not-found.tsx         # 404 頁面
│
├── public/
│   ├── favicon.ico
│   └── images/
│       └── hero-bg.jpg
│
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
├── package.json
└── README.md
```

---

## 📦 實作內容

### Task 5.1: 專案初始化

**5.1.1 package.json**

```json
{
  "name": "website",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "next": "^14.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.309.0",
    "@trading-robots/ui": "workspace:*",
    "@trading-robots/types": "workspace:*",
    "@trading-robots/config": "workspace:*"
  },
  "devDependencies": {
    "@types/node": "^20.11.5",
    "@types/react": "^18.2.48",
    "@types/react-dom": "^18.2.18",
    "autoprefixer": "^10.4.17",
    "postcss": "^8.4.33",
    "tailwindcss": "^3.4.1",
    "typescript": "^5.3.3"
  }
}
```

**5.1.2 next.config.js**

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ['@trading-robots/ui', '@trading-robots/types'],
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
}

module.exports = nextConfig
```

**5.1.3 tailwind.config.js**

```javascript
import baseConfig from '@trading-robots/config/tailwind'

export default {
  ...baseConfig,
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    '../../packages/ui/src/**/*.{js,ts,jsx,tsx}',
  ],
}
```

**5.1.4 tsconfig.json**

```json
{
  "extends": "@trading-robots/config/typescript/react",
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "module": "esnext",
    "jsx": "preserve",
    "plugins": [{ "name": "next" }],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./app/*"]
    },
    "incremental": true
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

---

### Task 5.2: 根布局與全域樣式

**5.2.1 app/layout.tsx**

```typescript
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Trading Robots - Automated Bitfinex Funding Bot',
  description: 'Maximize your crypto lending returns with our intelligent automated funding bot for Bitfinex',
  keywords: 'bitfinex, funding, lending, crypto, automated, bot',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
```

**5.2.2 app/globals.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --radius: 0.5rem;
}

@layer base {
  body {
    @apply bg-white text-gray-900;
  }
}
```

---

### Task 5.3: Marketing 頁面組件

**5.3.1 app/components/Navbar.tsx**

```typescript
import Link from 'next/link'
import { Button } from '@trading-robots/ui'

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="text-xl font-bold text-primary-600">
            Trading Robots
          </Link>
          
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/features" className="text-gray-700 hover:text-primary-600">
              Features
            </Link>
            <Link href="/pricing" className="text-gray-700 hover:text-primary-600">
              Pricing
            </Link>
            <Link href="/about" className="text-gray-700 hover:text-primary-600">
              About
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <Link href="/auth/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/auth/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
```

**5.3.2 app/components/Hero.tsx**

```typescript
import Link from 'next/link'
import { Button } from '@trading-robots/ui'
import { TrendingUp, Zap, Shield } from 'lucide-react'

export default function Hero() {
  return (
    <section className="pt-32 pb-20 px-4">
      <div className="max-w-7xl mx-auto text-center">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
          Automate Your Bitfinex
          <span className="text-primary-600"> Funding Strategy</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Maximize your passive income with our intelligent bot that automatically
          manages your funding offers 24/7 with optimized strategies.
        </p>
        <div className="flex justify-center gap-4">
          <Link href="/auth/register">
            <Button size="lg">
              Start Free Trial
            </Button>
          </Link>
          <Link href="/features">
            <Button size="lg" variant="outline">
              Learn More
            </Button>
          </Link>
        </div>

        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div className="flex flex-col items-center">
            <div className="bg-primary-100 p-4 rounded-full mb-4">
              <TrendingUp className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Smart Strategies</h3>
            <p className="text-gray-600 text-sm">
              AI-powered algorithms optimize your lending rates
            </p>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-primary-100 p-4 rounded-full mb-4">
              <Zap className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Fully Automated</h3>
            <p className="text-gray-600 text-sm">
              Set it and forget it - runs 24/7 automatically
            </p>
          </div>
          <div className="flex flex-col items-center">
            <div className="bg-primary-100 p-4 rounded-full mb-4">
              <Shield className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-lg font-semibold mb-2">Secure & Safe</h3>
            <p className="text-gray-600 text-sm">
              Your API keys are encrypted and never shared
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
```

**5.3.3 app/components/Features.tsx**

```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@trading-robots/ui'
import { 
  Target, 
  BarChart3, 
  Bell, 
  Lock, 
  Repeat, 
  Smartphone 
} from 'lucide-react'

const features = [
  {
    icon: Target,
    title: 'Multiple Strategies',
    description: 'Choose from market-following, ladder, or fixed-rate strategies',
  },
  {
    icon: BarChart3,
    title: 'Real-time Analytics',
    description: 'Track your earnings, performance, and lending history',
  },
  {
    icon: Bell,
    title: 'Smart Notifications',
    description: 'Get alerts via Telegram for important events',
  },
  {
    icon: Lock,
    title: 'Bank-level Security',
    description: 'Military-grade encryption for your API credentials',
  },
  {
    icon: Repeat,
    title: 'Auto-renewal',
    description: 'Automatically reinvest returned funds',
  },
  {
    icon: Smartphone,
    title: 'Mobile Ready',
    description: 'Manage your bot from anywhere, anytime',
  },
]

export default function Features() {
  return (
    <section className="py-20 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Everything You Need
          </h2>
          <p className="text-xl text-gray-600">
            Powerful features to maximize your lending returns
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
```

**5.3.4 app/components/PricingCards.tsx**

```typescript
import { Button, Card, CardContent, CardHeader, CardTitle, Badge } from '@trading-robots/ui'
import { Check } from 'lucide-react'

const plans = [
  {
    name: 'Starter',
    price: 'Free',
    description: 'Perfect for trying out',
    features: [
      'Up to $1,000 lending capital',
      '1 active strategy',
      'Basic analytics',
      'Email support',
    ],
  },
  {
    name: 'Pro',
    price: '$29',
    period: '/month',
    description: 'For serious lenders',
    popular: true,
    features: [
      'Unlimited lending capital',
      'Unlimited strategies',
      'Advanced analytics',
      'Priority support',
      'Telegram notifications',
      'Custom strategies',
    ],
  },
  {
    name: 'Enterprise',
    price: 'Custom',
    description: 'For institutions',
    features: [
      'Everything in Pro',
      'Dedicated account manager',
      'Custom integrations',
      'SLA guarantee',
      'White-label option',
    ],
  },
]

export default function PricingCards() {
  return (
    <section className="py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-xl text-gray-600">
            Choose the plan that fits your needs
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, index) => (
            <Card
              key={index}
              className={plan.popular ? 'border-primary-600 border-2 shadow-lg' : ''}
            >
              <CardHeader>
                {plan.popular && (
                  <Badge className="w-fit mb-2" variant="default">
                    Most Popular
                  </Badge>
                )}
                <CardTitle className="text-2xl">{plan.name}</CardTitle>
                <div className="mt-4">
                  <span className="text-4xl font-bold">{plan.price}</span>
                  {plan.period && (
                    <span className="text-gray-600">{plan.period}</span>
                  )}
                </div>
                <p className="text-gray-600 mt-2">{plan.description}</p>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3 mb-6">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-start">
                      <Check className="h-5 w-5 text-green-500 mr-2 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
                <Button
                  className="w-full"
                  variant={plan.popular ? 'default' : 'outline'}
                >
                  Get Started
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
```

**5.3.5 app/components/CTA.tsx**

```typescript
import Link from 'next/link'
import { Button } from '@trading-robots/ui'

export default function CTA() {
  return (
    <section className="py-20 px-4 bg-primary-600">
      <div className="max-w-4xl mx-auto text-center">
        <h2 className="text-4xl font-bold text-white mb-4">
          Ready to Start Earning?
        </h2>
        <p className="text-xl text-primary-100 mb-8">
          Join hundreds of users already maximizing their lending returns
        </p>
        <Link href="/auth/register">
          <Button size="lg" variant="outline" className="bg-white text-primary-600 hover:bg-gray-50">
            Start Free Trial Today
          </Button>
        </Link>
      </div>
    </section>
  )
}
```

**5.3.6 app/components/Footer.tsx**

```typescript
import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="text-white font-bold mb-4">Trading Robots</h3>
            <p className="text-sm">
              Automate your Bitfinex funding strategy and maximize returns.
            </p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Product</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/features">Features</Link></li>
              <li><Link href="/pricing">Pricing</Link></li>
              <li><Link href="/about">About</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/docs">Documentation</Link></li>
              <li><Link href="/contact">Contact</Link></li>
              <li><Link href="/faq">FAQ</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Legal</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/privacy">Privacy Policy</Link></li>
              <li><Link href="/terms">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 pt-8 text-sm text-center">
          © 2025 Trading Robots. All rights reserved.
        </div>
      </div>
    </footer>
  )
}
```

---

### Task 5.4: 頁面實作

**5.4.1 app/(marketing)/layout.tsx**

```typescript
import Navbar from '../components/Navbar'
import Footer from '../components/Footer'

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <Navbar />
      <main className="min-h-screen">
        {children}
      </main>
      <Footer />
    </>
  )
}
```

**5.4.2 app/(marketing)/page.tsx**（首頁）

```typescript
import Hero from '../components/Hero'
import Features from '../components/Features'
import CTA from '../components/CTA'

export default function HomePage() {
  return (
    <>
      <Hero />
      <Features />
      <CTA />
    </>
  )
}
```

**5.4.3 app/(marketing)/features/page.tsx**

```typescript
import Features from '@/components/Features'
import CTA from '@/components/CTA'

export default function FeaturesPage() {
  return (
    <div className="pt-20">
      <div className="max-w-4xl mx-auto text-center py-20 px-4">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Powerful Features for Smart Lending
        </h1>
        <p className="text-xl text-gray-600">
          Everything you need to automate and optimize your Bitfinex funding strategy
        </p>
      </div>
      <Features />
      <CTA />
    </div>
  )
}
```

**5.4.4 app/(marketing)/pricing/page.tsx**

```typescript
import PricingCards from '@/components/PricingCards'
import CTA from '@/components/CTA'

export default function PricingPage() {
  return (
    <div className="pt-20">
      <PricingCards />
      <CTA />
    </div>
  )
}
```

**5.4.5 app/(marketing)/about/page.tsx**

```typescript
export default function AboutPage() {
  return (
    <div className="pt-32 pb-20 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">About Us</h1>
        <div className="prose prose-lg">
          <p className="text-xl text-gray-600 mb-6">
            Trading Robots was born from our own frustration with manually managing
            Bitfinex funding offers.
          </p>
          <p className="text-gray-600 mb-4">
            We built this platform to help crypto holders maximize their passive income
            through intelligent automation and optimized lending strategies.
          </p>
          <p className="text-gray-600">
            Today, we serve hundreds of users managing millions in lending capital,
            helping them earn more while spending less time on manual operations.
          </p>
        </div>
      </div>
    </div>
  )
}
```

---

### Task 5.5: 認證頁面

**5.5.1 app/auth/register/page.tsx**

```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button, Card, CardContent, CardHeader, CardTitle, Input } from '@trading-robots/ui'

export default function RegisterPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || 'Registration failed')
      }

      // 註冊成功，導向 Backstage 登入
      router.push('http://localhost:5173/login?registered=true')
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-center text-2xl">Create Account</CardTitle>
          <p className="text-center text-gray-600 mt-2">
            Start your free trial today
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Password</label>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
              />
            </div>
            {error && <p className="text-sm text-red-600">{error}</p>}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Creating account...' : 'Create Account'}
            </Button>
          </form>
          <p className="text-center text-sm text-gray-600 mt-4">
            Already have an account?{' '}
            <Link href="/auth/login" className="text-primary-600 hover:underline">
              Login
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
```

**5.5.2 app/auth/login/page.tsx**

```typescript
export default function LoginPage() {
  // 直接導向 Backstage 登入頁
  if (typeof window !== 'undefined') {
    window.location.href = 'http://localhost:5173/login'
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p>Redirecting to login...</p>
    </div>
  )
}
```

---

### Task 5.6: API Routes

**5.6.1 app/api/auth/register/route.ts**

```typescript
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()

    // 轉發到 Backend
    const response = await fetch('http://localhost:8000/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    const data = await response.json()

    if (!response.ok) {
      return NextResponse.json(data, { status: response.status })
    }

    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

---

## ✅ 驗收標準

### 頁面完整性

- [ ] Landing Page 完整且美觀
- [ ] Features、Pricing、About 頁面實作完成
- [ ] 註冊頁面正常運作
- [ ] 登入頁面正確導向 Backstage

### SEO 優化

- [ ] 每個頁面有適當的 meta tags
- [ ] 語意化 HTML 標籤
- [ ] 圖片有 alt 文字
- [ ] 響應式設計

### UI/UX

- [ ] 使用共用 UI 組件庫
- [ ] 設計美觀現代
- [ ] 移動端友好
- [ ] Loading 和 Error 狀態處理

### 功能性

- [ ] 註冊成功後導向 Backstage
- [ ] API Route 正確轉發到 Backend
- [ ] 導航和連結正常運作

### 效能

- [ ] Next.js SSG/SSR 優化
- [ ] 圖片優化
- [ ] 快速載入時間

---

## 📚 後續優化（本次不實作）

- 添加 Blog 部分（MDX）
- 實作 Contact Form
- 添加客戶評價（Testimonials）
- Google Analytics 整合
- SEO 進階優化（sitemap、robots.txt）
- 國際化（i18n）

---

## 🔗 整合流程

Website → Backend → Backstage：

1. 用戶在 Website 註冊
2. Website API Route 轉發到 Backend
3. Backend 創建用戶
4. 用戶導向 Backstage 登入

---

## ⏱️ 預計時間

- Task 5.1-5.2: 1.5 小時（初始化和布局）
- Task 5.3: 3 小時（Marketing 組件）
- Task 5.4: 2 小時（頁面實作）
- Task 5.5: 1.5 小時（認證頁面）
- Task 5.6: 1 小時（API Routes）

**總計：約 9 小時（1.5-2 個工作日）**

### To-dos

- [ ] 初始化 Website 專案（Next.js, tailwind, tsconfig）
- [ ] 建立根布局和全域樣式
- [ ] 實作 Navbar 和 Footer 組件
- [ ] 實作 Hero 和 Features 組件
- [ ] 實作 PricingCards 和 CTA 組件
- [ ] 實作首頁 (Landing Page)
- [ ] 實作 Features、Pricing、About 頁面
- [ ] 實作 Register 和 Login 頁面
- [ ] 建立 API Routes（註冊轉發）
- [ ] 優化 SEO（metadata, sitemap）