# CSS Variables Reference

Complete list of DocPilot CSS variables for quick reference.

---

## Color Variables

### Primary Colors
```css
var(--color-primary)           /* #000000 (light), #FFFFFF (dark) */
var(--color-primary-hover)     /* #333333 (light), #EEEEEE (dark) */
var(--color-primary-active)    /* #111111 (light), #DDDDDD (dark) */
```

### Text Colors
```css
var(--color-text-primary)      /* #111111 (light), #FFFFFF (dark) */
var(--color-text-secondary)    /* #666666 (light), #A3A3A3 (dark) */
var(--color-text-tertiary)     /* #999999 (light), #737373 (dark) */
var(--color-text-quaternary)   /* #CCCCCC (light), #525252 (dark) */
var(--color-text-inverse)      /* #FFFFFF (light), #000000 (dark) */
```

### Background Colors
```css
var(--color-bg-primary)        /* #FFFFFF (light), #0A0A0A (dark) */
var(--color-bg-secondary)      /* #FAFAFA (light), #171717 (dark) */
var(--color-bg-tertiary)       /* #F5F5F5 (light), #1F1F1F (dark) */
var(--color-bg-elevated)       /* #FFFFFF (light), #262626 (dark) */
var(--color-bg-overlay)        /* rgba(0,0,0,0.5) (light), rgba(0,0,0,0.7) (dark) */
```

### Border Colors
```css
var(--color-border)            /* #E5E5E5 (light), #262626 (dark) */
var(--color-border-strong)     /* #D4D4D4 (light), #404040 (dark) */
var(--color-divider)           /* #EEEEEE (light), #333333 (dark) */
```

### Status Colors
```css
var(--color-success)           /* #22C55E */
var(--color-success-bg)        /* #F0FDF4 */
var(--color-warning)           /* #F59E0B */
var(--color-warning-bg)        /* #FFFBEB */
var(--color-error)             /* #EF4444 */
var(--color-error-bg)          /* #FEF2F2 */
var(--color-info)              /* #3B82F6 */
var(--color-info-bg)           /* #EFF6FF */
```

---

## Border Radius

```css
var(--radius-xs)        /* 4px */
var(--radius-sm)        /* 6px */
var(--radius-md)        /* 8px */
var(--radius-lg)        /* 12px - Buttons, Inputs */
var(--radius-xl)        /* 16px - Cards */
var(--radius-2xl)       /* 20px - Modals */
var(--radius-capsule)   /* 9999px - Pill buttons */
```

---

## Spacing

```css
var(--spacing-xs)       /* 4px */
var(--spacing-sm)       /* 8px */
var(--spacing-md)       /* 12px */
var(--spacing-lg)       /* 16px */
var(--spacing-xl)       /* 24px */
var(--spacing-2xl)      /* 32px */
var(--spacing-3xl)      /* 48px */
```

---

## Shadows

```css
var(--shadow-xs)   /* 0 1px 2px rgba(0, 0, 0, 0.05) */
var(--shadow-sm)   /* 0 1px 3px rgba(0, 0, 0, 0.08) */
var(--shadow-md)   /* 0 4px 6px -1px rgba(0, 0, 0, 0.08) */
var(--shadow-lg)   /* 0 10px 15px -3px rgba(0, 0, 0, 0.08) */
var(--shadow-xl)   /* 0 20px 25px -5px rgba(0, 0, 0, 0.08) */
```

---

## Transitions

```css
var(--transition-fast)    /* 150ms */
var(--transition-normal)  /* 200ms */
var(--transition-slow)    /* 300ms */
```

---

## Typography

```css
var(--font-sans)   /* -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif */
var(--font-mono)   /* 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace */
```

---

## Layout

```css
var(--sidebar-width)       /* 260px */
var(--header-height)       /* 56px */
var(--content-max-width)   /* 1200px */
```

---

## Usage Examples

### Button
```scss
.myButton {
  background: var(--color-primary);
  color: var(--color-text-inverse);
  border-radius: var(--radius-lg);
  padding: 0 var(--spacing-lg);
  height: 40px;
  transition: all var(--transition-fast);

  &:hover {
    background: var(--color-primary-hover);
  }
}
```

### Card
```scss
.myCard {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
}
```

### Text
```scss
.title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.description {
  font-size: 14px;
  color: var(--color-text-secondary);
}
```

### Input
```scss
.myInput {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--color-text-primary);

  &:focus {
    border-color: var(--color-border-strong);
  }
}
```

---

## Breakpoints (from breakpoints.scss)

```scss
// Use in SCSS
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

Breakpoint values:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px
