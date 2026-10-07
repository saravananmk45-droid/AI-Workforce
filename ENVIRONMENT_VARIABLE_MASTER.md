# ENVIRONMENT VARIABLE MASTER INVENTORY
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** EVM-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** COMPLETE & AUDITED  
**Governance:** Zero Secret Hardcoding | Strict Runtime Injection  

---

## 1. GOVERNANCE & SENSITIVITY CLASSIFICATION

Every environment variable required across all 23 platform domains is documented below. Variables are categorized by sensitivity:
- **PUBLIC**: Safe for inclusion in client-side bundles (`VITE_` prefix) or system documentation.
- **SECRET**: Sensitive credentials; must never appear in frontend bundles, logs, or unencrypted storage.
- **CRITICAL SECRET**: Cryptographic signing keys and master wrapping keys; compromised keys invalidate entire security domains.

---

## 2. COMPREHENSIVE ENVIRONMENT VARIABLE SPECIFICATION

### Domain 1: Application Server Core
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `ENVIRONMENT` |
| **TYPE** | String (`development` \| `test` \| `staging` \| `production`) |
| **REQ / OPT** | Required |
| **PURPOSE** | Controls application runtime mode, log verbosity, and safety guardrails |
| **USED BY** | Core API Backend, Celery Worker |
| **LOCAL DEV** | `development` |
| **STAGING** | `staging` |
| **PRODUCTION** | `production` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `development` |
| **WHERE TO OBTAIN** | Configured in deployment manifest |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `PORT` |
| **TYPE** | Integer |
| **REQ / OPT** | Required (Default: `8000`) |
| **PURPOSE** | HTTP listen port for the FastAPI gateway server |
| **USED BY** | Uvicorn / Core API |
| **LOCAL DEV** | `8000` |
| **STAGING** | `8000` |
| **PRODUCTION** | `8000` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `8000` |
| **WHERE TO OBTAIN** | Local config / Dockerfile EXPOSE |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `CORS_ALLOWED_ORIGINS` |
| **TYPE** | Comma-separated String |
| **REQ / OPT** | Required |
| **PURPOSE** | Permitted origins for Cross-Origin Resource Sharing (CORS) preflight validation |
| **USED BY** | FastAPI CORS Middleware |
| **LOCAL DEV** | `http://localhost:3000,http://localhost:5173` |
| **STAGING** | `https://stage-app.aiworkforce.io` |
| **PRODUCTION** | `https://app.aiworkforce.io` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `http://localhost:3000,http://localhost:5173` |
| **WHERE TO OBTAIN** | Domain registrar / ingress DNS config |
| **ROTATION** | Upon domain changes |

---

### Domain 2: Relational Database (PostgreSQL)
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `DATABASE_URL` |
| **TYPE** | URI String |
| **REQ / OPT** | Required |
| **PURPOSE** | Fully qualified connection string for primary transactional database with RLS |
| **USED BY** | SQLAlchemy 2.0 Engine, Alembic Migrations |
| **LOCAL DEV** | `postgresql+asyncpg://aiwf_user:dev_password_123@localhost:5432/aiwf_dev` |
| **STAGING** | `postgresql+asyncpg://app:[STG_SECRET]@aiwf-stage-db.internal:5432/aiwf_stage?ssl=require` |
| **PRODUCTION** | Injected via AWS Secrets Manager |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | Safe local dev credentials provided in `.env.example` |
| **WHERE TO OBTAIN** | Local Docker Compose / Cloud RDS Console |
| **ROTATION** | 90-day cycle via AWS Secrets Manager auto-rotation |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `DATABASE_POOL_SIZE` |
| **TYPE** | Integer |
| **REQ / OPT** | Optional (Default: `20`) |
| **PURPOSE** | Maximum steady-state connection pool size |
| **USED BY** | SQLAlchemy AsyncConnectionPool |
| **LOCAL DEV** | `10` |
| **STAGING** | `20` |
| **PRODUCTION** | `50` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `20` |
| **WHERE TO OBTAIN** | Sizing calculations based on container concurrency |
| **ROTATION** | N/A |

---

