# Product SVG Icons Library

Collection of SVG icons for common product integrations.

## Usage Pattern

```tsx
import { IconComponent } from '@ant-design/icons';
import { ProductIcon } from '@/components/ProductIcon';

// For UI elements: use Ant Design icons
<HomeOutlined />
<SettingOutlined />

// For product integrations: use product SVG icons
<ProductIcon name="notion" size={20} />
<ProductIcon name="github" size={16} />
```

---

## Product Icons

### Notion

```tsx
export const NotionIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path
      d="M4.459 4.208c.746.606 1.026.56 2.428.466l10.74-.746c1.527-.14 1.863.236 1.863 1.522v12.527c0 1.266-.28 1.809-1.604 1.928l-11.586.746c-1.024.093-1.454-.14-1.926-1.125V6.486l-.06-.626L4.46 4.208z"
      fill="currentColor"
    />
    <path d="M15.458 5.503l-1.49-1.49v8.715l1.49.094V5.503z" fill="#fff"/>
    <path d="M11.035 4.628l-1.776-.23v9.06l1.776.14v-8.97z" fill="#fff"/>
    <path d="M6.367 4.441l-1.637.23v8.348l1.637.28V4.441z" fill="#fff"/>
    <path d="M14.962 14.48l1.49-.094v2.414l-1.49.23v-2.55z" fill="#fff"/>
    <path d="M10.259 14.62l1.776-.14v2.667l-1.776.28v-2.807z" fill="#fff"/>
    <path d="M5.73 14.9l1.637-.28v2.9l-1.637.328V14.9z" fill="#fff"/>
  </svg>
);
```

### GitHub

```tsx
export const GitHubIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
  </svg>
);
```

### Slack

```tsx
export const SlackIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.522 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.522 2.521 2.528 2.528 0 0 1-2.522 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 8.834a2.528 2.528 0 0 1 2.522-2.521A2.528 2.528 0 0 1 24 8.834a2.528 2.528 0 0 1-2.522 2.522h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.522 2.527 2.527 0 0 1-2.52-2.522V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312zM15.165 18.956a2.528 2.528 0 0 1 2.523 2.522A2.528 2.528 0 0 1 15.165 24a2.527 2.527 0 0 1-2.52-2.522v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313A2.527 2.527 0 0 1 24 15.165a2.528 2.528 0 0 1-2.522 2.523h-6.313z" fill="currentColor"/>
  </svg>
);
```

### Google Drive

```tsx
export const GoogleDriveIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M7.71 3.5L1.15 15l4.58 7.5h13.54l4.58-7.5L17.29 3.5H7.71z" fill="currentColor" opacity="0.2"/>
    <path d="M7.71 3.5l-3.04 5.28L12.5 22h4.79l3.04-5.28L12.5 3.5H7.71z" fill="currentColor"/>
    <path d="M1.15 15l3.04 5.28h8.31l-3.04-5.28H1.15z" fill="currentColor"/>
  </svg>
);
```

### Linear

```tsx
export const LinearIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);
```

### Figma

```tsx
export const FigmaIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M5 5.5A3.5 3.5 0 0 1 8.5 2H12v7H8.5A3.5 3.5 0 0 1 5 5.5z" fill="#1abcfe"/>
    <path d="M12 2h3.5a3.5 3.5 0 1 1 0 7H12V2z" fill="#0acf83"/>
    <path d="M12 12a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z" fill="#ff7262"/>
    <path d="M8.5 9.5A3.5 3.5 0 0 0 5 13a3.5 3.5 0 0 0 3.5 3.5H12v-7H8.5z" fill="#f24e1e"/>
    <path d="M8.5 2A3.5 3.5 0 0 0 5 5.5v3.5h3.5a3.5 3.5 0 0 0 0-7H8.5z" fill="#a259ff"/>
  </svg>
);
```

### Discord

```tsx
export const DiscordIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
  </svg>
);
```

### Trello

```tsx
export const TrelloIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M22 10.5v8.5a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5v-8.5a2.5 2.5 0 0 1 2.5-2.5h15a2.5 2.5 0 0 1 2.5 2.5zM7 8.5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-10a1 1 0 0 0-1-1H7zm8 0a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2a1 1 0 0 0 1-1v-6a1 1 0 0 0-1-1h-2z"/>
  </svg>
);
```

### Jira

```tsx
export const JiraIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M11.571 0c-.176 0-.31.001-.358.007a19.76 19.76 0 0 1-.364.033C7.443.346 4.25 2.185 2.228 5.012a11.875 11.875 0 0 0-2.119 5.243c-.096.659-.108.854-.108 1.747s.012 1.089.108 1.748c.652 4.506 3.86 8.292 8.209 9.695.779.25 1.6.422 2.534.525.363.04 1.935.04 2.299 0 1.611-.178 2.977-.577 4.323-1.264.207-.106.247-.134.219-.158-.02-.013-.9-1.193-1.955-2.62l-1.919-2.592-2.404-3.558a338.739 338.739 0 0 0-2.422-3.556c-.009-.002-.018 1.579-.023 3.51-.007 3.38-.01 3.515-.052 3.595a.426.426 0 0 1-.206.214c-.075.037-.14.044-.495.044H7.81l-.108-.068a.438.438 0 0 1-.157-.171l-.05-.106.006-4.703.007-4.705.072-.092a.645.645 0 0 1 .174-.143c.096-.047.134-.051.54-.051.478 0 .558.018.682.154.035.038 1.337 1.999 2.895 4.361a10760.433 10760.433 0 0 0 4.735 7.17l1.9 2.879.096-.063a12.317 12.317 0 0 0 2.466-2.163 11.944 11.944 0 0 0 2.824-6.134c.096-.66.108-.854.108-1.748 0-.893-.012-1.088-.108-1.747-.652-4.506-3.859-8.292-8.208-9.695a12.597 12.597 0 0 0-2.499-.523A33.119 33.119 0 0 0 11.571 0zm4.069 7.217c.347 0 .408.005.486.047a.473.473 0 0 1 .237.277c.018.06.023 1.365.018 4.304l-.006 4.218-.744-1.14-.746-1.14v-3.066c0-1.982.01-3.097.023-3.15a.478.478 0 0 1 .233-.296c.096-.05.13-.054.5-.054z"/>
  </svg>
);
```

