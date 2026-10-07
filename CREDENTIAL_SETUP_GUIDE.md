# CREDENTIAL SETUP GUIDE
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** CSG-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** PUBLISHED  
**Audience:** Platform Developers, DevOps Engineers, Security Administrators  

---

## 1. PURPOSE & SECURITY POLICY

This guide provides step-by-step instructions for obtaining and configuring all required platform credentials across development, staging, and production tiers.

**Security Constraints:**
- Never commit any API key, password, or private certificate to Git.
- Never paste production keys into local development `.env` files.
- Always apply the principle of least privilege when issuing cloud credentials.

---

## 2. CREDENTIAL CATALOG & STEP-BY-STEP SETUP PROCEDURES

### 2.1 OpenAI API Credentials
1. **Provider**: OpenAI LLC
2. **Account Requirement**: Developer Account with API Billing enabled ([https://platform.openai.com](https://platform.openai.com)).
3. **Setup Steps**:
   - Log in to the OpenAI Platform Console.
   - Navigate to **API Keys** -> **Create new secret key**.
   - Name the key: `aiwf-platform-dev` (or `aiwf-platform-prod`).
   - Permissions: Select *Restricted* -> allow Model Capabilities (`gpt-4o`, `text-embedding-3-small`) or *All*.
   - Copy the key immediately (starts with `sk-proj-...` or `sk-...`).
4. **Required Value**: Secret key string.
5. **Environment Variable**: `PLATFORM_OPENAI_API_KEY`
6. **Usage**: Local Dev (Optional), Staging (Required), Production (Required).
7. **Security Requirements**: Restrict spend limit to $50/mo during development. Store in AWS Secrets Manager in production.
8. **Rotation Strategy**: Rotate every 90 days.

---

### 2.2 Anthropic API Credentials
1. **Provider**: Anthropic PBC
2. **Account Requirement**: Anthropic Console Account ([https://console.anthropic.com](https://console.anthropic.com)).
3. **Setup Steps**:
   - Log in to the Anthropic Console.
   - Navigate to **Settings** -> **API Keys**.
   - Click **Create Key**, name `aiwf-claude-dev`.
   - Copy key (starts with `sk-ant-...`).
4. **Required Value**: Secret key string.
5. **Environment Variable**: `PLATFORM_ANTHROPIC_API_KEY`
6. **Usage**: Local Dev (Optional), Staging (Optional), Production (Optional).
7. **Security Requirements**: Set monthly budget alerts.
8. **Rotation Strategy**: Rotate every 90 days.

---

### 2.3 Langfuse Observability Credentials
1. **Provider**: Langfuse (Self-Hosted or Langfuse Cloud)
2. **Account Requirement**: Langfuse Account ([https://cloud.langfuse.com](https://cloud.langfuse.com)).
3. **Setup Steps**:
   - Log in to Langfuse Cloud or local instance at `http://localhost:3100`.
   - Create a project: `AI-Workforce`.
   - Go to **Project Settings** -> **API Keys**.
   - Click **Create API Keys**.
   - Copy `Public Key` (`pk-lf-...`) and `Secret Key` (`sk-lf-...`).
4. **Required Value**: Public Key (`pk-lf-...`), Secret Key (`sk-lf-...`), Host URL (`https://cloud.langfuse.com`).
5. **Environment Variables**:
   - `LANGFUSE_PUBLIC_KEY`
   - `LANGFUSE_SECRET_KEY`
   - `LANGFUSE_HOST`
6. **Usage**: Local Dev (Optional), Staging (Required), Production (Required).
7. **Security Requirements**: Secret key must remain confidential. Public key is non-secret.
8. **Rotation Strategy**: Rotate Secret Key every 90 days via Langfuse console.

---

### 2.4 Master Encryption Key (AES-256-GCM Envelope Encryption)
1. **Provider**: Cryptographic OS Entropy (Local Dev) / AWS KMS (Production).
2. **Account Requirement**: OpenSSL command line (Local) / AWS Account with KMS permissions (Production).
3. **Setup Steps (Local Dev)**:
   - Run in terminal:
     ```bash
     openssl rand -hex 32
     ```
   - Copy the 64-character hex output (representing 32 bytes / 256 bits).
   - Paste into `.env` as `MASTER_ENCRYPTION_KEY`.
4. **Setup Steps (Production)**:
   - Create an AWS KMS Symmetric Customer Managed Key (CMK) with alias `alias/aiwf-vault-prod`.
   - Copy Key ARN into `AWS_KMS_KEY_ID`.
5. **Environment Variables**:
   - `MASTER_ENCRYPTION_KEY` (Local Dev)
   - `AWS_KMS_KEY_ID` (Staging / Production)
6. **Usage**: Local Dev (Required), Staging/Production (Replaced by AWS KMS).
7. **Security Requirements**: Critical Secret. If lost, encrypted tenant BYOK credentials cannot be decrypted.
8. **Rotation Strategy**: Production KMS rotates automatically annually.

---

### 2.5 JWT HMAC Signing Secret
1. **Provider**: Local Cryptographic Generator / OpenSSL.
2. **Account Requirement**: Terminal shell.
3. **Setup Steps**:
   - Run in terminal:
     ```bash
     openssl rand -base64 64
     ```
   - Copy output into `.env` as `JWT_SECRET_KEY`.
4. **Required Value**: Minimum 64 bytes base64-encoded string.
5. **Environment Variable**: `JWT_SECRET_KEY`
6. **Usage**: Required across all tiers (unique key per tier).
7. **Security Requirements**: Critical Secret.
8. **Rotation Strategy**: Rotate every 180 days with dual-key verification grace period.

---

### 2.6 Local PostgreSQL, Redis, Qdrant & MinIO Credentials
1. **Provider**: Docker Compose local services.
2. **Account Requirement**: None (local automated containers).
3. **Setup Steps**:
   - Start containers: `docker-compose up -d`.
   - Pre-configured defaults in `.env`:
     - PostgreSQL: user `aiwf_user`, password `dev_password_123`, DB `aiwf_dev`.
     - Redis: port `6379`, no password for local dev.
     - Qdrant: port `6333`, no API key required for local single node.
     - MinIO: user `minio_admin`, password `minio_password_123`.
4. **Environment Variables**: `DATABASE_URL`, `REDIS_URL`, `QDRANT_URL`, `S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.
5. **Usage**: Strictly Local Dev & Integration Testing.
6. **Security Requirements**: NEVER deploy these defaults to publicly reachable networks.
7. **Rotation Strategy**: N/A for local containers.