### Domain 3: Cache, Distributed Queue & Locks (Redis)
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `REDIS_URL` |
| **TYPE** | URI String |
| **REQ / OPT** | Required |
| **PURPOSE** | Connection string for Redis instance (rate limiting, distributed locks, Celery broker) |
| **USED BY** | Celery Worker, Redis Cache Manager, FastAPILimiter |
| **LOCAL DEV** | `redis://localhost:6379/0` |
| **STAGING** | `rediss://:[STG_TOKEN]@aiwf-stage-redis.internal:6379/0` |
| **PRODUCTION** | `rediss://:[PROD_TOKEN]@aiwf-prod-redis.internal:6379/0` |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | `redis://localhost:6379/0` |
| **WHERE TO OBTAIN** | Local Docker Compose / AWS ElastiCache Auth Token |
| **ROTATION** | 90-day cycle |

---

### Domain 4: Vector Database (Qdrant)
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `QDRANT_URL` |
| **TYPE** | URL String |
| **REQ / OPT** | Required |
| **PURPOSE** | REST/gRPC endpoint for Qdrant vector database cluster |
| **USED BY** | Qdrant Vector Search Engine, RAG Service |
| **LOCAL DEV** | `http://localhost:6333` |
| **STAGING** | `https://qdrant-stage.aiworkforce.internal:6333` |
| **PRODUCTION** | `https://qdrant.aiworkforce.internal:6333` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `http://localhost:6333` |
| **WHERE TO OBTAIN** | Docker Compose / Qdrant Cloud / Internal K8s Service |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `QDRANT_API_KEY` |
| **TYPE** | String |
| **REQ / OPT** | Optional in Local Dev, Required in Prod |
| **PURPOSE** | Authentication token authorizing requests to Qdrant cluster |
| **USED BY** | `QdrantClient` |
| **LOCAL DEV** | Empty (no auth required on local single node) |
| **STAGING** | Staging API Token |
| **PRODUCTION** | Prod Master/Read-Write Token |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | Empty |
| **WHERE TO OBTAIN** | Qdrant Cluster Configuration / Vault |
| **ROTATION** | 90-day cycle |

---

### Domain 5: Blob & Document Object Storage (S3 / MinIO)
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `S3_ENDPOINT_URL` |
| **TYPE** | URL String |
| **REQ / OPT** | Required in Dev, Omitted in Prod (defaults to AWS standard endpoints) |
| **PURPOSE** | Overrides standard AWS S3 endpoint to point to local MinIO container |
| **USED BY** | Boto3 S3 Client |
| **LOCAL DEV** | `http://localhost:9000` |
| **STAGING** | Omitted |
| **PRODUCTION** | Omitted |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `http://localhost:9000` |
| **WHERE TO OBTAIN** | Docker Compose MinIO service |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `S3_BUCKET_DOCUMENTS` |
| **TYPE** | String |
| **REQ / OPT** | Required |
| **PURPOSE** | Designates the primary S3 bucket for tenant-uploaded knowledge documents |
| **USED BY** | Document Ingestion Pipeline |
| **LOCAL DEV** | `aiwf-dev-documents` |
| **STAGING** | `aiwf-stage-documents-useast1` |
| **PRODUCTION** | `aiwf-prod-documents-useast1` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `aiwf-dev-documents` |
| **WHERE TO OBTAIN** | CloudFormation / Terraform bucket output |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `AWS_ACCESS_KEY_ID` |
| **TYPE** | String |
| **REQ / OPT** | Required |
| **PURPOSE** | IAM credential key ID authorized for S3 object operations |
| **USED BY** | Boto3 Client |
| **LOCAL DEV** | `minio_admin` |
| **STAGING** | Injected via K8s IRSA / IAM Role |
| **PRODUCTION** | Injected via K8s IRSA (IAM Roles for Service Accounts) |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | `minio_admin` (Dev MinIO only) |
| **WHERE TO OBTAIN** | AWS IAM / Local MinIO config |
| **ROTATION** | 90-day cycle (or eliminated via IRSA in cloud) |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `AWS_SECRET_ACCESS_KEY` |
| **TYPE** | String |
| **REQ / OPT** | Required |
| **PURPOSE** | IAM credential secret authorized for S3 object operations |
| **USED BY** | Boto3 Client |
| **LOCAL DEV** | `minio_password_123` |
| **STAGING** | Injected via IRSA |
| **PRODUCTION** | Injected via IRSA |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | `minio_password_123` (Dev MinIO only) |
| **WHERE TO OBTAIN** | AWS IAM / Local MinIO config |
| **ROTATION** | 90-day cycle |

---

