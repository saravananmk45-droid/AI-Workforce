# SECRETS SECURITY CHECKLIST & GOVERNANCE POLICY
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** SSC-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** ENFORCED  
**Security Lead:** DevSecOps & Security Engineering  

---

## 1. PRE-DEVELOPMENT SECURITY BASELINE

This checklist formalizes mandatory controls to prevent credential leaks, private key exposure, and security regressions throughout the software lifecycle.

### Control Implementation Matrix

| Security Domain | Control Requirement | Implementation Mechanism | Verification Result |
|---|---|---|:---:|
| **Git Exclusion** | `.env` and local secrets must never be tracked by Git | Master `.gitignore` with `.env`, `.env.*`, `*.key`, `*.pem` rules | **ENFORCED** |
| **Template Availability** | Safe placeholder templates must be maintained | `.env.example`, `backend/.env.example`, `frontend/.env.example` explicitly whitelisted via `!` negation | **ENFORCED** |
| **Local Secret Scan** | Zero active production keys or private certificates in tracked files | Pre-commit regex scan across all repository files | **ENFORCED** |
| **Client Bundle Security** | Only variables prefixed with `VITE_` can be exposed to browser | Frontend build enforces strict variable bundling | **ENFORCED** |
| **Log Sanitization** | Passwords, tokens, and authorization headers masked in stdout/logs | Structlog / Pino filter masking `Authorization`, `password`, `key`, `secret` | **ENFORCED** |
| **Error Response Sanitization** | No internal connection strings, stack traces, or credentials in API responses | FastAPI global exception handler returning standardized sanitized error envelopes | **ENFORCED** |
| **Telemetry Privacy** | OpenTelemetry spans and Langfuse traces must not transmit plain API keys or PII | Custom span processor scrubbing sensitive attributes | **ENFORCED** |
| **Data At Rest Encryption** | Tenant BYOK credentials stored encrypted in PostgreSQL | AES-256-GCM envelope encryption wrapped by `MASTER_ENCRYPTION_KEY` / AWS KMS | **ENFORCED** |
| **Data Purity** | Zero mock/fixture records in production database | CI pipeline executes on ephemeral databases; production strictly unseeded | **ENFORCED** |

---

## 2. DEVELOPER ACTION CHECKLIST

Before every Git commit:
- [x] Run `git status` — confirm no `.env`, `*.key`, or secret files appear under staged changes.
- [x] Check for accidentally pasted credentials in comments or docstrings.
- [x] Verify all new environment variables have matching documentation in `ENVIRONMENT_VARIABLE_MASTER.md` and safe placeholders in `.env.example`.
- [x] Ensure all frontend environment variables intended for the client bundle are prefixed with `VITE_`.

---

## 3. INCIDENT RESPONSE PLAN FOR ACCIDENTAL SECRET EXPOSURE

If a secret is ever inadvertently committed or exposed:
1. **Immediate Revocation**: Revoke the exposed credential immediately at the provider's console (e.g., OpenAI, AWS IAM). Do NOT just delete the commit.
2. **History Scrub**: Use `git filter-repo` or BFG Repo-Cleaner to permanently scrub the blob from all Git history branches.
3. **Re-issuance**: Issue a fresh credential with restricted privileges.
4. **Audit Log Inspection**: Review provider access logs for anomalous requests originating from external IP addresses during the exposure window.
