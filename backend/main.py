from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from datetime import datetime
from contextlib import asynccontextmanager
from database.config import get_db, Base
from env import run_migrations_online
from backend.routes.auth import router as auth_router
from backend.routes.documents import router as documents_router

app = FastAPI(
    title="PaperPal",
    description="AI-powered document processing and query application",
    version="1.0.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        run_migrations_online()  # Run database migrations
    except Exception as e:
        raise RuntimeError(f"Failed to run migrations: {str(e)}")
    yield
    # Shutdown logic (if any)
    pass

app.router.lifespan_context = lifespan

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(documents_router, prefix="/api")