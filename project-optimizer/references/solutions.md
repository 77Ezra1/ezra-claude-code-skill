# Solution Examples

This reference contains concrete solution examples for common frontend issues found during testing.

## Performance Solutions

### Large Bundle Size

**Problem**: JavaScript bundle > 500KB

**Solutions**:

1. **Code Splitting** (Effort: M)
```typescript
// Before: Everything imported at top
import { Chart, Table, Form } from './components';

// After: Lazy load components
const Chart = lazy(() => import('./components/Chart'));
const Table = lazy(() => import('./components/Table'));

// Use Suspense boundary
<Suspense fallback={<Spinner />}>
  <Chart />
</Suspense>
```

2. **Tree Shaking** (Effort: S)
```json
// package.json - use ES modules
{
  "type": "module",
  "sideEffects": false
}
```

3. **Replace heavy libraries** (Effort: L)
```bash
# Replace Moment.js (67KB) with date-fns (tree-shakeable)
npm uninstall moment
npm install date-fns
```

### Slow Initial Load

**Problem**: LCP > 2.5s

**Solutions**:

1. **Image Optimization** (Effort: S)
```typescript
// Use next/image or responsive images
import Image from 'next/image';

<Image
  src="/hero.jpg"
  width={1920}
  height={1080}
  priority // For above-fold images
  placeholder="blur"
/>
```

2. **Critical CSS Inlining** (Effort: M)
Extract and inline critical CSS for above-fold content.

3. **Preload Critical Resources** (Effort: XS)
```html
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/styles.css" as="style">
```

### Unnecessary Re-renders

**Problem**: Components re-render unnecessarily

**Solution**:
```typescript
// Use React.memo for expensive components
export const ExpensiveList = React.memo(({ items }) => {
  // ...
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.items.length === nextProps.items.length;
});

// Use useMemo for expensive calculations
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// Use useCallback for stable function references
const handleClick = useCallback((id) => {
  // ...
}, [dependency]);
```

## Accessibility Solutions

### Missing ARIA Labels

**Problem**: Interactive elements lack accessible names

**Solution**:
```typescript
// Before
<button onClick={handleMenu}>
  <IconMenu />
</button>

// After
<button onClick={handleMenu} aria-label="Open menu">
  <IconMenu aria-hidden="true" />
</button>

// For icon buttons with visible text
<button onClick={handleMenu}>
  <IconMenu aria-hidden="true" />
  <span>Menu</span>
</button>
```

### Keyboard Navigation Issues

**Problem**: Custom components don't work with keyboard

**Solution**:
```typescript
// Make custom dropdown keyboard accessible
const Dropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        setIsOpen(!isOpen);
        break;
      case 'Escape':
        setIsOpen(false);
        buttonRef.current?.focus();
        break;
    }
  };

  return (
    <>
      <button
        ref={buttonRef}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        Options
      </button>
      {isOpen && (
        <ul role="menu" autoFocus>
          {/* Menu items */}
        </ul>
      )}
    </>
  );
};
```

### Form Validation Without Announcements

**Problem**: Screen readers don't announce errors

**Solution**:
```typescript
const FormField = ({ error, label, ...props }) => (
  <div>
    <label htmlFor={props.id}>{label}</label>
    <input
      {...props}
      aria-invalid={!!error}
      aria-describedby={error ? `${props.id}-error` : undefined}
    />
    {error && (
      <span id={`${props.id}-error`} role="alert" aria-live="polite">
        {error}
      </span>
    )}
  </div>
);
```

## UI/UX Solutions

### Mobile Layout Issues

**Problem**: Content overflows on small screens

**Solution**:
```css
/* Use proper responsive breakpoints */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Mobile-first approach */
.card {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .card {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .card {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Touch Target Too Small

**Problem**: Buttons/links are hard to tap on mobile

**Solution**:
```css
/* Minimum touch target: 44x44px */
.button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}

/* For small icons, add padding */
.icon-button {
  padding: 10px;
}
```

### Inconsistent Spacing

**Problem**: Inconsistent margins and padding

**Solution**:
```typescript
// Use a design system approach
const spacing = {
  xs: '0.25rem',   // 4px
  sm: '0.5rem',    // 8px
  md: '1rem',      // 16px
  lg: '1.5rem',    // 24px
  xl: '2rem',      // 32px
  '2xl': '3rem',   // 48px
};

// Apply consistently
const styles = {
  section: css`
    padding: ${spacing.lg} ${spacing.md};
    margin-bottom: ${spacing.xl};
  `,
};
```

## Security Solutions

### XSS Vulnerabilities

**Problem**: Unsafe HTML rendering

**Solution**:
```typescript
// DON'T - dangerouslySetInnerHTML with user input
<div dangerouslySetInnerHTML={{ __html: userInput }} />

// DO - Sanitize or use text content
import DOMPurify from 'dompurify';

<div
  dangerouslySetInnerHTML={{
    __html: DOMPurify.sanitize(userInput)
  }}
/>
```

### Sensitive Data in URLs

**Problem**: API tokens or sensitive data in query params

**Solution**:
```typescript
// DON'T
fetch(`/api/data?token=${apiToken}`);

// DO - Use headers
fetch('/api/data', {
  headers: {
    Authorization: `Bearer ${apiToken}`
  }
});

// Store securely
import { secureStorage } from './utils/secureStorage';
secureStorage.setItem('token', apiToken);
```

## Code Quality Solutions

### TypeScript Errors

**Problem**: `any` types or missing types

**Solution**:
```typescript
// DON'T
function processData(data: any) {
  return data.map((item: any) => item.value);
}

// DO - Define proper types
interface DataItem {
  id: string;
  value: number;
  timestamp: Date;
}

function processData(data: DataItem[]): number[] {
  return data.map(item => item.value);
}
```

### Missing Error Boundaries

**Problem**: Unhandled errors crash the app

**Solution**:
```typescript
class ErrorBoundary extends React.Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
    // Log to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

### Console Errors

**Problem**: Unhandled promise rejections

**Solution**:
```typescript
// Add global error handler
window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled promise rejection:', event.reason);
  event.preventDefault();
});

// Use proper error handling
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    // Handle error appropriately
    handleError(error);
    throw error; // Re-throw if needed
  }
}
```
