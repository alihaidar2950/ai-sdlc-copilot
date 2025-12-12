"""
AI SDLC Co-Pilot - FastAPI Backend
==================================
MVP-Free Version ($0/month)

Endpoints:
- GET /health - Health check for Docker/monitoring
- GET /api/v1/status - API status and version info
"""

import logging
import os
import sys
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# =============================================================================
# Logging Configuration
# =============================================================================

def setup_logging() -> logging.Logger:
    """Configure structured logging for the application."""
    log_level = logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO

    # Create logger
    logger = logging.getLogger("ai_sdlc_copilot")
    logger.setLevel(log_level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Console handler with formatting
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # Format: timestamp - level - message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Initialize logger
logger = setup_logging()

# =============================================================================
# App Configuration
# =============================================================================

APP_NAME = "AI SDLC Co-Pilot"
APP_VERSION = "0.1.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="Automated test case generation, PR review, and defect creation using LLMs",
    version=APP_VERSION,
    docs_url="/docs" if DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if DEBUG else None,
)

# CORS middleware - allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Health & Status Endpoints
# =============================================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint for Docker and load balancers.
    Returns 200 OK if the service is running.
    """
    return {"status": "healthy"}


@app.get("/api/v1/status")
async def api_status():
    """
    API status endpoint with version and environment info.
    Useful for debugging and monitoring.
    """
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "environment": ENVIRONMENT,
        "debug": DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
    }


# =============================================================================
# Root Endpoint
# =============================================================================

@app.get("/")
async def root():
    """
    Root endpoint - redirects to docs or returns basic info.
    """
    return {
        "message": f"Welcome to {APP_NAME}",
        "version": APP_VERSION,
        "docs": "/docs" if DEBUG else "Docs disabled in production",
        "health": "/health",
        "api": "/api/v1/status",
    }


# =============================================================================
# Startup & Shutdown Events
# =============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    Initialize connections to external services.
    """
    logger.info(f"🚀 {APP_NAME} v{APP_VERSION} starting...")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.debug("Debug logging is enabled")
    # TODO: Initialize Supabase connection
    # TODO: Initialize Redis connection
    # TODO: Load prompt templates


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown.
    Clean up connections.
    """
    logger.info(f"👋 {APP_NAME} shutting down...")
    # TODO: Close database connections
    # TODO: Close Redis connection
