# Analysis Framework

Systematic approach to analyzing a project for iteration opportunities.

## Step 1: Categorize the Project Type

First, identify what type of application this is:

| Project Type | Characteristics | Key Feature Areas |
|--------------|-----------------|-------------------|
| **Document Management** | File upload, storage, search, version control | Upload/download, search, sharing, permissions, preview |
| **SaaS Dashboard** | Multi-tenant, admin panel, analytics | Authentication, roles, billing, reports, settings |
| **E-commerce** | Products, cart, checkout | Catalog, cart, payments, orders, inventory |
| **Social/Chat** | Real-time, messaging, notifications | WebSocket, push notifications, user profiles |
| **Content Platform** | CMS, publishing, comments | Editor, media handling, SEO, comments |
| **Developer Tool** | API, integrations, CLI | API keys, webhooks, documentation, SDK |
| **AI/AI-Assistant** | LLM integration, RAG | Prompt management, context, vector DB, streaming |

## Step 2: Feature Completeness Analysis

For each category, check implemented vs missing:

### Core Features (Always Required)
- [ ] Authentication (login, register, logout, password reset)
- [ ] User profile management
- [ ] Basic authorization (roles, permissions)
- [ ] Error handling (user-friendly error pages)
- [ ] Input validation

### Domain-Specific Features

#### Document Management
- [ ] File upload (drag-drop, multi-file)
- [ ] File preview (PDF, images, documents)
- [ ] Search (full-text, filters)
- [ ] Folder/collection organization
- [ ] Sharing (links, permissions)
- [ ] Version history
- [ ] Download/export
- [ ] OCR/document parsing
- [ ] AI-powered insights

#### SaaS/Multi-tenant
- [ ] Team/workspace management
- [ ] Invite members
- [ ] Role-based access control
- [ ] Billing/subscription
- [ ] Usage analytics
- [ ] Audit logs
- [ ] API access

#### AI/Assistant
- [ ] Chat interface
- [ ] Context management
- [ ] Streaming responses
- [ ] Document Q&A (RAG)
- [ ] Prompt templates
- [ ] Session history
- [ ] Export conversations

## Step 3: Technical Maturity Assessment

### Level 1 - MVP
- Basic CRUD operations
- Simple authentication
- Minimal error handling

### Level 2 - Production Ready
- Proper error handling
- Input validation
- Basic tests
- Logging
- API documentation

### Level 3 - Scalable
- Caching layer
- Database optimization
- Background jobs
- Rate limiting
- Monitoring

### Level 4 - Enterprise
- Multi-region support
- Advanced security (SSO, 2FA)
- Compliance (GDPR, SOC2)
- Advanced observability
- Disaster recovery

## Step 4: Identify Patterns

### Common Gaps by Project Maturity

| Maturity | Typical Gaps |
|----------|--------------|
| Early MVP | Tests, logging, proper error handling |
| Growth | Caching, optimization, monitoring |
| Scaling | Rate limiting, background jobs, CDN |
| Mature | Advanced permissions, audit logs, integrations |

### Quick Wins Detection

Low effort, high impact improvements:
- Add loading states for better UX
- Implement optimistic updates
- Add keyboard shortcuts
- Improve error messages
- Add skeleton screens
- Implement debounced search
- Add toast notifications for actions

## Step 5: Priority Scoring

Score each suggested feature on:

| Factor | Weight | Scoring |
|--------|--------|---------|
| User Value | 40% | 5 = Critical, 1 = Nice to have |
| Implementation Effort | 30% | 1 = Easy, 5 = Major effort |
| Strategic Importance | 20% | 5 = Aligns with vision, 1 = Peripheral |
| Dependencies | 10% | 1 = Unblocks others, 5 = Blocked |

**Priority Score** = (User Value × 0.4) + ((6 - Effort) × 0.3) + (Strategic × 0.2) + ((6 - Dependencies) × 0.1)

Higher score = Higher priority
