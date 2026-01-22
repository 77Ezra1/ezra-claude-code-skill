# Architecture Patterns

Common architectural improvements and refactorings.

## Frontend Architecture

### State Management Patterns

| Pattern | When to Apply | Signs You Need It |
|---------|---------------|-------------------|
| Context API | Low-medium complexity | Prop drilling > 3 levels |
| Redux Toolkit | Medium-high complexity | Shared state across many components |
| Zustand/Jotai | Medium complexity | Want simpler than Redux |
| React Query | Server state | Frequent fetch calls, caching needs |

### Component Architecture

| Pattern | Description | When to Apply |
|---------|-------------|---------------|
| Atomic Design | atoms → molecules → organisms | Large design system |
| Feature-based | Group by feature, not type | Growing application |
| Container/Presentational | Logic separate from UI | Reusable UI components |
| Composition over inheritance | Compose behaviors | Complex component variants |

### Code Splitting Opportunities

```
Routes by feature
├─ /dashboard → lazy load dashboard module
├─ /documents → lazy load documents module
├─ /settings → lazy load settings module
└─ /admin → lazy load admin module

Heavy components
├─ Charts/Graphs → lazy load on viewport
├─ Rich text editor → lazy load when needed
└─ File upload → lazy load on drop zone open
```

## Backend Architecture

### API Design Patterns

| Pattern | Description | When to Apply |
|---------|-------------|---------------|
| Repository | Abstract data access | Multiple data sources, testing |
| Service Layer | Business logic separation | Complex domain logic |
| CQRS | Separate read/write models | High read/write ratio differences |
| Unit of Work | Transactional consistency | Multi-step operations |

### Common Smells & Solutions

| Smell | Solution |
|-------|----------|
| Fat controllers | Extract service layer |
| Anemic models | Move behavior to entities |
| God classes | Split by responsibility |
| Duplicate logic | Extract to utilities/services |
| Magic numbers | Use constants/enums |
| Inconsistent error handling | Create exception hierarchy |

## Database Patterns

### Query Optimization Signs

```python
# Signs you need optimization:
- List endpoint without pagination → Add LIMIT/OFFSET
- N+1 queries (user.posts for each user) → Use eager loading
- Full table scans → Add indexes
- Slow joins → Consider denormalization
```

### Common Index Needs

| Query Pattern | Index to Add |
|---------------|--------------|
| WHERE user_id = ? | CREATE INDEX idx_user_id ON table(user_id) |
| WHERE created_at > ? ORDER BY created_at | CREATE INDEX idx_created ON table(created_at) |
| WHERE email = ? (unique) | CREATE UNIQUE INDEX idx_email ON table(email) |
| WHERE status = ? AND created_at > ? | CREATE INDEX idx_status_created ON table(status, created_at) |

## Caching Strategy

### What to Cache

| Data Type | Cache Strategy | TTL |
|-----------|----------------|-----|
| User profile | Write-through | 1 hour |
| Session data | Write-behind | 24 hours |
| API responses | Cache-aside | 5-60 min |
| Static content | CDN | Long |
| Search results | Cache-aside | 15 min |

### Cache Invalidation Patterns

| Pattern | When to Use |
|---------|-------------|
| Time-based | Data changes infrequently |
| Event-based | Data changes are predictable |
| Write-through | Cache must be always fresh |
| Cache-aside | Read-heavy workload |

## Integration Patterns

### Third-party Service Integration

| Service | Integration Pattern |
|---------|---------------------|
| Payment (Stripe) | Webhook + polling fallback |
| Email (SendGrid) | Queue + retry |
| Storage (S3) | Direct upload with presigned URL |
| AI (OpenAI) | Streaming + response cache |
| Auth (OAuth) | Token refresh interceptor |

## Microservices Considerations

### Signs You Might Need Microservices

- [ ] Different scaling needs per service
- [ ] Separate teams per domain
- [ ] Different technology requirements
- [ ] Deployment independence needed

### When NOT to Split

- [ ] Small team (< 10 developers)
- [ ] Low traffic
- [ ] Shared data needs are high
- [ ] Team lacks microservices experience

## Performance Patterns

### Frontend

| Technique | Impact | Effort |
|-----------|--------|--------|
| Code splitting | High | Medium |
| Image optimization | High | Low |
| Debounced inputs | Medium | Low |
| Virtual scrolling | High | Medium |
| Memoization | Medium | Low |

### Backend

| Technique | Impact | Effort |
|-----------|--------|--------|
| Database indexing | High | Low |
| Query optimization | High | Medium |
| Caching layer | High | Medium |
| Async processing | High | High |
| Connection pooling | Medium | Low |
