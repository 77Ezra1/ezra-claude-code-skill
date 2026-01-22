# Integration Page Templates

Templates for creating integration UI pages (Notion, GitHub, Slack, etc.).

---

## Integration Settings Page Template

```tsx
// IntegrationSettingsPage.tsx
import React from 'react';
import { PageHeader } from '@/components/PageHeader';
import { IntegrationCard } from '@/components/IntegrationCard';
import { ProductIcon, ProductName } from '@/components/ProductIcon';
import styles from './IntegrationSettingsPage.module.scss';

interface Integration {
  id: string;
  name: string;
  productName: ProductName;
  description: string;
  connected: boolean;
}

const integrations: Integration[] = [
  {
    id: 'notion',
    name: 'Notion',
    productName: 'notion',
    description: 'Connect your Notion workspace to sync documents',
    connected: false,
  },
  {
    id: 'github',
    name: 'GitHub',
    productName: 'github',
    description: 'Link repositories for code documentation',
    connected: false,
  },
  {
    id: 'slack',
    name: 'Slack',
    productName: 'slack',
    description: 'Get notifications in your Slack channels',
    connected: false,
  },
];

export const IntegrationSettingsPage: React.FC = () => {
  const [connectedIds, setConnectedIds] = React.useState<Set<string>>(new Set());

  const handleToggle = (integration: Integration) => {
    // Handle connect/disconnect
    setConnectedIds(prev => {
      const next = new Set(prev);
      if (next.has(integration.id)) {
        next.delete(integration.id);
      } else {
        next.add(integration.id);
      }
      return next;
    });
  };

  return (
    <div className={styles.container}>
      <PageHeader
        title="Integrations"
        description="Connect your favorite tools to enhance your workflow"
      />

      <div className={styles.grid}>
        {integrations.map(integration => (
          <IntegrationCard
            key={integration.id}
            {...integration}
            connected={connectedIds.has(integration.id)}
            onClick={() => handleToggle(integration)}
          />
        ))}
      </div>
    </div>
  );
};
```

```scss
// IntegrationSettingsPage.module.scss
.container {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--spacing-lg);
  padding-bottom: var(--spacing-3xl);
}
```

---

## OAuth Connection Modal Template

```tsx
// OAuthModal.tsx
import React from 'react';
import { Modal, Button } from 'antd';
import { ProductIcon, ProductName } from '@/components/ProductIcon';
import styles from './OAuthModal.module.scss';

interface OAuthModalProps {
  visible: boolean;
  productName: ProductName;
  productNameDisplay: string;
  onClose: () => void;
  onConnect: () => void;
  loading?: boolean;
}

export const OAuthModal: React.FC<OAuthModalProps> = ({
  visible,
  productName,
  productNameDisplay,
  onClose,
  onConnect,
  loading = false,
}) => {
  return (
    <Modal
      open={visible}
      onCancel={onClose}
      footer={null}
      width={440}
      className={styles.modal}
    >
      <div className={styles.content}>
        <div className={styles.iconWrapper}>
          <ProductIcon name={productName} size={48} />
        </div>

        <h2 className={styles.title}>Connect to {productNameDisplay}</h2>

        <p className={styles.description}>
          You will be redirected to {productNameDisplay} to authorize the connection.
          We only request the permissions necessary for the integration to work.
        </p>

        <div className={styles.permissions}>
          <h4 className={styles.permissionsTitle}>Required permissions</h4>
          <ul className={styles.permissionsList}>
            <li>Read access to your documents</li>
            <li>Write access to create new content</li>
            <li>Basic profile information</li>
          </ul>
        </div>

        <div className={styles.actions}>
          <Button className={styles.cancelBtn} onClick={onClose}>
            Cancel
          </Button>
          <Button
            type="primary"
            className={styles.connectBtn}
            onClick={onConnect}
            loading={loading}
          >
            Connect
          </Button>
        </div>
      </div>
    </Modal>
  );
};
```