### Domain 6 & 20: Authentication, JWT & Sessions
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `JWT_SECRET_KEY` |
| **TYPE** | String (minimum 64 bytes base64) |
| **REQ / OPT** | Required |
| **PURPOSE** | Cryptographic secret for signing HMAC-SHA256 user session tokens |
| **USED BY** | Auth Service, Token Verification Middleware |
| **LOCAL DEV** | Safe dev token generated locally via `openssl rand -base64 64` |
| **STAGING** | Staging HMAC Key |
| **PRODUCTION** | Production HMAC Key injected via Secrets Manager |
| **SENSITIVITY** | **Critical Secret** |
| **DEFAULT VALUE** | Must be locally generated, never hardcoded |
| **WHERE TO OBTAIN** | Generated cryptographically |
| **ROTATION** | 180-day cycle with dual-key verification window |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `JWT_ACCESS_EXPIRATION_MINUTES` |
| **TYPE** | Integer |
| **REQ / OPT** | Optional (Default: `60`) |
| **PURPOSE** | Lifespan of short-lived JWT access tokens |
| **USED BY** | Token Generator |
| **LOCAL DEV** | `60` |
| **STAGING** | `30` |
| **PRODUCTION** | `15` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `60` |
| **WHERE TO OBTAIN** | Security compliance baseline |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `JWT_REFRESH_EXPIRATION_DAYS` |
| **TYPE** | Integer |
| **REQ / OPT** | Optional (Default: `30`) |
| **PURPOSE** | Lifespan of sliding refresh tokens stored in secure HTTP-only cookies |
| **USED BY** | Session Refresh Engine |
| **LOCAL DEV** | `30` |
| **STAGING** | `14` |
| **PRODUCTION** | `7` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `30` |
| **WHERE TO OBTAIN** | Security compliance baseline |
| **ROTATION** | N/A |

---

### Domain 7 & 8: AI Gateway, LiteLLM & LLM Providers
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `PLATFORM_OPENAI_API_KEY` |
| **TYPE** | String (`sk-...`) |
| **REQ / OPT** | Optional in Local Dev, Required in Prod for Starter Tier Fallbacks |
| **PURPOSE** | Platform fallback OpenAI credential utilized exclusively for Starter tier trials and platform evaluations |
| **USED BY** | LiteLLM Gateway |
| **LOCAL DEV** | Optional (BYOK used during manual testing) |
| **STAGING** | OpenAI Staging Organization Key |
| **PRODUCTION** | OpenAI Production Organization Key |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | None |
| **WHERE TO OBTAIN** | OpenAI API Console |
| **ROTATION** | 90-day cycle |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `PLATFORM_ANTHROPIC_API_KEY` |
| **TYPE** | String (`sk-ant-...`) |
| **REQ / OPT** | Optional |
| **PURPOSE** | Platform fallback Anthropic credential for Claude 3.5 Sonnet execution |
| **USED BY** | LiteLLM Gateway |
| **LOCAL DEV** | Optional |
| **STAGING** | Anthropic Staging Key |
| **PRODUCTION** | Anthropic Production Key |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | None |
| **WHERE TO OBTAIN** | Anthropic Console |
| **ROTATION** | 90-day cycle |

---

### Domain 9 & 10: Embedding & Reranking Providers
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `DEFAULT_EMBEDDING_MODEL` |
| **TYPE** | String |
| **REQ / OPT** | Required (Default: `text-embedding-3-small`) |
| **PURPOSE** | Canonical model name for vectorizing chunks into 1536-dimensional space |
| **USED BY** | Knowledge Ingestion Service |
| **LOCAL DEV** | `text-embedding-3-small` |
| **STAGING** | `text-embedding-3-small` |
| **PRODUCTION** | `text-embedding-3-small` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `text-embedding-3-small` |
| **WHERE TO OBTAIN** | Architecture Decision Baseline |
| **ROTATION** | N/A |

---

