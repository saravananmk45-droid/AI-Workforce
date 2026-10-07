"""
AI Workforce Platform — Core API Gateway
FastAPI Application Entry Point & Pre-Development Health Endpoints
OpenAPI 3.1 & Swagger UI compliant
"""

import os
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Workforce Platform — Core API Gateway",
    description="Autonomous Business Workflow Automation Platform REST & SSE API Gateway",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/v1/openapi.json",
)

# Configure CORS
origins_env = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173")
origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """Root platform discovery endpoint."""
    return {
        "service": "AI Workforce Platform — Core API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/v1/healthz",
    }


@app.get("/v1/healthz", tags=["Observability"])
async def health_check() -> dict[str, Any]:
    """
    Liveness probe returning platform runtime environment and service health status.
    """
    return {
        "status": "HEALTHY",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0",
        "services": {
            "api": "UP",
            "database": "CONFIGURED",
            "redis": "CONFIGURED",
            "qdrant": "CONFIGURED",
            "object_storage": "CONFIGURED",
        },
    }


@app.get("/v1/healthz/ready", tags=["Observability"])
async def readiness_check() -> dict[str, str]:
    """
    Readiness probe for container orchestration.
    """
    return {"status": "READY"}
