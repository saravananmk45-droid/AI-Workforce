# MISSING CREDENTIALS REGISTER
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** MCR-AIWF-2026-001  
**Version:** 1.0.0 | **Audit Status:** PENDING USER INPUT (NON-BLOCKING FOR REPO INITIALIZATION)  

---

## 1. OVERVIEW

During the Pre-Development Environment & Repository Initialization phase, all local service credentials (PostgreSQL, Redis, Qdrant, MinIO) and local cryptographic keys (AES Master Key, JWT HMAC Secret) were pre-configured with secure, self-contained local development values.

However, live cloud AI integrations and remote telemetry require external provider keys. In accordance with Section 7 and Section 37 of `Instructions.md`, **no fake or simulated external API keys have been invented**.

The table below catalogs every external credential not yet provided, whether local development can proceed without it, and the exact steps required from the user.

---

## 2. EXTERNAL CREDENTIAL STATUS MATRIX

| Credential Name | Why It Is Needed | Provider | Official Setup Location | Environment | Can Dev Continue Without It? | Exact Action Required from User |
|---|---|---|---|---|:---:|---|
| `PLATFORM_OPENAI_API_KEY` | Platform fallback for Starter plan metered runs & default embedding generation (`text-embedding-3-small`) | OpenAI | [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) | Dev (optional), Staging/Prod (Required) | **YES** (Mock mode or tenant BYOK can be used during local testing) | Generate an API key in OpenAI console with Model Read/Write & Embedding permissions. Paste into `backend/.env`. |
| `PLATFORM_ANTHROPIC_API_KEY` | Platform fallback for Claude 3.5 Sonnet agent reasoning loops | Anthropic | [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) | Dev (optional), Staging/Prod (Optional) | **YES** | Create key in Anthropic Console and paste into `backend/.env` if Claude evaluation testing is desired. |
| `LANGFUSE_PUBLIC_KEY` & `LANGFUSE_SECRET_KEY` | Fine-grained LLM observability, prompt versioning, trace spans, and token cost dashboards | Langfuse | [https://cloud.langfuse.com](https://cloud.langfuse.com) (or self-hosted) | Dev (optional), Staging/Prod (Required) | **YES** (Tracing gracefully degrades to no-op if keys are omitted) | Create a free project on Langfuse Cloud, copy Project API keys into `backend/.env`. |
| `QDRANT_API_KEY` | Vector database authentication for managed Qdrant Cloud | Qdrant | [https://cloud.qdrant.io](https://cloud.qdrant.io) | Dev (Not required), Prod (Required) | **YES** (Local Docker Qdrant does not enforce authentication) | None for local Docker. Required only when switching from local Docker to managed Qdrant Cloud. |
| `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET` | Google Single Sign-On (SSO) login flow | Google Cloud | [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials) | Staging / Prod | **YES** (Local dev utilizes native email + password JWT authentication) | None for MVP local dev. Configure OAuth Consent Screen and Web Client in Google Cloud for SSO. |
| `SMTP_PASSWORD` / `SENDGRID_API_KEY` | Transactional email delivery for team invitations and human approval requests | SendGrid / AWS SES | SendGrid Console / AWS SES Console | Staging / Prod | **YES** (Local development logs email payloads to terminal or MailHog) | None for local dev. Configure SES/SendGrid in Staging/Prod. |

---

## 3. BLOCKER CLASSIFICATION

- **Local Repository & Environment Initialization Blocker:** **NO (NON-BLOCKING)**
- **Application Feature Development Blocker:** **NO** (Local tests use local Docker infrastructure + mock LLM adapters / developer BYOK keys).
- **Staging / Production Deployment Blocker:** **YES** (Must be injected prior to staging release).