### Domain 11 & 12: Observability (Langfuse & OpenTelemetry)
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `LANGFUSE_HOST` |
| **TYPE** | URL String |
| **REQ / OPT** | Optional in Dev, Required in Prod |
| **PURPOSE** | Endpoint URL for Langfuse tracing backend |
| **USED BY** | Langfuse Python Client |
| **LOCAL DEV** | `http://localhost:3100` (or `https://cloud.langfuse.com`) |
| **STAGING** | `https://cloud.langfuse.com` |
| **PRODUCTION** | `https://cloud.langfuse.com` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `http://localhost:3100` |
| **WHERE TO OBTAIN** | Langfuse Project Settings |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `LANGFUSE_PUBLIC_KEY` |
| **TYPE** | String (`pk-lf-...`) |
| **REQ / OPT** | Optional in Dev, Required in Prod |
| **PURPOSE** | Langfuse organization public identifier |
| **USED BY** | Langfuse Client |
| **LOCAL DEV** | Optional |
| **STAGING** | Staging Langfuse Public Key |
| **PRODUCTION** | Production Langfuse Public Key |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | None |
| **WHERE TO OBTAIN** | Langfuse Project Settings |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `LANGFUSE_SECRET_KEY` |
| **TYPE** | String (`sk-lf-...`) |
| **REQ / OPT** | Optional in Dev, Required in Prod |
| **PURPOSE** | Langfuse authorization secret |
| **USED BY** | Langfuse Client |
| **LOCAL DEV** | Optional |
| **STAGING** | Staging Secret Key |
| **PRODUCTION** | Production Secret Key |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | None |
| **WHERE TO OBTAIN** | Langfuse Project Settings |
| **ROTATION** | 90-day cycle |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `OTEL_EXPORTER_OTLP_ENDPOINT` |
| **TYPE** | URL String |
| **REQ / OPT** | Optional in Dev, Required in Prod |
| **PURPOSE** | Destination collector for OpenTelemetry trace spans |
| **USED BY** | OpenTelemetry Tracing Provider |
| **LOCAL DEV** | `http://localhost:4318` |
| **STAGING** | Internal OTLP Collector |
| **PRODUCTION** | AWS Distro for OTel / Datadog Agent OTLP |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `http://localhost:4318` |
| **WHERE TO OBTAIN** | APM Collector Endpoint |
| **ROTATION** | N/A |

---

### Domain 13: Model Context Protocol (MCP) Sandbox
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `MCP_EXECUTION_TIMEOUT_SECONDS` |
| **TYPE** | Integer |
| **REQ / OPT** | Required (Default: `30`) |
| **PURPOSE** | Hard timeout cutoff for executing external MCP tool scripts |
| **USED BY** | Tool Sandboxing Engine |
| **LOCAL DEV** | `30` |
| **STAGING** | `30` |
| **PRODUCTION** | `30` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `30` |
| **WHERE TO OBTAIN** | Tool Sandboxing Specification |
| **ROTATION** | N/A |

---

### Domain 14: Transactional Email & Alerts (SMTP)
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `SMTP_HOST` |
| **TYPE** | String |
| **REQ / OPT** | Optional in Dev (stdout mock), Required in Prod |
| **PURPOSE** | Hostname of outbound mail server for approvals and invitations |
| **USED BY** | Email Notification Service |
| **LOCAL DEV** | `localhost` |
| **STAGING** | `smtp.sendgrid.net` |
| **PRODUCTION** | `email-smtp.us-east-1.amazonaws.com` (AWS SES) |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `localhost` |
| **WHERE TO OBTAIN** | Mail provider / SES |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `SMTP_PORT` |
| **TYPE** | Integer |
| **REQ / OPT** | Optional (Default: `587`) |
| **PURPOSE** | SMTP submission port |
| **USED BY** | Mailer |
| **LOCAL DEV** | `1025` (MailHog) |
| **STAGING** | `587` |
| **PRODUCTION** | `587` |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | `587` |
| **WHERE TO OBTAIN** | Mail provider documentation |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `SMTP_PASSWORD` |
| **TYPE** | String |
| **REQ / OPT** | Optional in Dev, Required in Prod |
| **PURPOSE** | SMTP authentication secret / API key |
| **USED BY** | Mailer |
| **LOCAL DEV** | Empty |
| **STAGING** | SendGrid API Key |
| **PRODUCTION** | AWS SES SMTP Password |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | Empty |
| **WHERE TO OBTAIN** | SES / SendGrid console |
| **ROTATION** | 90-day cycle |

---

### Domain 15: OAuth & SSO
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `GOOGLE_CLIENT_ID` |
| **TYPE** | String |
| **REQ / OPT** | Optional in Dev, Required for Google SSO |
| **PURPOSE** | Client ID for Google OAuth2 authentication |
| **USED BY** | Auth SSO Service |
| **LOCAL DEV** | Optional |
| **STAGING** | Staging OAuth Client ID |
| **PRODUCTION** | Production OAuth Client ID |
| **SENSITIVITY** | Non-Secret |
| **DEFAULT VALUE** | None |
| **WHERE TO OBTAIN** | Google Cloud Console |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `GOOGLE_CLIENT_SECRET` |
| **TYPE** | String |
| **REQ / OPT** | Optional in Dev, Required for Google SSO |
| **PURPOSE** | Client secret for Google OAuth2 authentication |
| **USED BY** | Auth SSO Service |
| **LOCAL DEV** | Optional |
| **STAGING** | Staging Secret |
| **PRODUCTION** | Production Secret |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | None |
| **WHERE TO OBTAIN** | Google Cloud Console |
| **ROTATION** | 180-day cycle |

