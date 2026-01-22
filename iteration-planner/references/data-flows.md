# Data Flows

Common data flow patterns and improvements.

## CRUD Data Flow Analysis

### Standard CRUD Flow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Frontend│ ──▶ │ API     │ ──▶ │ Service │ ──▶ │ Database│
│ Component│    │ Handler │     │ Layer   │     │         │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
     │ ◀─────────────│◀──────────────│◀──────────────│
     │               │               │               │
```

### Common Gaps

| Gap | Sign | Solution |
|-----|------|----------|
| No service layer | Business logic in controllers | Extract to services |
| Direct DB access | Controllers query DB directly | Use repository pattern |
| No validation | Invalid data reaches DB | Add validation layer |
| No caching | Repeated identical queries | Add cache layer |
| No error handling | Raw exceptions to client | Add exception handlers |

## Authentication Flow

### Standard Auth Flow

```
Login Request:
  └─ POST /auth/login
     ├─ Validate input
     ├─ Check user exists
     ├─ Verify password
     ├─ Generate tokens (access + refresh)
     ├─ Set session/cache
     └─ Return user + tokens

Authenticated Request:
  └─ Any protected endpoint
     ├─ Extract/verify token
     ├─ Load user from DB/cache
     ├─ Check permissions
     └─ Proceed or return 401/403
```

### Missing Auth Features to Check

- [ ] Refresh token rotation
- [ ] Token revocation (logout)
- [ ] Rate limiting on auth endpoints
- [ ] Login attempt tracking
- [ ] Session management
- [ ] Password reset flow
- [ ] Email verification flow

## File Upload Flow

### Recommended Pattern

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Frontend│ ──▶ │ API     │ ──▶ │ Storage │ ──▶ │ Database│
│ (Select │     │ (Generate│     │ (Direct │     │ (Record  │
│  file)  │     │  presign │     │  upload)│     │  metadata)│
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │               │
     │───────────────│───────────────│───────────────│
     │  Upload with presigned URL directly to storage │
     └────────────────────────────────────────────────┘
```

### Improvements Over Direct Upload

| Issue | Direct Upload | Presigned URL |
|-------|---------------|---------------|
| Server memory | Files pass through server | Direct to storage |
| Scalability | Limited by server | Scales with storage |
| Resumability | Complex to implement | Built-in to storage |
| Cost | Higher egress bandwidth | Lower |

## Real-time Data Flow

### WebSocket vs Polling vs SSE

| Pattern | Best For | Complexity |
|---------|----------|------------|
| Polling | Simple updates, low frequency | Low |
| SSE | Server → client only | Medium |
| WebSocket | Bidirectional, real-time | High |

### WebSocket Reconnection Strategy

```javascript
// Exponential backoff reconnection
const delays = [1000, 2000, 5000, 10000, 30000];

function connect(attempt = 0) {
  ws = new WebSocket(url);

  ws.onclose = () => {
    const delay = delays[Math.min(attempt, delays.length - 1)];
    setTimeout(() => connect(attempt + 1), delay);
  };
}
```

## State Synchronization

### Client State vs Server State

| State Type | Storage | Sync Strategy |
|------------|---------|---------------|
| User preferences | Local storage | Sync on login/load |
| Ephemeral UI state | Component state | No sync |
| Application data | Server state | API sync |
| Offline edits | IndexedDB | Sync when online |

### Optimistic Updates

```
User Action:
  1. Update UI immediately (assume success)
  2. Send API request
  3a. On success: Continue
  3b. On error: Revert UI, show error
```

When to use:
- High likelihood of success
- Quick user feedback important
- Easy to reverse operation

## Background Jobs

### When to Use Background Jobs

| Task | Synchronous | Background |
|------|-------------|------------|
| Email sending | ✗ (slow) | ✓ |
| Image processing | ✗ (very slow) | ✓ |
| Webhook calls | ✗ (unreliable) | ✓ |
| Data export | ✗ (slow) | ✓ |
| Cache warming | ✗ (nice to have) | ✓ |
| Database cleanup | ✗ (intensive) | ✓ |

### Job Queue Patterns

| Pattern | Use Case |
|---------|----------|
| FIFO | Standard processing |
| Priority | Urgent tasks first |
| Delayed | Schedule for later |
| Recurring | Periodic tasks |

## Caching Strategies

### Cache Aside (Lazy Loading)

```
Read:
  1. Check cache
  2. Hit? Return data
  3. Miss? Load from DB, write to cache, return

Write:
  1. Update DB
  2. Invalidate cache
```

### Write Through

```
Write:
  1. Write to cache
  2. Write to DB
  3. Return

Read:
  1. Check cache (always fresh)
```

### Write Back (Write Behind)

```
Write:
  1. Write to cache
  2. Acknowledge
  3. Async write to DB

Risk: Data loss if cache fails
```

## Error Handling Flow

### Proper Error Propagation

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│Database │ ──▶ │Service  │ ──▶ │Handler  │ ──▶ │Frontend │
│ Error   │     │ Maps to │     │ HTTP    │     │ Displays│
└─────────┘     │ Domain  │     │ Status  │     │ Message │
                │ Error   │     │         │     │         │
                └─────────┘     └─────────┘     └─────────┘
```

### Error Hierarchy Example

```python
# Domain errors (map to HTTP)
NotFoundError → 404
ValidationError → 400
AuthenticationError → 401
AuthorizationError → 403
ConflictError → 409
RateLimitError → 429

# Unexpected errors (map to 500)
DatabaseError → 500
ExternalServiceError → 500
```
