---
name: ui-optimizer
description: Frontend UI optimization specialist for DocPilot project. Uses the project's design system: Notion-style + black/white/gray + iOS capsule rounded corners. NO emojis. Uses SVG icons for products/services. Use when user requests: (1) UI optimization, (2) Component creation, (3) Style improvements, (4) Integration UI design, (5) Responsive design fixes 当用户提到「优化前端UI" / "优化界面" / "美化界面、改进UI" / "UI优化" / "界面优化、优化样式" / "修改样式" / "调整样式、这个页面需要优化" / "页面美化、UI优化建议" / "界面改进建议、optimize UI" / "improve interface、UI设计优化" / "界面设计、创建组件" / "新建组件" / "设计组件、做个xxx组件" / "实现xxxUI、帮我设计xxx" / "实现xxx界面、创建xxx页面" / "做xxx页面、create component" / "design UI、新建页面" / "页面开发、集成notion" / "集成github" / "集成slack、notion集成界面" / "github连接页面」等关键词时触发。
user-invocable: true
---



# UI Optimizer

Frontend UI optimization specialist for DocPilot project. Follows the project's design system strictly.

## Design Philosophy

**"Notion-style + Black/White/Gray + iOS Capsule Rounded Corners"**

Minimalist, professional, and elegant visual experience.

---

## Color System

### Primary Colors (Light Mode)
```css
--color-primary: #000000;          /* Pure black */
--color-primary-hover: #333333;
--color-primary-active: #111111;
```

### Text Colors
```css
--color-text-primary: #111111;     /* Main text */
--color-text-secondary: #666666;   /* Secondary text */
--color-text-tertiary: #999999;    /* Helper text */
--color-text-quaternary: #CCCCCC;  /* Placeholder text */
```

### Background Colors
```css
--color-bg-primary: #FFFFFF;       /* Main background */
--color-bg-secondary: #FAFAFA;     /* Secondary background */
--color-bg-tertiary: #F5F5F5;      /* Tertiary background */
```

### Border Colors
```css
--color-border: #E5E5E5;           /* Main border */
--color-border-strong: #D4D4D4;    /* Strong border */
--color-divider: #EEEEEE;          /* Divider */
```

### Status Colors
```css
--color-success: #22C55E;          /* Green */
--color-warning: #F59E0B;          /* Orange */
--color-error: #EF4444;            /* Red */
--color-info: #3B82F6;             /* Blue */
```

### Dark Mode (data-theme="dark")
```css
--color-primary: #FFFFFF;
--color-text-primary: #FFFFFF;
--color-bg-primary: #0A0A0A;
--color-border: #262626;
```

---

## Border Radius (iOS Capsule Style)

```css
--radius-xs: 4px;
--radius-sm: 6px;
--radius-md: 8px;
--radius-lg: 12px;      /* Most buttons */
--radius-xl: 16px;      /* Cards */
--radius-2xl: 20px;     /* Modals */
--radius-capsule: 9999px; /* Pill buttons */
```

---

## Spacing System

```css
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 12px;
--spacing-lg: 16px;
--spacing-xl: 24px;
--spacing-2xl: 32px;
--spacing-3xl: 48px;
```

---

## Typography

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
font-size: 14px;
line-height: 1.5;
```

### Font Weights
- Regular: 400
- Medium: 500
- Semibold: 600

### Heading Sizes
- Page title: 32px / 600
- Section title: 24px / 600 or 20px / 600
- Card title: 16px / 500 or 14px / 500

---

## Shadows (Subtle)

```css
--shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
--shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.08);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.08);
```

---

## Transitions

```css
--transition-fast: 150ms;
--transition-normal: 200ms;
--transition-slow: 300ms;
```

---

## Component Patterns

### Button (Primary)
```tsx
<button className="ant-btn-primary">
  Button Text
</button>
```

Style:
```css
background: var(--color-primary);
border-radius: var(--radius-lg); /* 12px */
height: 40px;
padding: 0 20px;
font-weight: 500;
```

### Button (Secondary)
```tsx
<button className="ant-btn-default">
  Button Text
</button>
```

### Input Field
```tsx
<input className="ant-input" placeholder="Placeholder..." />
```

Style:
```css
border-radius: var(--radius-lg); /* 12px */
border-color: var(--color-border);
padding: 8px 14px;
```

### Card
```tsx
<div className="ant-card">
  <div className="ant-card-body">Content</div>
</div>
```

Style:
```css
border-radius: var(--radius-xl); /* 16px */
border-color: var(--color-border);
box-shadow: none;
```

---

## SVG Icons for Products/Services

**CRITICAL: Always use SVG icons for product integrations.**

### Common Product SVG Icons

#### Notion
```tsx
<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
  <path d="M4.459 4.208c.746.606 1.026.56 2.428.466l10.74-.746c1.527-.14 1.863.236 1.863 1.522v12.527c0 1.266-.28 1.809-1.604 1.928l-11.586.746c-1.024.093-1.454-.14-1.926-1.125V6.486l-.06-.626L4.46 4.208z" fill="currentColor"/>
  <path d="M15.458 5.503l-1.49-1.49v8.715l1.49.094V5.503z" fill="#fff"/>
  <path d="M11.035 4.628l-1.776-.23v9.06l1.776.14v-8.97z" fill="#fff"/>
  <path d="M6.367 4.441l-1.637.23v8.348l1.637.28V4.441z" fill="#fff"/>
  <path d="M14.962 14.48l1.49-.094v2.414l-1.49.23v-2.55z" fill="#fff"/>
  <path d="M10.259 14.62l1.776-.14v2.667l-1.776.28v-2.807z" fill="#fff"/>
  <path d="M5.73 14.9l1.637-.28v2.9l-1.637.328V14.9z" fill="#fff"/>
