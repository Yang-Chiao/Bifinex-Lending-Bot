# @trading-robots/config

共用配置包，提供 TypeScript、Tailwind、ESLint 和 Prettier 的統一配置。

## 使用方式

### TypeScript 配置

```json
{
  "extends": "@trading-robots/config/typescript/base"
}
```

或 React 專案：

```json
{
  "extends": "@trading-robots/config/typescript/react"
}
```

### Tailwind 配置

```javascript
import baseConfig from '@trading-robots/config/tailwind'

export default {
  ...baseConfig,
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
}
```

### ESLint 配置

```javascript
import baseConfig from '@trading-robots/config/eslint/base'

export default {
  ...baseConfig,
  // 專案特定規則
}
```

### Prettier 配置

```javascript
import prettierConfig from '@trading-robots/config/prettier'

export default prettierConfig
```

