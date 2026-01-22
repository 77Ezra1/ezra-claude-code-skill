# Integration Options

Third-party services and features to integrate.

## Authentication Services

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Clerk** | Quick setup, modern UX | Prebuilt UI, SSO, MFA |
| **Auth0** | Enterprise needs | SSO, MFA, Breached Password Detection |
| **Supabase Auth** | Open source, PostgreSQL native | Row-level security, Realtime |
| **NextAuth.js** | Next.js projects | OAuth providers, database agnostic |
| **Lucia** | Lightweight, framework agnostic | Session-based, customizable |

## File Storage

| Service | Best For | Key Features |
|---------|----------|--------------|
| **AWS S3** | Enterprise, scale | Durability, Glacier, extensive features |
| **Cloudflare R2** | Cost optimization | Zero egress fees, S3 compatible |
| **Supabase Storage** | Quick setup | CDN, transformations, RLS |
| **UploadThing** | Developer experience | Prebuilt uploads, easy client-side |
| **Vercel Blob** | Vercel deployments | Simple, integrated |

## Database & Caching

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Supabase** | PostgreSQL + Realtime | Realtime subscriptions, Auth, Storage |
| **Neon** | Serverless PostgreSQL | Branching, autoscaling |
| **PlanetScale** | MySQL compatible | Branching, schema migrations |
| **Turso** | Edge SQLite | Global edge, low latency |
| **Redis** | Caching, pub/sub | Fast, versatile |
| **Upstash Redis** | Serverless Redis | Edge compatible, durable |

## Email & Notifications

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Resend** | Transactional email | React emails, good DX |
| **SendGrid** | High volume | Reliable, extensive templates |
| **Postmark** | Transactional only | Fast, delivery focused |
| **AWS SES** | Cost optimization | Cheap at scale |
| **Novu** | Multi-channel | Email, SMS, push, in-app |

## AI/LLM Services

| Service | Best For | Key Features |
|---------|----------|--------------|
| **OpenAI** | General purpose | GPT-4, best quality |
| **Anthropic** | Long context | Claude, 200K tokens |
| **Cohere** | RAG, embeddings | Rerank, excellent embeddings |
| **Together** | Open source models | Many model options |
| **Anyscale** | LLM apps | OpenAI API compatible |
| **LangChain** | LLM orchestration | Framework, agnostic |

**Vector Stores for RAG:**
| Service | Best For | Key Features |
|---------|----------|--------------|
| **Pinecone** | Managed vector DB | Fully managed, scalable |
| **Weaviate** | Open source | Self-hosted, hybrid search |
| **Chroma** | Local development | Simple, embedded |
| **Qdrant** | Edge deployment | Fast, filterable |
| **Supabase Vector** | Integrated solution | pgvector, RLS |

## Payment & Billing

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Stripe** | General payments | Most complete, global |
| **LemonSqueezy** | SaaS, merchants | Global tax handling |
| **Paddle** | SaaS, EU focus | Tax compliance, fraud |
| **PayPal** | Consumer payments | Wide acceptance |

## Analytics & Monitoring

| Service | Best For | Key Features |
|---------|----------|--------------|
| **PostHog** | Product analytics | Session replay, funnels |
| **Mixpanel** | Event tracking | User-centric, retention |
| **Plausible** | Privacy-friendly | Simple, GDPR compliant |
| **Vercel Analytics** | Vercel apps | Web vitals, edge |
| **Sentry** | Error tracking | Stack traces, releases |
| **LogRocket** | Session replay | UX debugging |

## Forms & Data Collection

| Service | Best For | Key Features |
|---------|----------|--------------|
| **React Hook Form** | React forms | Minimal re-renders |
| **Zod** | Schema validation | TypeScript first |
| **TanStack Form** | Framework agnostic | Headless, type-safe |
| **Typeform** | Beautiful forms | Conversational UI |
| **Formspree** | Backendless forms | Email on submit |

## Developer Experience

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Vercel** | Next.js, frontend | Preview deployments, edge |
| **Netlify** | JAMstack | Simple, fast builds |
| **Railway** | Full stack apps | Simple, database included |
| **Render** | Docker, containers | Free tier, simple |
| **Fly.io** | Global deployment | Close to users |

## API & Backend

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Supabase** | Auto-generated API | PostgreSQL, Realtime |
| **Convex** | Full stack sync | Reactive, backend in TypeScript |
| **Appwrite** | Open source Firebase | Functions, auth, storage |
| **Firebase** | Google ecosystem | Realtime DB, Firestore |
| **tRPC** | TypeScript APIs | End-to-end type safety |

## Communication

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Pusher** | Real-time features | WebSocket, presence |
| **Ably** | Real-time critical | Guarantees, edge |
| **Socket.io** | Custom real-time | Fallbacks, rooms |
| **Slack SDK** | Slack integrations | Webhooks, API |

## Search

| Service | Best For | Key Features |
|---------|----------|--------------|
| **Algolia** | Instant search | Fast, typo tolerance |
| **Meilisearch** | Open source | Fast, self-hosted |
| **Typesense** | Simple search | Easy to host, fast |
| **Elasticsearch** | Complex needs | Powerful, complex |

## Integration Prioritization

### High Impact, Low Effort (Do First)
- Resend (email)
- UploadThing or Vercel Blob (file upload)
- Zod + React Hook Form (forms)

### High Impact, Medium Effort
- Stripe (payments)
- PostHog or Plausible (analytics)
- Sentry (error tracking)

### Project Dependent
- Clerk/Supabase Auth (if auth not implemented)
- OpenAI/Anthropic (if AI features needed)
- Algolia (if search is core)
