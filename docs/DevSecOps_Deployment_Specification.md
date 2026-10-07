# DEVSECOPS & DEPLOYMENT SPECIFICATION
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** DSO-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** FINAL & APPROVED  
**Target Environments:** Local Docker Compose, Kubernetes (EKS / GKE)  
**Compliance Standards:** SOC 2 Type II, GDPR, CIS Benchmark Hardened  

---

## TABLE OF CONTENTS
1. [DevSecOps Principles & Governance](#1-devsecops-principles--governance)
2. [Physical & Logical Environment Isolation](#2-physical--logical-environment-isolation)
3. [Containerization & Docker Architecture](#3-containerization--docker-architecture)
   - 3.1 [Core API Backend Dockerfile](#31-core-api-backend-dockerfile)
   - 3.2 [Web Frontend SPA Dockerfile](#32-web-frontend-spa-dockerfile)
   - 3.3 [Worker & Sandbox Dockerfile](#33-worker--sandbox-dockerfile)
4. [Docker Compose Architecture (Local Development)](#4-docker-compose-architecture-local-development)
5. [CI/CD Pipeline Architecture (GitHub Actions)](#5-cicd-pipeline-architecture-github-actions)
   - 5.1 [Stage 1: Code Quality, Lint & Type Check](#51-stage-1-code-quality-lint--type-check)
   - 5.2 [Stage 2: Unit & Integration Test Matrix](#52-stage-2-unit--integration-test-matrix)
   - 5.3 [Stage 3: Security & Vulnerability Scanning (SAST/DAST)](#53-stage-3-security--vulnerability-scanning-sastdast)
   - 5.4 [Stage 4: Container Build & Image Signing](#54-stage-4-container-build--image-signing)
   - 5.5 [Stage 5: Automated Staging Deployment & E2E Validation](#55-stage-5-automated-staging-deployment--e2e-validation)
   - 5.6 [Stage 6: Production Blue/Green Deployment & Canary](#56-stage-6-production-bluegreen-deployment--canary)
6. [Database Migration Execution & Rollback Engine](#6-database-migration-execution--rollback-engine)
7. [Secret Management & KMS Envelope Encryption](#7-secret-management--kms-envelope-encryption)
8. [Health Probes, Observability & Self-Healing](#8-health-probes-observability--self-healing)
9. [Backup, Disaster Recovery & Zero-Data-Loss Strategy](#9-backup-disaster-recovery--zero-data-loss-strategy)

---

## 1. DEVSECOPS PRINCIPLES & GOVERNANCE

1. **Shift-Left Security**: Vulnerability, dependency, and static analysis scans execute on every pull request. No code merges without passing automated security gates.
2. **Immutability of Artifacts**: The exact container image digest validated in Staging is promoted to Production. Images are never recompiled between environments.
3. **Least Privilege Runtime**: Containers execute as non-root users (`USER appuser`, UID 10001) with read-only root filesystems and dropped Linux capabilities (`cap_drop: ALL`).
4. **Zero Test Data in Production**: The production database (`aiwf_prod`) never hosts test fixtures, demo organizations, or simulated runs. Ephemeral test databases are used during CI.

---

## 2. PHYSICAL & LOGICAL ENVIRONMENT ISOLATION

Strict separation between environments is enforced at network, credential, database, and object storage layers:

| Dimension | Development (`dev`) | Testing / CI (`test`) | Staging (`stage`) | Production (`prod`) |
|---|---|---|---|---|
| **Cluster / Host** | Local Workstation / Docker | Ephemeral GitHub Runner | Dedicated Staging K8s Cluster | Multi-AZ High-Availability K8s |
| **PostgreSQL DB** | Local `aiwf_dev` instance | In-memory / Ephemeral container | Managed RDS `aiwf-stage-db` | Multi-AZ Managed RDS `aiwf-prod-db` |
| **Vector DB (Qdrant)**| Local Qdrant (Single Node) | Ephemeral Qdrant test instance | Dedicated Staging Qdrant Node | Distributed Qdrant Cluster (Multi-AZ) |
| **Redis** | Local Redis 7 Container | Ephemeral Redis test instance | Managed ElastiCache (Staging) | Managed ElastiCache Cluster (HA) |
| **Object Storage** | Local MinIO Container | In-memory Mock Storage | S3 `aiwf-stage-assets` | Multi-Region KMS Encrypted S3 |
| **LLM Provider Keys** | Personal Sandbox / Mock Keys | WireMock / VCR.py replay (Zero Live API Hits) | Vendor Sandbox Accounts | Verified Tenant BYOK Credentials |
| **Data Purity Rule** | Seed fixtures allowed | Ephemeral fixtures created & destroyed | Sanitized masked replicas | **Zero test data / Zero mock accounts** |

---

## 3. CONTAINERIZATION & DOCKER ARCHITECTURE

### 3.1 Core API Backend Dockerfile

Multi-stage build minimizing attack surface, utilizing non-root security context:

```dockerfile
# Stage 1: Build & Dependency Resolution
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Hardened Runtime Container
FROM python:3.11-slim-bookworm AS runner

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged system user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/false -m appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup ./src /app/src

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/v1/healthz || exit 1

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 3.2 Web Frontend SPA Dockerfile

```dockerfile
# Stage 1: Build Application Bundle
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --prefer-offline --no-audit

COPY . .
RUN npm run build

# Stage 2: Hardened Nginx Web Server
FROM nginx:1.25-alpine AS runner

# Drop root privilege in Nginx
RUN chown -R nginx:nginx /var/cache/nginx /var/run /var/log/nginx
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

USER nginx
EXPOSE 8080

HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD wget -q --spider http://localhost:8080/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### 3.3 Worker & Sandbox Dockerfile

```dockerfile
FROM python:3.11-slim-bookworm

WORKDIR /worker
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/false -m appuser

COPY requirements-worker.txt .
RUN pip install --no-cache-dir -r requirements-worker.txt

COPY --chown=appuser:appgroup ./worker /worker

USER appuser
ENTRYPOINT ["celery", "-A", "worker.tasks", "worker", "--loglevel=INFO", "--concurrency=8"]
```

---

## 4. DOCKER COMPOSE ARCHITECTURE (LOCAL DEVELOPMENT)

Local development orchestration file (`docker-compose.yml`):

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: aiwf-postgres-dev
    environment:
      POSTGRES_DB: aiwf_dev
      POSTGRES_USER: aiwf_user
      POSTGRES_PASSWORD: dev_password_123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U aiwf_user -d aiwf_dev"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.2-alpine
    container_name: aiwf-redis-dev
    command: ["redis-server", "--appendonly", "yes"]
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  qdrant:
    image: qdrant/qdrant:v1.9.0
    container_name: aiwf-qdrant-dev
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/readyz"]
      interval: 10s
      timeout: 5s
      retries: 3

  minio:
    image: minio/minio:RELEASE.2024-03-30T09-41-56Z
    container_name: aiwf-minio-dev
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minio_admin
      MINIO_ROOT_PASSWORD: minio_password_123
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: aiwf-api-dev
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://aiwf_user:dev_password_123@postgres:5432/aiwf_dev
      - REDIS_URL=redis://redis:6379/0
      - QDRANT_URL=http://qdrant:6333
      - S3_ENDPOINT_URL=http://minio:9000
      - S3_ACCESS_KEY=minio_admin
      - S3_SECRET_KEY=minio_password_123
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  minio_data:
```

---

## 5. CI/CD PIPELINE ARCHITECTURE (GITHUB ACTIONS)

```
[Git Push / PR]
       │
       ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 1: Code Quality & Static Analysis               │
│ • Ruff / ESLint (Zero warnings)                        │
│ • TypeScript / MyPy Strict Type Checking               │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 2: Security & Vulnerability Scanning             │
│ • Semgrep SAST & GitGuardian Secret Detection          │
│ • Trivy Container Vulnerability Scan (Zero CRITICAL)   │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 3: Test Matrix Execution                         │
│ • Unit Tests (Pytest / Vitest) -> Coverage >= 85%      │
│ • Integration Tests against Ephemeral Containers       │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 4: Build, Tag & Sign Container Images            │
│ • Multi-stage Docker Build                             │
│ • Push to AWS ECR with Git SHA tag                     │
│ • Cosign Container Image Signature                     │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 5: Staging Deployment & Playwright E2E           │
│ • Apply Helm Chart to Staging K8s                      │
│ • Execute Synthetic E2E Regression Suite               │
└───────────────────────┬────────────────────────────────┘
                        │ (Manual Approval Gate)
                        ▼
┌────────────────────────────────────────────────────────┐
│ STAGE 6: Production Blue/Green Deployment              │
│ • Rolling / Canary update (10% -> 50% -> 100%)         │
│ • Automated Rollback on 5xx Error Rate Spike           │
└────────────────────────────────────────────────────────┘
```

---

## 6. DATABASE MIGRATION EXECUTION & ROLLBACK ENGINE

1. **Pre-Deployment Execution**: Migrations run as a Kubernetes `Job` prior to rolling out updated application pods.
2. **Backward Compatibility Rule**: Migrations must follow the **Expand/Contract pattern**:
   - *Phase 1 (Expand)*: Add new columns as nullable; deploy code that writes to both old and new columns.
   - *Phase 2 (Contract)*: Backfill historical data; deploy code reading only new column; drop deprecated column in subsequent release.
3. **Automated Rollback Safeguard**: If a migration script fails, the transaction is rolled back, the deployment pipeline halts, and existing pods continue running against the unaffected schema.

---

## 7. SECRET MANAGEMENT & KMS ENVELOPE ENCRYPTION

- **Platform Secrets**: Managed via AWS Secrets Manager or HashiCorp Vault. Injected at container runtime via Kubernetes CSI Secret Driver.
- **Tenant BYOK Keys**:
  - Encrypted using **AES-256-GCM** authenticated envelope encryption.
  - The Data Encryption Key (DEK) is generated per secret and wrapped with a Master Key residing in **AWS KMS** (`kms:Encrypt`, `kms:Decrypt`).
  - Stored in `encrypted_secrets` table. Decrypted values reside strictly in volatile worker memory and are never written to disk, swap, or logs.

---

## 8. HEALTH PROBES, OBSERVABILITY & SELF-HEALING

- **Liveness Probe**:
  - Path: `/v1/healthz`
  - Period: 10s, Timeout: 3s, Failure Threshold: 3.
  - Action: Pod restarted if process hangs or deadlocks.
- **Readiness Probe**:
  - Path: `/v1/readyz`
  - Period: 10s, Timeout: 5s, Failure Threshold: 2.
  - Validates PostgreSQL connection pool, Redis ping, and Qdrant readiness.
  - Action: Pod removed from load balancer rotation until healthy.

---

## 9. BACKUP, DISASTER RECOVERY & ZERO-DATA-LOSS STRATEGY

1. **PostgreSQL Point-in-Time Recovery (PITR)**:
   - AWS RDS Automated Snapshots daily (30-day retention).
   - Write-Ahead Logs (WAL) continuously streamed to S3, enabling restoration to any minute within the last 30 days.
2. **Qdrant Vector Snapshots**:
   - Nightly collection snapshots automatically uploaded to S3 bucket `aiwf-backups-qdrant`.
3. **Disaster Recovery Targets**:
   - **RPO (Recovery Point Objective)**: $\le 15 \text{ minutes}$ (guaranteed by continuous WAL archiving).
   - **RTO (Recovery Time Objective)**: $\le 2 \text{ hours}$ (automated Terraform cold infrastructure spin-up).

---

*End of DevSecOps & Deployment Specification*  
*Document Version: 1.0.0 | Status: FINAL & APPROVED*