```scss
// OAuthModal.module.scss
.modal {
  :global {
    .ant-modal-content {
      border-radius: var(--radius-2xl);
      padding: var(--spacing-xl);
    }

    .ant-modal-close {
      top: var(--spacing-lg);
      right: var(--spacing-lg);
    }
  }
}

.content {
  text-align: center;
}

.iconWrapper {
  width: 64px;
  height: 64px;
  margin: 0 auto var(--spacing-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-xl);
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md) 0;
}

.description {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0 0 var(--spacing-lg) 0;
}

.permissions {
  text-align: left;
  padding: var(--spacing-md);
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-xl);
}

.permissionsTitle {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.permissionsList {
  margin: 0;
  padding-left: var(--spacing-lg);

  li {
    font-size: 13px;
    color: var(--color-text-secondary);
    margin-bottom: var(--spacing-xs);

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

.cancelBtn {
  flex: 1;
}

.connectBtn {
  flex: 1;
}
```

---

## Integration Detail Page Template

```tsx
// IntegrationDetailPage.tsx
import React from 'react';
import { PageHeader } from '@/components/PageHeader';
import { Button } from 'antd';
import { ProductIcon, ProductName } from '@/components/ProductIcon';
import { CheckCircleOutlined, DisconnectOutlined } from '@ant-design/icons';
import styles from './IntegrationDetailPage.module.scss';

interface IntegrationDetailPageProps {
  productName: ProductName;
  productNameDisplay: string;
  connected: boolean;
  accountName?: string;
  lastSync?: Date;
  onConnect: () => void;
  onDisconnect: () => void;
}

export const IntegrationDetailPage: React.FC<IntegrationDetailPageProps> = ({
  productName,
  productNameDisplay,
  connected,
  accountName,
  lastSync,
  onConnect,
  onDisconnect,
}) => {
  return (
    <div className={styles.container}>
      <PageHeader
        title={productNameDisplay}
        backLink={
          <button className={styles.backLink} onClick={() => window.history.back()}>
            Back to Integrations
          </button>
        }
      />

      <div className={styles.content}>
        <div className={styles.card}>
          <div className={styles.header}>
            <div className={styles.iconWrapper}>
              <ProductIcon name={productName} size={32} />
            </div>
            <div className={styles.info}>
              <h2 className={styles.title}>{productNameDisplay}</h2>
              {connected ? (
                <div className={styles.statusConnected}>
                  <CheckCircleOutlined /> Connected as {accountName}
                </div>
              ) : (
                <div className={styles.statusDisconnected}>Not connected</div>
              )}
            </div>
          </div>

          {connected && lastSync && (
            <div className={styles.syncInfo}>
              <span className={styles.label}>Last sync</span>
              <span className={styles.value}>
                {lastSync.toLocaleDateString()} at {lastSync.toLocaleTimeString()}
              </span>
            </div>
          )}

          <div className={styles.actions}>
            {connected ? (
              <Button
                danger
                icon={<DisconnectOutlined />}
                onClick={onDisconnect}
              >
                Disconnect
              </Button>
            ) : (
              <Button type="primary" onClick={onConnect}>
                Connect {productNameDisplay}
              </Button>
            )}
          </div>
        </div>

        <div className={styles.features}>
          <h3 className={styles.featuresTitle}>Features</h3>
          <div className={styles.featuresList}>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>sync</div>
              <div className={styles.featureContent}>
                <h4 className={styles.featureTitle}>Two-way sync</h4>
                <p className={styles.featureDescription}>
                  Changes are synced automatically between the platforms
                </p>
              </div>
            </div>
            <div className={styles.feature}>
              <div className={styles.featureIcon}>search</div>
              <div className={styles.featureContent}>
                <h4 className={styles.featureTitle}>Unified search</h4>
                <p className={styles.featureDescription}>
                  Search across all your connected platforms
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
```

