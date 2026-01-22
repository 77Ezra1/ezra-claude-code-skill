# Component Templates

Standardized component templates following DocPilot design system.

---

## Card Component

```tsx
// Card.tsx
import React from 'react';
import styles from './Card.module.scss';

interface CardProps {
  title: string;
  description?: string;
  icon?: React.ReactNode;
  action?: React.ReactNode;
  onClick?: () => void;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  title,
  description,
  icon,
  action,
  onClick,
  className = '',
}) => {
  return (
    <div className={`${styles.card} ${className} ${onClick ? styles.clickable : ''}`} onClick={onClick}>
      <div className={styles.header}>
        {icon && <div className={styles.icon}>{icon}</div>}
        <div className={styles.content}>
          <h3 className={styles.title}>{title}</h3>
          {description && <p className={styles.description}>{description}</p>}
        </div>
        {action && <div className={styles.action}>{action}</div>}
      </div>
    </div>
  );
};
```

```scss
// Card.module.scss
.card {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--spacing-lg);
  transition: all var(--transition-fast);

  &.clickable {
    cursor: pointer;

    &:hover {
      border-color: var(--color-border-strong);
      box-shadow: var(--shadow-sm);
    }
  }
}

.header {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
}

.content {
  flex: 1;
  min-width: 0;
}

.title {
  font-size: 16px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.description {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.5;
}

.action {
  flex-shrink: 0;
}
```

---

## Button Component

```tsx
// Button.tsx
import React from 'react';
import styles from './Button.module.scss';

type ButtonVariant = 'primary' | 'secondary' | 'ghost';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
  icon?: React.ReactNode;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  loading = false,
  icon,
  children,
  className = '',
  disabled,
  ...props
}) => {
  return (
    <button
      className={`${styles.button} ${styles[variant]} ${styles[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span className={styles.spinner} />}
      {icon && <span className={styles.icon}>{icon}</span>}
      <span>{children}</span>
    </button>
  );
};
```

```scss
// Button.module.scss
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  font-family: inherit;
  font-weight: 500;
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;

  &:disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }
}

.primary {
  background: var(--color-primary);
  color: var(--color-text-inverse);

  &:hover:not(:disabled) {
    background: var(--color-primary-hover);
  }

  &:active:not(:disabled) {
    background: var(--color-primary-active);
  }
}

.secondary {
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);

  &:hover:not(:disabled) {
    background: var(--color-bg-secondary);
    border-color: var(--color-border-strong);
  }
}

.ghost {
  background: transparent;
  color: var(--color-text-primary);

  &:hover:not(:disabled) {
    background: var(--color-bg-secondary);
  }
}

.sm {
  height: 32px;
  padding: 0 var(--spacing-md);
  font-size: 13px;
}

.md {
  height: 40px;
  padding: 0 var(--spacing-lg);
  font-size: 14px;
}

.lg {
  height: 48px;
  padding: 0 var(--spacing-xl);
  font-size: 16px;
}

.icon {
  display: flex;
  align-items: center;
  font-size: 16px;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
```

---

## Input Component

```tsx
// Input.tsx
import React from 'react';
import styles from './Input.module.scss';

interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  label?: string;
  error?: string;
  prefix?: React.ReactNode;
  suffix?: React.ReactNode;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, prefix, suffix, className = '', ...props }, ref) => {
    return (
      <div className={`${styles.container} ${className}`}>
        {label && <label className={styles.label}>{label}</label>}
        <div className={`${styles.wrapper} ${error ? styles.error : ''}`}>
          {prefix && <span className={styles.prefix}>{prefix}</span>}
          <input ref={ref} className={styles.input} {...props} />
          {suffix && <span className={styles.suffix}>{suffix}</span>}
        </div>
        {error && <span className={styles.errorText}>{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';
```

```scss
// Input.module.scss
.container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.wrapper {
  display: flex;
  align-items: center;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-sm) var(--spacing-md);
  transition: all var(--transition-fast);

  &:hover {
    border-color: var(--color-border-strong);
  }

  &:focus-within {
    border-color: var(--color-text-secondary);
  }

  &.error {
    border-color: var(--color-error);
  }
}

.input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  color: var(--color-text-primary);

  &::placeholder {
    color: var(--color-text-quaternary);
  }
}

.prefix,
.suffix {
  display: flex;
  align-items: center;
  color: var(--color-text-tertiary);
}

.prefix {
  margin-right: var(--spacing-sm);
}

.suffix {
  margin-left: var(--spacing-sm);
}

.errorText {
  font-size: 12px;
  color: var(--color-error);
}
```

---

## Status Badge Component

```tsx
// StatusBadge.tsx
import React from 'react';
import styles from './StatusBadge.module.scss';

type Status = 'success' | 'warning' | 'error' | 'info' | 'default';

interface StatusBadgeProps {
  status: Status;
  children: React.ReactNode;
}

const statusLabels: Record<Status, string> = {
  success: 'Success',
  warning: 'Warning',
  error: 'Error',
  info: 'Info',
  default: 'Default',
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, children }) => {
  return (
    <span className={`${styles.badge} ${styles[status]}`}>
      {children || statusLabels[status]}
    </span>
  );
};
```

```scss
// StatusBadge.module.scss
.badge {
  display: inline-flex;
  align-items: center;
  padding: 2px var(--spacing-sm);
  font-size: 12px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  white-space: nowrap;
}

.default {
  background: var(--color-bg-tertiary);
  color: var(--color-text-secondary);
}

.success {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.warning {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.error {
  background: var(--color-error-bg);
  color: var(--color-error);
}

.info {
  background: var(--color-info-bg);
  color: var(--color-info);
}
```

---

## Empty State Component

```tsx
// EmptyState.tsx
import React from 'react';
import styles from './EmptyState.module.scss';

interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  action,
}) => {
  return (
    <div className={styles.container}>
      {icon && <div className={styles.icon}>{icon}</div>}
      <h3 className={styles.title}>{title}</h3>
      {description && <p className={styles.description}>{description}</p>}
      {action && <div className={styles.action}>{action}</div>}
    </div>
  );
};
```

```scss
// EmptyState.module.scss
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-3xl) var(--spacing-lg);
  text-align: center;
}

.icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-tertiary);
  margin-bottom: var(--spacing-lg);
}

.title {
  font-size: 16px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.description {
  font-size: 14px;
  color: var(--color-text-secondary);
  max-width: 400px;
  margin: 0 0 var(--spacing-lg) 0;
}

.action {
  margin-top: var(--spacing-sm);
}
```

---

## Integration Card Component (Product Integration)

```tsx
// IntegrationCard.tsx
import React from 'react';
import { ProductIcon, ProductName } from '@/components/ProductIcon';
import { CheckOutlined, PlusOutlined } from '@ant-design/icons';
import styles from './IntegrationCard.module.scss';

interface IntegrationCardProps {
  name: string;
  productName: ProductName;
  description: string;
  connected: boolean;
  onClick: () => void;
}

export const IntegrationCard: React.FC<IntegrationCardProps> = ({
  name,
  productName,
  description,
  connected,
  onClick,
}) => {
  return (
    <div className={styles.card} onClick={onClick}>
      <div className={styles.header}>
        <div className={styles.iconWrapper}>
          <ProductIcon name={productName} size={24} />
        </div>
        <div className={styles.content}>
          <h4 className={styles.name}>{name}</h4>
          <p className={styles.description}>{description}</p>
        </div>
      </div>
      <div className={`${styles.status} ${connected ? styles.connected : ''}`}>
        {connected ? (
          <>
            <CheckOutlined /> Connected
          </>
        ) : (
          <>
            <PlusOutlined /> Connect
          </>
        )}
      </div>
    </div>
  );
};
```

```scss
// IntegrationCard.module.scss
.card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-lg);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    border-color: var(--color-border-strong);
    box-shadow: var(--shadow-sm);
  }
}

.header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex: 1;
  min-width: 0;
}

.iconWrapper {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
}

.content {
  min-width: 0;
}

.name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.description {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-md);
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  flex-shrink: 0;

  &.connected {
    background: var(--color-success-bg);
    color: var(--color-success);
  }
}
```

---

## Page Header Component

```tsx
// PageHeader.tsx
import React from 'react';
import styles from './PageHeader.module.scss';

interface PageHeaderProps {
  title: string;
  description?: string;
  actions?: React.ReactNode;
  breadcrumbs?: React.ReactNode;
  backLink?: React.ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  actions,
  breadcrumbs,
  backLink,
}) => {
  return (
    <div className={styles.container}>
      {(breadcrumbs || backLink) && (
        <div className={styles.nav}>
          {backLink && <div className={styles.back}>{backLink}</div>}
          {breadcrumbs && <div className={styles.breadcrumbs}>{breadcrumbs}</div>}
        </div>
      )}
      <div className={styles.content}>
        <div className={styles.text}>
          <h1 className={styles.title}>{title}</h1>
          {description && <p className={styles.description}>{description}</p>}
        </div>
        {actions && <div className={styles.actions}>{actions}</div>}
      </div>
    </div>
  );
};
```

```scss
// PageHeader.module.scss
.container {
  padding: var(--spacing-xl) 0;
  border-bottom: 1px solid var(--color-divider);
  margin-bottom: var(--spacing-xl);
}

.nav {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 13px;
  color: var(--color-text-tertiary);
}

.content {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--spacing-lg);

  @media (max-width: 768px) {
    flex-direction: column;
  }
}

.text {
  flex: 1;
}

.title {
  font-size: 32px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;

  @media (max-width: 768px) {
    font-size: 24px;
  }
}

.description {
  font-size: 16px;
  color: var(--color-text-secondary);
  margin: 0;
  max-width: 600px;
}

.actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-shrink: 0;
}
```
