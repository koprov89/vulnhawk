"""Main FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes
from app.database import engine, Base
from app.config import settings

# Create FastAPI application
app = FastAPI(
    title="VulnHawk API",
    description="Network Vulnerability Scanner API",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(routes.router, prefix="/api")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "VulnHawk"}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to VulnHawk API",
        "version": "0.1.0",
        "docs_url": "/docs"
    }