---

### Domain 16: External Webhooks & Signatures
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `WEBHOOK_SIGNING_SECRET` |
| **TYPE** | String |
| **REQ / OPT** | Required |
| **PURPOSE** | Master secret used to generate HMAC-SHA256 signatures for outgoing webhooks |
| **USED BY** | Webhook Dispatch Engine |
| **LOCAL DEV** | Safe dev secret |
| **STAGING** | Staging Secret |
| **PRODUCTION** | Production Secret |
| **SENSITIVITY** | **Secret** |
| **DEFAULT VALUE** | Locally generated |
| **WHERE TO OBTAIN** | Generated cryptographically |
| **ROTATION** | 180-day cycle |

---

### Domain 18 & 19: Security, Encryption & KMS
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `MASTER_ENCRYPTION_KEY` |
| **TYPE** | 32-byte Hex String (256 bits) |
| **REQ / OPT** | Required in Dev, Replaced by AWS KMS in Prod |
| **PURPOSE** | AES-256-GCM envelope encryption key for wrapping tenant BYOK API keys at rest |
| **USED BY** | Vault Encryption Service |
| **LOCAL DEV** | 32-byte hex generated via `openssl rand -hex 32` |
| **STAGING** | Injected via AWS KMS Key ARN |
| **PRODUCTION** | Injected via AWS KMS Key ARN |
| **SENSITIVITY** | **Critical Secret** |
| **DEFAULT VALUE** | Must be locally generated, never committed |
| **WHERE TO OBTAIN** | `openssl rand -hex 32` |
| **ROTATION** | Annual envelope re-wrapping |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `AWS_KMS_KEY_ID` |
| **TYPE** | ARN String |
| **REQ / OPT** | Required in Prod, Omitted in Local Dev |
| **PURPOSE** | Customer Managed Key (CMK) ARN for hardware-level KMS wrapping |
| **USED BY** | KMS Encryption Client |
| **LOCAL DEV** | Omitted |
| **STAGING** | `arn:aws:kms:us-east-1:123456789012:key/stage-...` |
| **PRODUCTION** | `arn:aws:kms:us-east-1:123456789012:key/prod-...` |
| **SENSITIVITY** | Non-Secret (ARN) |
| **DEFAULT VALUE** | Omitted |
| **WHERE TO OBTAIN** | AWS KMS Console |
| **ROTATION** | Automated AWS CMK annual key rotation |

---

### Domain 21, 22 & 23: Frontend Bundles, Docker & CI/CD
| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `VITE_API_BASE_URL` |
| **TYPE** | URL String |
| **REQ / OPT** | Required |
| **PURPOSE** | Client-facing base URL for backend API requests |
| **USED BY** | Frontend API Client (Axios / Fetch) |
| **LOCAL DEV** | `http://localhost:8000/v1` |
| **STAGING** | `https://stage-api.aiworkforce.io/v1` |
| **PRODUCTION** | `https://api.aiworkforce.io/v1` |
| **SENSITIVITY** | Non-Secret (Publicly bundled) |
| **DEFAULT VALUE** | `http://localhost:8000/v1` |
| **WHERE TO OBTAIN** | API Ingress DNS |
| **ROTATION** | N/A |

| Field | Detail |
|---|---|
| **VARIABLE_NAME** | `VITE_APP_NAME` |
| **TYPE** | String |
| **REQ / OPT** | Required |
| **PURPOSE** | UI display title rendered across browser title and application header |
| **USED BY** | Frontend Web Console |
| **LOCAL DEV** | `AI Workforce` |
| **STAGING** | `AI Workforce (Staging)` |
| **PRODUCTION** | `AI Workforce` |
| **SENSITIVITY** | Non-Secret (Publicly bundled) |
| **DEFAULT VALUE** | `AI Workforce` |
| **WHERE TO OBTAIN** | Product branding |
| **ROTATION** | N/A |

---

*Signed off by Principal Security Engineer & DevSecOps Lead*
