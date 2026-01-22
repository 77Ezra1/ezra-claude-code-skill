# Code Quality Solutions

Common code quality issues and improvements for FastAPI/Python applications.

## Type Hints

### Missing Return Types

```python
# BAD - No type hints
def get_user(user_id):
    return db.query(User).filter(User.id == user_id).first()

# GOOD - Full type hints
from typing import Optional
from app.models import User

def get_user(user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

# EVEN BETTER - With pydantic
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

def get_user(user_id: str) -> UserResponse | None:
    user = db.query(User).filter(User.id == user_id).first()
    return UserResponse.from_orm(user) if user else None
```

### Complex Type Hints

```python
# Use proper generics
from typing import List, Dict, Optional

# BAD
def get_items():
    return [{"id": 1, "name": "item"}]

# GOOD
def get_items() -> List[Dict[str, any]]:  # or more specific
    return [{"id": 1, "name": "item"}]

# BETTER - Use TypedDict or dataclass
from typing import TypedDict

class Item(TypedDict):
    id: int
    name: str

def get_items() -> List[Item]:
    return [{"id": 1, "name": "item"}]
```

## Error Handling

### Specific Exceptions

```python
# BAD - Bare except
try:
    result = process_data(data)
except:
    pass

# GOOD - Specific exceptions
try:
    result = process_data(data)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise HTTPException(status_code=500, detail="Database error")

# BEST - With context
try:
    result = process_data(data)
except ValidationError as e:
    logger.error(f"Validation failed for data={data[:100]}: {e}")
    raise
```

### Custom Exceptions

```python
# Create domain-specific exceptions
class AppError(Exception):
    """Base exception for application errors"""
    pass

class NotFoundError(AppError):
    """Resource not found"""
    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} with id '{identifier}' not found")

class ValidationError(AppError):
    """Input validation failed"""
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation failed for '{field}': {message}")

# Usage
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await prisma.user.find_unique(where={"id": user_id})
    if not user:
        raise NotFoundError("User", user_id)
    return user

# Global exception handler
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"error": str(exc), "resource": exc.resource}
    )
```

## Logging

### Proper Logging Setup

```python
# structured logging
import structlog

logger = structlog.get_logger()

# Use structured logging with context
@app.post("/users")
async def create_user(user: CreateUserSchema, request: Request):
    logger.info("user_creation_started",
                email=user.email,
                ip=request.client.host)

    try:
        result = await prisma.user.create(data=user.dict())
        logger.info("user_created",
                    user_id=result.id,
                    email=result.email)
        return result
    except Exception as e:
        logger.error("user_creation_failed",
                     email=user.email,
                     error=str(e),
                     exc_info=True)
        raise
```

### Log Levels

```python
# Use appropriate log levels
logger.debug("Detailed debugging info", context=...)    # Development only
logger.info("Normal operation", context=...)            # Normal operations
logger.warning("Something unexpected", context=...)     # Recoverable issues
logger.error("Error occurred", context=...)            # Errors that don't crash
logger.critical("Critical failure", context=...)       # Serious failures

# DON'T use print()
print("User created")  # BAD

# DO use logger
logger.info("User created", user_id=user.id)  # GOOD
```

## Code Organization

### File Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── deps.py          # Dependencies
│   │   └── endpoints/       # Route handlers
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   ├── security.py      # Auth, crypto
│   │   └── logger.py        # Logging setup
│   ├── db/
│   │   └── database.py      # Database connection
│   ├── models/
│   │   └── user.py          # Data models
│   ├── schemas/
│   │   └── user.py          # Pydantic schemas
│   ├── services/
│   │   └── user_service.py  # Business logic
│   └── main.py              # App entry point
```

### Dependency Injection

```python
# Use FastAPI's Depends for dependencies
from fastapi import Depends