### Confluence

```tsx
export const ConfluenceIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M16.568 17.442c-.286 0-.522.097-.748.283l-.09.082c-1.18 1.043-2.804 1.59-4.56 1.59-3.548 0-6.666-2.318-7.86-5.73a.973.973 0 0 1 .595-1.236.98.98 0 0 1 1.246.585c.944 2.693 3.36 4.475 6.02 4.475 1.385 0 2.66-.423 3.582-1.237l.09-.078a.988.988 0 0 1 1.383.082.966.966 0 0 1-.082 1.372 6.33 6.33 0 0 1-1.576.912zm4.827-5.254a.973.973 0 0 1-.598-.206l-.1-.09a9.27 9.27 0 0 0-6.094-2.277c-2.352 0-4.525.853-6.148 2.273a.988.988 0 0 1-1.386-.072.965.965 0 0 1 .072-1.372A11.205 11.205 0 0 1 14.603 7.59c2.654 0 5.098.947 6.925 2.525l.1.09a.965.965 0 0 1-.074 1.47.98.98 0 0 1-.595.208v.006zm-3.896-5.46a.973.973 0 0 1-.605-.21l-.078-.067a6.556 6.556 0 0 0-4.227-1.54 6.56 6.56 0 0 0-4.232 1.536.988.988 0 0 1-1.382-.082.966.966 0 0 1 .082-1.372A8.51 8.51 0 0 1 12.59 3.07c2.025 0 3.89.717 5.32 1.91l.078.067a.965.965 0 0 1-.086 1.573.98.98 0 0 1-.607.1z"/>
  </svg>
);
```

### Asana

```tsx
export const AsanaIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M6 14c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zM6 2C3.79 2 2 3.79 2 6s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm12 0c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 12c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4z"/>
  </svg>
);
```

### Dropbox

```tsx
export const DropboxIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M6 1.803L0 5.622l6 3.62 6-3.62-6-3.819zm12 0l-6 3.819 6 3.62 6-3.62-6-3.819zM0 13.937l6 3.819 6-3.819-6-3.62-6 3.62zm12 0l6 3.819 6-3.819-6-3.62-6 3.62zM6 19.378L0 23.197l6 3.803 6-3.803-6-3.819zm12 0l-6 3.819 6 3.803 6-3.803-6-3.819z"/>
  </svg>
);
```

### Zoom

```tsx
export const ZoomIcon = ({ size = 16, className = '' }: { size?: number; className?: string }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    className={className}
  >
    <path d="M14.5 12c0 1.38-1.12 2.5-2.5 2.5S9.5 13.38 9.5 12s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5z"/>
    <path d="M21 16.5v-9c0-1.1-.9-2-2-2H3c-1.1 0-2 .9-2 2v9c0 1.1.9 2 2 2h5.34l-.82 2.45c-.14.43.18.87.63.87h.01c.2 0 .39-.11.48-.28L10.66 17h2.69l1.01 2.55c.09.17.28.28.48.28h.01c.45 0 .78-.44.63-.87L15.66 16.5H19c1.1 0 2-.9 2-2zM12 14.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
  </svg>
);
```

---

## Unified Component

```tsx
// frontend/src/components/ProductIcon/ProductIcon.tsx
import React from 'react';

export type ProductName =
  | 'notion'
  | 'github'
  | 'slack'
  | 'google-drive'
  | 'linear'
  | 'figma'
  | 'discord'
  | 'trello'
  | 'jira'
  | 'confluence'
  | 'asana'
  | 'dropbox'
  | 'zoom';

interface ProductIconProps {
  name: ProductName;
  size?: number;
  className?: string;
}

export const ProductIcon: React.FC<ProductIconProps> = ({ name, size = 16, className = '' }) => {
  const icons: Record<ProductName, JSX.Element> = {
    notion: <NotionIcon size={size} className={className} />,
    github: <GitHubIcon size={size} className={className} />,
    slack: <SlackIcon size={size} className={className} />,
    'google-drive': <GoogleDriveIcon size={size} className={className} />,
    linear: <LinearIcon size={size} className={className} />,
    figma: <FigmaIcon size={size} className={className} />,
    discord: <DiscordIcon size={size} className={className} />,
    trello: <TrelloIcon size={size} className={className} />,
    jira: <JiraIcon size={size} className={className} />,
    confluence: <ConfluenceIcon size={size} className={className} />,
    asana: <AsanaIcon size={size} className={className} />,
    dropbox: <DropboxIcon size={size} className={className} />,
    zoom: <ZoomIcon size={size} className={className} />,
  };

  return icons[name] || null;
};
```
