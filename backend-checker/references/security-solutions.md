# Backend Security Solutions

Common security vulnerabilities and their fixes for FastAPI/Python applications.

## SQL Injection

### Problem
User input directly interpolated into SQL queries.

```python
# VULNERABLE
@app.get("/users/{username}")
def get_user(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# SAFE - Parameterized queries
@app.get("/users/{username}")
def get_user(username: str):
    return db.query(User).filter(User.username == username).first()

# SAFE - Prisma with parameters
result = await prisma.user.find_first(where={"username": username})
```

## Authentication Issues

### Missing Authentication on Endpoints

```python
# VULNERABLE
@app.get("/admin/users")
def list_all_users():
    return db.query(User).all()

# SAFE - Require auth
from fastapi import Depends, HTTPException, status
from .auth import get_current_user, require_admin

@app.get("/admin/users")
def list_all_users(current_user = Depends(require_admin)):
    return db.query(User).all()
```

### JWT Without Expiration

```python
# VULNERABLE - Token never expires
token = jwt.encode({"user_id": user.id}, SECRET_KEY)

# SAFE - Add expiration
token = jwt.encode(
    {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=24)},
    SECRET_KEY
)

# SAFER - Use refresh tokens
access_token = create_access_token(data={"sub": user.id}, expires_delta=timedelta(minutes=15))
refresh_token = create_refresh_token(data={"sub": user.id}, expires_delta=timedelta(days=7))
```

## Authorization Bypass

### Path Traversal

```python
# VULNERABLE
@app.get("/files/{filename}")
def get_file(filename: str):
    return FileResponse(f"uploads/{filename}")  # Can access ../../etc/passwd

# SAFE - Validate and sanitize
from pathlib import Path
import os

@app.get("/files/{filename}")
def get_file(filename: str):
    # Remove directory traversal attempts
    clean_filename = os.path.basename(filename)
    file_path = Path("uploads") / clean_filename

    # Ensure path is within uploads directory
    if not str(file_path.resolve()).startswith(str(Path("uploads").resolve())):
        raise HTTPException(status_code=403, detail="Access denied")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
```

### IDOR (Insecure Direct Object Reference)

```python
# VULNERABLE - Anyone can access any order
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

# SAFE - Verify ownership
@app.get("/orders/{order_id}")
def get_order(order_id: int, current_user = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return order
```

## Sensitive Data Exposure

### Passwords in Logs

```python
# VULNERABLE
logger.info(f"User login: {username}, password: {password}")

# SAFE - Never log sensitive data
logger.info(f"User login attempt: {username}")

# BEST - Sanitize before logging
from logging import Filter

class SensitiveDataFilter(Filter):
    def filter(self, record):
        record.msg = str(record.msg).replace(password, "***")
        return True
```

### Hardcoded Secrets

```python
# VULNERABLE
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "admin123"

# SAFE - Use environment variables
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    db_password: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### Leaking Stack Traces

```python
# VULNERABLE - Exposes internal structure
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": traceback.format_exc()}
    )

# SAFE - Generic error in production
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Exception: {exc}", exc_info=True)
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={"error": str(exc), "traceback": traceback.format_exc()}
        )
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

## CORS Misconfiguration

```python
# VULNERABLE - Allows any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SAFE - Specific origins with validation
ALLOWED_ORIGINS = [
    "https://example.com",
    "https://app.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

## Rate Limiting

```python
# Add rate limiting to prevent abuse
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(request: Request, credentials: LoginSchema):
    # ...
```

## Input Validation

```python
# Use Pydantic for validation
from pydantic import BaseModel, EmailStr, Field, validator

class CreateUserSchema(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    password: str = Field(..., min_length=8)

    @validator("password")
    def password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v

@app.post("/users")
async def create_user(user: CreateUserSchema):
    # Already validated
    pass
```

## Dependency Vulnerabilities

Regularly update dependencies:

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update requirements
pip-compile requirements.in --upgrade
```

## File Upload Security

```python
import uuid
from pathlib import Path
import imghdr

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Validate file size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="File type not allowed")

    # Validate actual content (not just extension)
    img_type = imghdr.what(None, h=content)
    if img_type not in ["jpeg", "png", "gif"]:
        raise HTTPException(status_code=415, detail="Invalid image")

    # Generate safe filename
    safe_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = Path("uploads") / safe_filename

    with open(file_path, "wb") as f:
        f.write(content)

    return {"filename": safe_filename}
```
