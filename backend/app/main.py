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
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pytest_router, testcases

# Load .env from project root (one level up from backend/)
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

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


# =============================================================================
# Lifespan Context Manager (replaces on_event decorators)
# =============================================================================


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for startup and shutdown events.
    Modern replacement for deprecated @app.on_event decorators.
    """
    # Startup
    logger.info(f"🚀 {APP_NAME} v{APP_VERSION} starting...")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Debug mode: {DEBUG}")
    logger.debug("Debug logging is enabled")
    # TODO: Initialize Supabase connection
    # TODO: Initialize Redis connection
    # TODO: Load prompt templates

    yield  # App runs here

    # Shutdown
    logger.info(f"👋 {APP_NAME} shutting down...")
    # TODO: Close database connections
    # TODO: Close Redis connection


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    description="Automated test case generation, PR review, and defect creation using LLMs",
    version=APP_VERSION,
    docs_url="/docs" if DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if DEBUG else None,
    lifespan=lifespan,
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

# Include routers
app.include_router(testcases.router)
app.include_router(pytest_router.router)


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
        "timestamp": datetime.now(UTC).isoformat(),
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
# LLM Test Endpoint
# =============================================================================


@app.post("/api/v1/llm/test")
async def test_llm(prompt: str = "Say hello in one sentence."):
    """
    Test LLM integration.
    Sends a simple prompt and returns the response.
    """
    from app.services.llm_service import get_llm_service

    try:
        llm = get_llm_service()
        response = await llm.generate(prompt)
        return {
            "success": True,
            "prompt": prompt,
            "response": response,
        }
    except Exception as e:
        logger.error(f"LLM test failed: {e}")
        return {
            "success": False,
            "prompt": prompt,
            "error": str(e),
        }