</svg>
```

#### GitHub
```tsx
<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
</svg>
```

#### Slack
```tsx
<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
  <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.522 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.522 2.521 2.528 2.528 0 0 1-2.522 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.522h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.522 2.527 2.527 0 0 1-2.52-2.522V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312zM15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z" fill="currentColor"/>
</svg>
```

#### Google Drive
```tsx
<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
  <path d="M7.71 3.5L1.15 15l4.58 7.5h13.54l4.58-7.5L17.29 3.5H7.71z" fill="currentColor" opacity="0.2"/>
  <path d="M7.71 3.5l-3.04 5.28L12.5 22h4.79l3.04-5.28L12.5 3.5H7.71z" fill="currentColor"/>
  <path d="M1.15 15l3.04 5.28h8.31l-3.04-5.28H1.15z" fill="currentColor"/>
</svg>
```

#### Linear
```tsx
<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
</svg>
```

#### Figma
```tsx
<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
  <path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z" fill="currentColor"/>
  <path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z" fill="currentColor"/>
  <path d="M12 12a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z" fill="currentColor"/>
  <path d="M8.5 9.5A3.5 3.5 0 0 0 5 13a3.5 3.5 0 0 0 3.5 3.5H12v-7H8.5z" fill="currentColor"/>
  <path d="M8.5 9.5A3.5 3.5 0 0 0 5 13a3.5 3.5 0 0 0 3.5 3.5H12v-7H8.5z" fill="currentColor" opacity="0.5"/>
</svg>
```

### Custom SVG Icon Component
```tsx
interface ProductIconProps {
  name: 'notion' | 'github' | 'slack' | 'google-drive' | 'linear' | 'figma';
  size?: number;
  className?: string;
}

const productIcons = {
  notion: (size: number) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
      {/* Notion SVG path */}
    </svg>
  ),
  // ... other icons
};

export const ProductIcon: React.FC<ProductIconProps> = ({ name, size = 16, className }) => {
  return (
    <span className={className} style={{ display: 'inline-flex', alignItems: 'center' }}>
      {productIcons[name](size)}
    </span>
  );
};
```

---

## Ant Design Icons

For non-product icons, use `@ant-design/icons`:

```tsx
import {
  HomeOutlined,
  FileTextOutlined,
  FolderOutlined,
  SettingOutlined,
  PlusOutlined,
  SearchOutlined,
  MoreOutlined,
  EditOutlined,
  DeleteOutlined,
  CheckOutlined,
  CloseOutlined,
  ArrowLeftOutlined,
  ArrowRightOutlined,
  DownloadOutlined,
  UploadOutlined,
  LinkOutlined,
  UserOutlined,
  TeamOutlined,
} from '@ant-design/icons';
```

---

## SCSS Module Pattern

```scss
// ComponentName.module.scss
.container {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  background: var(--color-bg-primary);
  border-radius: var(--radius-xl);
  border: 1px solid var(--color-border);
  transition: all var(--transition-fast);

  &:hover {
    border-color: var(--color-border-strong);
    box-shadow: var(--shadow-sm);
  }
}

.title {
  font-size: 16px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.description {
  font-size: 14px;
  color: var(--color-text-secondary);
}
```

---

## Component Template

```tsx
// ComponentName.tsx
import React from 'react';
import styles from './ComponentName.module.scss';

interface ComponentNameProps {
  title: string;
  description?: string;
  onClick?: () => void;
}

export const ComponentName: React.FC<ComponentNameProps> = ({
  title,
  description,
  onClick,
}) => {
  return (
    <div className={styles.container} onClick={onClick}>
      <h3 className={styles.title}>{title}</h3>
      {description && <p className={styles.description}>{description}</p>}
    </div>
  );
};
```

---

## Responsive Design

```scss
// Use breakpoints from styles/breakpoints.scss
@use '../../styles/breakpoints' as bp;

.container {
  padding: var(--spacing-lg);

  @include bp.md {
    padding: var(--spacing-xl);
  }

  @include bp.lg {
    padding: var(--spacing-2xl);
  }
}
```

Breakpoints:
- sm: 640px
- md: 768px
- lg: 1024px
- xl: 1280px
- 2xl: 1536px

---

## Important Rules

### 1. NO Emojis
Never use emojis in UI. Always use text labels or SVG icons.

### 2. Use Product SVG Icons
When integrating with external services (Notion, GitHub, Slack, etc.), use their official SVG icons.

### 3. Follow Design System
Always use CSS variables for colors, spacing, and border radius.

### 4. Consistent Naming
- Use PascalCase for components
- Use camelCase for props and functions
- Use kebab-case for SCSS classes

### 5. Accessibility
- Add proper ARIA labels for icon-only buttons
- Ensure sufficient color contrast (4.5:1 minimum)
- Support keyboard navigation

### 6. Dark Mode Support
Use semantic color variables that automatically adapt to dark mode.

---

## File Structure

```
frontend/src/
├── components/
│   ├── ComponentName/
│   │   ├── ComponentName.tsx
│   │   ├── ComponentName.module.scss
│   │   └── index.ts
├── styles/
│   ├── variables.css
│   ├── globals.css
│   └── breakpoints.scss
└── pages/
    └── pageName/
        ├── PageName.tsx
        ├── PageName.module.scss
        └── index.ts
```