```scss
// IntegrationDetailPage.module.scss
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.backLink {
  font-size: 13px;
  color: var(--color-text-secondary);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);

  &:hover {
    color: var(--color-text-primary);
  }
}

.content {
  padding-bottom: var(--spacing-3xl);
}

.card {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
}

.header {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.iconWrapper {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
}

.info {
  flex: 1;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.statusConnected {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  font-size: 14px;
  color: var(--color-success);
}

.statusDisconnected {
  font-size: 14px;
  color: var(--color-text-tertiary);
}

.syncInfo {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md) 0;
  border-top: 1px solid var(--color-divider);
  border-bottom: 1px solid var(--color-divider);
  margin-bottom: var(--spacing-lg);
}

.label {
  font-size: 13px;
  color: var(--color-text-tertiary);
}

.value {
  font-size: 14px;
  color: var(--color-text-primary);
}

.actions {
  display: flex;
  gap: var(--spacing-md);
}

.features {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
}

.featuresTitle {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-lg) 0;
}

.featuresList {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.feature {
  display: flex;
  gap: var(--spacing-md);
}

.featureIcon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-secondary);
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.featureContent {
  flex: 1;
}

.featureTitle {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.featureDescription {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin: 0;
}
```

---

## Quick Integration Button Template

```tsx
// QuickConnectButton.tsx
import React from 'react';
import { Button } from 'antd';
import { ProductIcon, ProductName } from '@/components/ProductIcon';
import styles from './QuickConnectButton.module.scss';

interface QuickConnectButtonProps {
  productName: ProductName;
  productNameDisplay: string;
  connected: boolean;
  onClick: () => void;
}

export const QuickConnectButton: React.FC<QuickConnectButtonProps> = ({
  productName,
  productNameDisplay,
  connected,
  onClick,
}) => {
  return (
    <button
      className={`${styles.button} ${connected ? styles.connected : ''}`}
      onClick={onClick}
    >
      <ProductIcon name={productName} size={16} />
      <span>{connected ? 'Connected' : `Connect ${productNameDisplay}`}</span>
    </button>
  );
};
```

```scss
// QuickConnectButton.module.scss
.button {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    border-color: var(--color-border-strong);
    background: var(--color-bg-secondary);
  }

  &.connected {
    border-color: var(--color-success);
    background: var(--color-success-bg);
    color: var(--color-success);
  }
}
```

---

## Integration Configuration Form Template

```tsx
// IntegrationConfigForm.tsx
import React from 'react';
import { Input, Button } from '@/components';
import { ProductIcon, ProductName } from '@/components/ProductIcon';
import styles from './IntegrationConfigForm.module.scss';

interface IntegrationConfigFormProps {
  productName: ProductName;
  productNameDisplay: string;
  fields: Array<{
    name: string;
    label: string;
    type: 'text' | 'password' | 'url';
    placeholder: string;
    required?: boolean;
  }>;
  onSave: (values: Record<string, string>) => void;
  onCancel: () => void;
  loading?: boolean;
}

export const IntegrationConfigForm: React.FC<IntegrationConfigFormProps> = ({
  productName,
  productNameDisplay,
  fields,
  onSave,
  onCancel,
  loading = false,
}) => {
  const [values, setValues] = React.useState<Record<string, string>>({});
  const [errors, setErrors] = React.useState<Record<string, string>>({});

  const handleChange = (name: string, value: string) => {
    setValues(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => {
        const next = { ...prev };
        delete next[name];
        return next;
      });
    }
  };

  const handleSubmit = () => {
    const newErrors: Record<string, string> = {};

    for (const field of fields) {
      if (field.required && !values[field.name]) {
        newErrors[field.name] = `${field.label} is required`;
      }
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSave(values);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <ProductIcon name={productName} size={32} />
        <h3 className={styles.title}>Configure {productNameDisplay}</h3>
      </div>

      <div className={styles.form}>
        {fields.map(field => (
          <Input
            key={field.name}
            label={field.label}
            type={field.type}
            placeholder={field.placeholder}
            value={values[field.name] || ''}
            onChange={e => handleChange(field.name, e.target.value)}
            error={errors[field.name]}
            required={field.required}
          />
        ))}
      </div>

      <div className={styles.actions}>
        <Button variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
        <Button variant="primary" onClick={handleSubmit} loading={loading}>
          Save Configuration
        </Button>
      </div>
    </div>
  );
};
```

```scss
// IntegrationConfigForm.module.scss
.container {
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
}

.header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
}
```