# In deps.py
async def get_db():
    async with db_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    payload = decode_token(token)
    user = await db.query(User).filter(User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# In endpoints
@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Configuration

### Environment-Based Config

```python
from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    # Application
    app_name: str = "DocPilot API"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str

    # Security
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # External services
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Usage
@app.on_event("startup")
async def startup():
    if settings.debug:
        logger.warning("Running in DEBUG mode - not suitable for production!")
```

## Testing

### Test Structure

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123!"
    }

# tests/test_users.py
class TestUsers:

    async def test_create_user(self, client: AsyncClient, test_user: dict):
        response = await client.post("/users", json=test_user)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user["email"]
        assert "id" in data
        assert "password_hash" not in data  # Never expose!

    async def test_create_duplicate_user(self, client: AsyncClient, test_user: dict):
        # First creation
        await client.post("/users", json=test_user)
        # Duplicate should fail
        response = await client.post("/users", json=test_user)
        assert response.status_code == 409

    async def test_get_user_requires_auth(self, client: AsyncClient):
        response = await client.get("/users/me")
        assert response.status_code == 401
```

### Database Tests

```python
# Use test database
@pytest.fixture
async def test_db():
    # Create test database
    await create_test_database()
    yield
    await drop_test_database()

async def test_user_creation(test_db):
    user = await prisma.user.create(data={
        "email": "test@example.com",
        "username": "test"
    })
    assert user.email == "test@example.com"
```

## Code Style

### PEP 8 Compliance

```python
# Install and configure tools
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Naming Conventions

```python
# Module: lowercase with underscores
user_service.py
database_utils.py

# Class: CapWords (PascalCase)
class UserService:
    pass

class DatabaseConnection:
    pass

# Function/variable: lowercase_with_underscores
def get_user_by_id(user_id: str):
    pass

user_name = "John"

# Constants: UPPER_WITH_UNDERSCORES
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Private: _leading_underscore
class MyClass:
    def __init__(self):
        self._internal_state = None
```

## Documentation

### Docstrings

```python
def get_user_projects(
    user_id: str,
    skip: int = 0,
    limit: int = 50,
    archived: bool = False
) -> List[Project]:
    """
    Retrieve projects for a specific user.

    Args:
        user_id: The UUID of the user to fetch projects for.
        skip: Number of projects to skip for pagination. Defaults to 0.
        limit: Maximum number of projects to return. Defaults to 50.
        archived: Include archived projects. Defaults to False.

    Returns:
        A list of Project objects belonging to the user.

    Raises:
        UserNotFoundError: If the user_id doesn't exist.
        DatabaseError: If there's a database connection issue.

    Example:
        >>> projects = get_user_projects("user-123", limit=10)
        >>> len(projects)
        10
    """
    pass
```

### API Documentation

```python
from fastapi import FastAPI, Query
from typing import List

@app.get(
    "/projects",
    response_model=List[ProjectResponse],
    summary="List all projects",
    description="Retrieve a paginated list of projects for the current user",
    responses={
        200: {"description": "Successful response"},
        401: {"description": "Not authenticated"},
        400: {"description": "Invalid pagination parameters"},
    },
    tags=["projects"]
)
async def list_projects(
    skip: int = Query(0, ge=0, description="Number of projects to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum projects to return"),
):
    """List projects with pagination"""
    pass
```

## Performance Best Practices

### Avoid Global State

```python
# BAD - Global state
cache = {}

def get_cached_data(key):
    return cache.get(key)

# GOOD - Dependency injection
class CacheService:
    def __init__(self):
        self._cache = {}

    def get(self, key: str):
        return self._cache.get(key)

@app.get("/data")
async def get_data(cache: CacheService = Depends()):
    return cache.get("key")
```

### Use Async Properly

```python
# BAD - Mixing sync and async
async def process_data():
    data = sync_function()  # Blocks!
    return await async_process(data)

# GOOD - All async
async def process_data():
    data = await async_get_data()
    return await async_process(data)
```
