# Backend Performance Solutions

Common performance issues and optimizations for FastAPI/Python applications.

## Database Query Optimization

### N+1 Query Problem

```python
# SLOW - N+1 queries
@app.get("/projects")
def get_projects():
    projects = db.query(Project).all()
    for project in projects:
        # This executes a query for EACH project!
        project.owner = db.query(User).filter(User.id == project.owner_id).first()
    return projects

# FAST - Single query with join
from sqlalchemy.orm import joinedload

@app.get("/projects")
def get_projects():
    projects = db.query(Project).options(joinedload(Project.owner)).all()
    return projects

# PRISMA - Use include
projects = await prisma.project.find_many(include={"owner": True})
```

### Select Only Needed Columns

```python
# SLOW - Fetches all columns
users = db.query(User).all()

# FAST - Only needed columns
users = db.query(User.id, User.name, User.email).all()

# PRISMA
users = await prisma.user.find_many(select={"id": True, "name": True, "email": True})
```

### Pagination

```python
# SLOW - Returns all records (can be millions!)
@app.get("/items")
def get_items():
    return db.query(Item).all()

# FAST - Paginated
from pydantic import BaseModel

class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list

@app.get("/items")
def get_items(page: int = 1, page_size: int = 50):
    query = db.query(Item)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return PaginatedResponse(total=total, page=page, page_size=page_size, items=items)
```

### Database Indexing

```python
# Add indexes to commonly queried fields
# In Prisma schema:
model User {
  id        String   @id @default(uuid())
  email     String   @unique  # Index for email lookups
  username  String   @unique  # Index for username lookups
  createdAt DateTime @default(now())
  role      String

  @@index([email])  # Explicit index
  @@index([role, createdAt])  # Composite index for filtered queries
}

# Or in SQLAlchemy:
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(50), unique=True, index=True)
    role = Column(String(50))

    __table_args__ = (
        Index('ix_user_role_created', 'role', 'created_at'),
    )
```

### Connection Pooling

```python
# Configure connection pool
# Prisma - in schema.prisma:
database db {
  provider = "postgresql"
  url      = env("DATABASE_URL")

  pool_timeout = 30
  connection_limit = 10  # Adjust based on your needs
}

# SQLAlchemy
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,          # Number of connections to maintain
    max_overflow=20,       # Additional connections under load
    pool_timeout=30,       # Wait time for connection
    pool_recycle=3600,     # Recycle connections after 1 hour
    pool_pre_ping=True,    # Verify connections before use
)
```

## Async Operations

### Use Async I/O

```python
# SLOW - Blocking I/O in async handler
import requests  # Synchronous!

@app.get("/proxy")
async def proxy_data():
    response = requests.get("https://api.example.com/data")  # Blocks event loop!
    return response.json()

# FAST - Async HTTP client
import httpx

@app.get("/proxy")
async def proxy_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
    return response.json()

# EVEN FASTER - Reuse client
# In main.py or dependency
client = httpx.AsyncClient(timeout=30.0)

@app.get("/proxy")
async def proxy_data(http_client: httpx.AsyncClient = Depends(lambda: client)):
    response = await http_client.get("https://api.example.com/data")
    return response.json()

# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown():
    await client.aclose()
```

### Parallel Independent Operations

```python
# SLOW - Sequential operations
async def get_dashboard(user_id: str):
    user = await get_user(user_id)
    projects = await get_user_projects(user_id)
    notifications = await get_notifications(user_id)
    return {"user": user, "projects": projects, "notifications": notifications}

# FAST - Parallel operations
import asyncio

async def get_dashboard(user_id: str):
    user, projects, notifications = await asyncio.gather(
        get_user(user_id),
        get_user_projects(user_id),
        get_notifications(user_id)
    )
    return {"user": user, "projects": projects, "notifications": notifications}
```

### Background Tasks

```python
from fastapi import BackgroundTasks

@app.post("/process")
async def start_processing(item_id: str, background_tasks: BackgroundTasks):
    # Don't wait for processing to complete
    background_tasks.add_task(process_item, item_id)
    return {"message": "Processing started"}

async def process_item(item_id: str):
    # This runs in the background
    await heavy_computation(item_id)
    await send_notification(item_id)
```

## Caching

### Response Caching

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

@app.get("/projects/{project_id}")
@cache(expire=60)  # Cache for 60 seconds
async def get_project(project_id: str):
    return await prisma.project.find_unique(where={"id": project_id})
```

### Database Query Result Caching

```python
from functools import lru_cache
import hashlib
import json

# Simple in-memory cache (not suitable for distributed systems)
_query_cache = {}

async def cached_query(key: str, query_func, ttl: int = 300):
    if key in _query_cache:
        result, timestamp = _query_cache[key]
        if time.time() - timestamp < ttl:
            return result

    result = await query_func()
    _query_cache[key] = (result, time.time())
    return result
```

## Response Optimization

### Compression

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Stream Large Responses

```python
from fastapi.responses import StreamingResponse
import io

@app.get("/large-download")
async def download_large_file():
    def iterfile():
        with open("large_file.bin", "rb") as f:
            while chunk := f.read(1024 * 1024):  # 1MB chunks
                yield chunk

    return StreamingResponse(iterfile(), media_type="application/octet-stream")
```

### Exclude Unnecessary Data

```python
# Use response models to limit data
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    # Don't include password_hash, internal notes, etc.

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    return await prisma.user.find_unique(where={"id": user_id})
```

## Monitoring and Profiling

### Add Request Timing Middleware

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # Log slow requests
    if process_time > 1.0:
        logger.warning(f"Slow request: {request.url} took {process_time:.2f}s")

    return response
```

### Database Query Logging

```python
import logging

# Enable SQLAlchemy query logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# For Prisma, configure logging
import prisma
prisma.logger.setLevel(logging.INFO)
```

## Memory Optimization

### Use Generators for Large Data

```python
# SLOW - Loads everything into memory
@app.get("/export")
async def export_data():
    data = await prisma.item.find_many()  # Could be millions of rows!
    return {"data": data}

# FAST - Streams results
@app.get("/export")
async def export_data():
    async def generate():
        async for item in prisma.item.find_each(batch_size=100):
            yield json.dumps(item) + "\n"

    return StreamingResponse(generate(), media_type="application/jsonl")
```

### Cleanup Resources

```python
@app.post("/upload")
async def upload_file(file: UploadFile):
    content = await file.read()

    # Process file
    result = await process_file(content)

    # Explicit cleanup
    await file.close()
    del content

    return result
```
