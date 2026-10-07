# ENVIRONMENT CONFIGURATION REQUIREMENTS
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** ENV-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** FINAL & APPROVED  
**Classification:** Confidential — Platform Engineering  

---

## TABLE OF CONTENTS
1. [Overview & Secret Governance Principles](#1-overview--secret-governance-principles)
2. [Variable Classification Matrix](#2-variable-classification-matrix)
3. [Core Application & Server Configuration](#3-core-application--server-configuration)
4. [Database & Persistence Layer (PostgreSQL)](#4-database--persistence-layer-postgresql)
5. [Cache, Lock & Message Broker (Redis)](#5-cache-lock--message-broker-redis)
6. [Vector Database (Qdrant)](#6-vector-database-qdrant)
7. [Blob & Document Object Storage (S3 / MinIO)](#7-blob--document-object-storage-s3--minio)
8. [Security, Cryptography & KMS Vault](#8-security-cryptography--kms-vault)
9. [JWT, Session & Authentication](#9-jwt-session--authentication)
10. [AI Gateway & Platform Fallback Keys](#10-ai-gateway--platform-fallback-keys)
11. [Third-Party OAuth & Single Sign-On (SSO)](#11-third-party-oauth--single-sign-on-sso)
12. [Transactional Email & Notifications (SMTP / SendGrid)](#12-transactional-email--notifications-smtp--sendgrid)
13. [Observability, Telemetry & Traces (Langfuse / OpenTelemetry)](#13-observability-telemetry--traces-langfuse--opentelemetry)
14. [Webhooks & Signature Verification](#14-webhooks--signature-verification)
15. [Frontend Client Environment Variables](#15-frontend-client-environment-variables)
16. [Environment-Specific Resolution Table](#16-environment-specific-resolution-table)

---

## 1. OVERVIEW & SECRET GOVERNANCE PRINCIPLES

1. **Zero Secret Commitment**: Under no circumstances shall real passwords, API tokens, private keys, or credentials be committed to git repositories, Docker images, or documentation.
2. **Runtime Injection**: All secrets in Staging and Production are injected at runtime via Kubernetes Secrets or AWS Secrets Manager.
3. **Public vs Secret Boundary**: Variables prefixed with `VITE_` or `NEXT_PUBLIC_` are bundled into client-side JavaScript and are considered public. No sensitive credentials may ever carry these prefixes.
4. **Environment Divergence**: Every variable has distinct values across Development, Testing, Staging, and Production.

---

## 2. VARIABLE CLASSIFICATION MATRIX

| Variable Name | Sensitivity | Layer | Dev Default | Production Source |
|---|---|---|---|---|
| `ENVIRONMENT` | Public | Core | `development` | K8s ConfigMap |
| `DATABASE_URL` | **Secret** | Persistence | `postgresql://aiwf_user:...@localhost:5432/aiwf_dev` | AWS RDS / Secrets Manager |
| `REDIS_URL` | **Secret** | Cache | `redis://localhost:6379/0` | AWS ElastiCache |
| `QDRANT_URL` | Public / Internal | Vector | `http://localhost:6333` | Internal K8s Service |
| `QDRANT_API_KEY` | **Secret** | Vector | (None for local) | Secrets Manager |
| `MASTER_ENCRYPTION_KEY` | **Critical Secret** | Security | 32-byte hex generated locally | AWS KMS Key Alias |
| `JWT_SECRET_KEY` | **Critical Secret** | IAM | 64-byte random string | Secrets Manager |
| `PLATFORM_OPENAI_API_KEY` | **Secret** | AI Gateway | `sk-mock-dev-key` | OpenAI Developer Console |
| `LANGFUSE_SECRET_KEY` | **Secret** | Observability | (Optional local) | Langfuse Cloud Dashboard |

---

## 3. CORE APPLICATION & SERVER CONFIGURATION

### `ENVIRONMENT`
- **Purpose**: Defines active runtime environment (`development`, `test`, `staging`, `production`).
- **Sensitivity**: Public | **Required**: Yes
- **Dev**: `development` | **Test**: `test` | **Prod**: `production`

### `PORT`
- **Purpose**: HTTP listen port for backend API service.
- **Sensitivity**: Public | **Required**: Yes (Default: `8000`)

### `CORS_ALLOWED_ORIGINS`
- **Purpose**: Comma-separated list of allowed frontend origins for CORS headers.
- **Sensitivity**: Public | **Required**: Yes
- **Dev**: `http://localhost:3000,http://localhost:5173` | **Prod**: `https://app.aiworkforce.io`

---

## 4. DATABASE & PERSISTENCE LAYER (POSTGRESQL)

### `DATABASE_URL`
- **Purpose**: Fully qualified PostgreSQL connection URI with credentials and connection pool params.
- **Sensitivity**: **Secret** | **Required**: Yes
- **Format**: `postgresql://[user]:[password]@[host]:[port]/[database]?sslmode=[mode]`
- **Dev**: `postgresql://aiwf_user:dev_password_123@localhost:5432/aiwf_dev`
- **Prod**: `postgresql://app_user:[SECRET]@aiwf-prod-cluster.rds.amazonaws.com:5432/aiwf_prod?sslmode=verify-full`

### `DATABASE_POOL_SIZE`
- **Purpose**: Maximum connections maintained in application connection pool.
- **Sensitivity**: Public | **Required**: Yes (Default: `20`)

---

## 5. CACHE, LOCK & MESSAGE BROKER (REDIS)

### `REDIS_URL`
- **Purpose**: Connection URI for Redis instance used for locks, rate limiting, and BullMQ queues.
- **Sensitivity**: **Secret** | **Required**: Yes
- **Dev**: `redis://localhost:6379/0`
- **Prod**: `rediss://:[SECRET]@aiwf-redis.elasticache.us-east-1.amazonaws.com:6379/0`

---

## 6. VECTOR DATABASE (QDRANT)

### `QDRANT_URL`
- **Purpose**: REST/gRPC endpoint for Qdrant vector database.
- **Sensitivity**: Public / Internal | **Required**: Yes
- **Dev**: `http://localhost:6333` | **Prod**: `https://qdrant.aiworkforce.internal:6333`

### `QDRANT_API_KEY`
- **Purpose**: Authentication token for Qdrant API.
- **Sensitivity**: **Secret** | **Required**: Optional in local dev, Required in Prod.

---

## 7. BLOB & DOCUMENT OBJECT STORAGE (S3 / MINIO)

### `S3_ENDPOINT_URL`
- **Purpose**: Custom S3 endpoint (configured for local MinIO; omitted when using AWS S3).
- **Sensitivity**: Public | **Required**: Dev only (`http://localhost:9000`)

### `S3_BUCKET_DOCUMENTS`
- **Purpose**: S3 bucket name designated for uploaded tenant knowledge documents.
- **Sensitivity**: Public | **Required**: Yes
- **Dev**: `aiwf-dev-documents` | **Prod**: `aiwf-prod-documents-useast1`

### `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`
- **Purpose**: IAM credentials authorized for S3 object operations.
- **Sensitivity**: **Secret** | **Required**: Yes

---

## 8. SECURITY, CRYPTOGRAPHY & KMS VAULT

### `MASTER_ENCRYPTION_KEY`
- **Purpose**: 256-bit AES Master Key used to wrap tenant credentials when AWS KMS is not utilized (dev mode).
- **Sensitivity**: **Critical Secret** | **Required**: Yes (Dev: generated via `openssl rand -hex 32`)

### `AWS_KMS_KEY_ID`
- **Purpose**: AWS KMS Key ARN utilized for hardware envelope encryption of tenant BYOK secrets in production.
- **Sensitivity**: **Secret** | **Required**: Production only.

---

## 9. JWT, SESSION & AUTHENTICATION

### `JWT_SECRET_KEY`
- **Purpose**: Cryptographic secret utilized to sign HMAC-SHA256 session tokens.
- **Sensitivity**: **Critical Secret** | **Required**: Yes (Dev: `openssl rand -base64 64`)

### `JWT_ACCESS_EXPIRATION_MINUTES`
- **Purpose**: Lifespan of access token (Default: `60` minutes).

### `JWT_REFRESH_EXPIRATION_DAYS`
- **Purpose**: Lifespan of refresh token (Default: `30` days).

---

## 10. AI GATEWAY & PLATFORM FALLBACK KEYS

### `PLATFORM_OPENAI_API_KEY`
- **Purpose**: Platform-managed OpenAI API key utilized strictly for Starter tier metered trials and evaluation fallback.
- **Sensitivity**: **Secret** | **Required**: Yes in Prod.

### `PLATFORM_ANTHROPIC_API_KEY`
- **Purpose**: Platform-managed Anthropic API key utilized for platform fallback.
- **Sensitivity**: **Secret** | **Required**: Optional.

---

## 11. THIRD-PARTY OAUTH & SINGLE SIGN-ON (SSO)

### `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`
- **Purpose**: Google OAuth 2.0 web client credentials for SSO login.
- **Sensitivity**: Client ID (Public), Secret (**Secret**).

---

## 12. TRANSACTIONAL EMAIL & NOTIFICATIONS

### `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD`
- **Purpose**: Outbound transactional SMTP configuration for invitation emails and approval alerts.
- **Sensitivity**: **Secret** | **Required**: Optional in Dev (logs to stdout), Required in Prod.

---

## 13. OBSERVABILITY, TELEMETRY & TRACES

### `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_HOST`
- **Purpose**: API credentials for Langfuse AI tracing and LLM step inspection.
- **Sensitivity**: Secret Key (**Secret**), Public Key (Public).

### `OTEL_EXPORTER_OTLP_ENDPOINT`
- **Purpose**: OpenTelemetry gRPC/HTTP collector endpoint for distributed tracing.
- **Sensitivity**: Public / Internal.

---

## 14. WEBHOOKS & SIGNATURE VERIFICATION

### `WEBHOOK_SIGNING_SECRET`
- **Purpose**: Master HMAC secret used to sign outbound notification payloads dispatched to tenant endpoints.
- **Sensitivity**: **Secret** | **Required**: Yes.

---

## 15. FRONTEND CLIENT ENVIRONMENT VARIABLES

Variables exposed to the browser build bundle:

| Variable Name | Description | Default Dev Value |
|---|---|---|
| `VITE_API_BASE_URL` | Base endpoint URL for the backend API | `http://localhost:8000/v1` |
| `VITE_APP_NAME` | Display name of the platform | `AI Workforce` |
| `VITE_ENABLE_ANALYTICS` | Feature toggle for frontend telemetry | `false` |

---

## 16. ENVIRONMENT-SPECIFIC RESOLUTION TABLE

| Variable | Local Dev (`.env`) | CI Pipeline (`test`) | Production (`prod`) |
|---|---|---|---|
| `ENVIRONMENT` | `development` | `test` | `production` |
| `DATABASE_URL` | `postgresql://aiwf_user:dev_password_123@localhost:5432/aiwf_dev` | `postgresql://test:test@localhost:5432/aiwf_test` | Injected via AWS Secrets Manager |
| `REDIS_URL` | `redis://localhost:6379/0` | `redis://localhost:6379/1` | Injected via ElastiCache Auth Token |
| `QDRANT_URL` | `http://localhost:6333` | `http://localhost:6333` | Private VPC Cluster Endpoint |
| `S3_ENDPOINT_URL` | `http://localhost:9000` | Mock S3 | *Omitted (uses standard AWS S3)* |

---

*End of Environment Configuration Requirements*  
*Document Version: 1.0.0 | Status: FINAL & APPROVED*
