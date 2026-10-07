# OBSERVABILITY ENVIRONMENT SETUP
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** OES-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** APPROVED  
**Architecture:** OpenTelemetry Standard + Langfuse Step Tracing  

---

## 1. OBSERVABILITY ARCHITECTURE OVERVIEW

AI Workforce implements a dual-layer observability model designed for high-concurrency autonomous agent workflows:
1. **System & Service APM Layer (OpenTelemetry)**:
   - Tracks distributed HTTP requests, database query latency, Redis queue latencies, and container metrics.
   - Emits vendor-neutral OTLP spans over HTTP/gRPC (`http://localhost:4318`).
2. **AI & Agent Execution Layer (Langfuse)**:
   - Traces step-by-step LLM calls, prompt templates, completions, token usage breakdown (prompt tokens, completion tokens, cached tokens), dollar cost attribution, and tool dispatch logs.
   - Operates in no-op fallback mode when keys are omitted during offline development.

---

## 2. PRIVACY & SANITIZATION POLICIES (ZERO PII & CREDENTIAL LEAK)

Both OpenTelemetry span processors and Langfuse trace hooks enforce strict redaction rules:
- **Header Masking**: `Authorization`, `Cookie`, `X-API-Key`, `Proxy-Authorization` are completely stripped from HTTP span attributes.
- **Tenant Credential Scrubbing**: Any string matching patterns `sk-[a-zA-Z0-9_-]{20,}`, `whsec_[a-zA-Z0-9_-]{20,}`, or `password` is replaced with `[REDACTED]`.
- **Database Query Parameters**: SQL statements are logged as parameterized templates only; bind parameters are never emitted in plaintext logs.

---

## 3. CONFIGURATION & RUNTIME INITIALIZATION

### Local Development Setup:
- Local traces emit to internal telemetry buffer or local Langfuse container:
  ```env
  LANGFUSE_HOST=http://localhost:3100
  LANGFUSE_PUBLIC_KEY=pk-lf-mock
  LANGFUSE_SECRET_KEY=sk-lf-mock
  OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
  ```

### Staging & Production Setup:
- Configured with managed Langfuse Cloud credentials:
  ```env
  LANGFUSE_HOST=https://cloud.langfuse.com
  LANGFUSE_PUBLIC_KEY=pk-lf-live-...
  LANGFUSE_SECRET_KEY=sk-lf-live-...
  OTEL_EXPORTER_OTLP_ENDPOINT=https://otel-collector.aiworkforce.internal:4318
  ```

---

## 4. VERIFICATION PROCEDURE

1. **Verify OpenTelemetry Exporter**:
   - Check endpoint reachability: `curl -v http://localhost:4318/v1/traces`
2. **Verify Langfuse Connectivity**:
   - SDK initializes on startup; health status confirmed at `/v1/healthz`.
3. **Verify Token Cost Calculation**:
   - LiteLLM token metering maps directly to Langfuse generations table with organization-specific cost metrics.
