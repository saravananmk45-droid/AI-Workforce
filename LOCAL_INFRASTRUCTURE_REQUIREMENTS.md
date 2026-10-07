# LOCAL INFRASTRUCTURE REQUIREMENTS
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** LIR-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** APPROVED  
**Target:** Local Docker Compose Environment  

---

## 1. INFRASTRUCTURE ARCHITECTURE OVERVIEW

To maintain 100% development parity with cloud staging and production without incurring external hosting costs, the local development environment runs containerized infrastructure orchestrated via `docker-compose.yml`.

---

## 2. SERVICE SPECIFICATIONS

### Service 1: PostgreSQL 16
- **Name**: `aiwf-postgres-dev`
- **Container Image**: `postgres:16-alpine`
- **Port**: `5432:5432`
- **Purpose**: Primary relational ACID database with Row-Level Security (RLS) and cryptographic extensions.
- **Persistent Storage**: Named volume `postgres_data` mapped to `/var/lib/postgresql/data`.
- **Health Check**:
  ```bash
  pg_isready -U aiwf_user -d aiwf_dev
  ```
  Interval: 5s, Timeout: 5s, Retries: 5.
- **Dependency Relationships**: Independent base datastore (Tier 1).
- **Required Environment Variables**:
  - `POSTGRES_DB`: `aiwf_dev`
  - `POSTGRES_USER`: `aiwf_user`
  - `POSTGRES_PASSWORD`: `dev_password_123`
- **Startup Order**: Stage 1 (Initial).
- **Shutdown Behavior**: `SIGTERM` with 30s grace period for active transactions to flush.

---

### Service 2: Redis 7.2
- **Name**: `aiwf-redis-dev`
- **Container Image**: `redis:7.2-alpine`
- **Port**: `6379:6379`
- **Purpose**: Distributed caching, atomic rate limiting, distributed lock manager, and Celery worker message broker.
- **Persistent Storage**: Named volume `redis_data` mapped to `/data` (`--appendonly yes`).
- **Health Check**:
  ```bash
  redis-cli ping
  ```
  Interval: 5s, Timeout: 3s, Retries: 5.
- **Dependency Relationships**: Independent base service (Tier 1).
- **Required Environment Variables**: None (standard CLI flags).
- **Startup Order**: Stage 1 (Initial).
- **Shutdown Behavior**: `SIGTERM` triggering AOF sync to disk.

---

### Service 3: Qdrant Vector Database
- **Name**: `aiwf-qdrant-dev`
- **Container Image**: `qdrant/qdrant:v1.9.0`
- **Port**: `6333:6333` (REST), `6334:6334` (gRPC)
- **Purpose**: High-performance vector index for document chunk embeddings and cosine similarity search.
- **Persistent Storage**: Named volume `qdrant_data` mapped to `/qdrant/storage`.
- **Health Check**:
  ```bash
  curl -f http://localhost:6333/readyz
  ```
  Interval: 10s, Timeout: 5s, Retries: 3.
- **Dependency Relationships**: Independent base service (Tier 1).
- **Required Environment Variables**: None for unauthenticated local development.
- **Startup Order**: Stage 1 (Initial).
- **Shutdown Behavior**: Graceful shutdown waiting for WAL flush.

---

### Service 4: MinIO (S3-Compatible Object Storage)
- **Name**: `aiwf-minio-dev`
- **Container Image**: `minio/minio:RELEASE.2024-03-30T09-41-56Z`
- **Port**: `9000:9000` (S3 API), `9001:9001` (Web Console)
- **Purpose**: S3-compatible document storage for tenant files, knowledge source uploads, and trace archives.
- **Persistent Storage**: Named volume `minio_data` mapped to `/data`.
- **Health Check**:
  ```bash
  curl -f http://localhost:9000/minio/health/live
  ```
- **Dependency Relationships**: Independent base service (Tier 1).
- **Required Environment Variables**:
  - `MINIO_ROOT_USER`: `minio_admin`
  - `MINIO_ROOT_PASSWORD`: `minio_password_123`
- **Startup Order**: Stage 1 (Initial).
- **Shutdown Behavior**: Flush buffered writes to disk.

---

### Service 5: Core API Backend
- **Name**: `aiwf-api-dev`
- **Container Image**: Built from `./backend/Dockerfile`
- **Port**: `8000:8000`
- **Purpose**: FastAPI REST and SSE API gateway.
- **Persistent Storage**: Ephemeral container, reads environment from `.env`.
- **Health Check**:
  ```bash
  curl -f http://localhost:8000/v1/healthz
  ```
- **Dependency Relationships**: Depends on `postgres` (healthy), `redis` (healthy), `qdrant`, `minio`.
- **Startup Order**: Stage 2 (Post-Datastores).
- **Shutdown Behavior**: Uvicorn graceful shutdown of worker threads.

---

### Service 6: Celery Background Worker
- **Name**: `aiwf-worker-dev`
- **Container Image**: Built from `./backend/Dockerfile.worker`
- **Port**: None (internal process).
- **Purpose**: Executes asynchronous workflows, cyclic agent loops, and tool invocations.
- **Persistent Storage**: Ephemeral.
- **Dependency Relationships**: Depends on `postgres` (healthy), `redis` (healthy).
- **Startup Order**: Stage 2 (Post-Datastores).
- **Shutdown Behavior**: Celery `warm shutdown` waiting for running tasks to complete.

---

## 3. ORCHESTRATION SUMMARY MATRIX

| Order | Service Name | Container Name | Port(s) | Status Check | Volume |
|:---:|---|---|---|---|---|
| **1** | PostgreSQL | `aiwf-postgres-dev` | 5432 | `pg_isready` | `postgres_data` |
| **1** | Redis | `aiwf-redis-dev` | 6379 | `redis-cli ping` | `redis_data` |
| **1** | Qdrant | `aiwf-qdrant-dev` | 6333, 6334 | `/readyz` | `qdrant_data` |
| **1** | MinIO | `aiwf-minio-dev` | 9000, 9001 | `/minio/health/live` | `minio_data` |
| **2** | Core API | `aiwf-api-dev` | 8000 | `/v1/healthz` | None |
| **2** | Worker | `aiwf-worker-dev` | None | Process status | None |
