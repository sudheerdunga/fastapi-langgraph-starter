from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.chat import router as chat_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB tables, warm up models, etc.
    yield
    # Shutdown: Clean up connection pools, close sessions


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(chat_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}
