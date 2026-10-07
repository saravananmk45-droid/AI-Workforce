# SYSTEM ARCHITECTURE SPECIFICATION
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** SAS-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** FINAL & APPROVED  
**Classification:** Confidential — Engineering & Architecture  
**Target Audience:** Principal Engineers, Architects, DevSecOps, Platform Engineering  

---

## TABLE OF CONTENTS
1. [Executive Architectural Summary](#1-executive-architectural-summary)
2. [Architectural Principles & Non-Negotiable Constraints](#2-architectural-principles--non-negotiable-constraints)
3. [C4 Architecture Models](#3-c4-architecture-models)
   - 3.1 [C4 Level 1: System Context Diagram](#31-c4-level-1-system-context-diagram)
   - 3.2 [C4 Level 2: Container Diagram](#32-c4-level-2-container-diagram)
   - 3.3 [C4 Level 3: Component Diagram (Core Engine)](#33-c4-level-3-component-diagram-core-engine)
4. [Subsystem & Service Boundary Specifications](#4-subsystem--service-boundary-specifications)
   - 4.1 [Edge & Ingress Gateway](#41-edge--ingress-gateway)
   - 4.2 [API Service & IAM Layer](#42-api-service--iam-layer)
   - 4.3 [Workflow Engine (DAG & Execution Orchestrator)](#43-workflow-engine-dag--execution-orchestrator)
   - 4.4 [Agent Execution Engine (LangGraph ReAct Loop)](#44-agent-execution-engine-langgraph-react-loop)
   - 4.5 [AI Gateway & Model Router](#45-ai-gateway--model-router)
   - 4.6 [Knowledge Ingestion & Hybrid RAG Pipeline](#46-knowledge-ingestion--hybrid-rag-pipeline)
   - 4.7 [Model Context Protocol (MCP) & Tool Dispatcher](#47-model-context-protocol-mcp--tool-dispatcher)
   - 4.8 [Human-in-the-Loop (HITL) & Approval Engine](#48-human-in-the-loop-hitl--approval-engine)
   - 4.9 [Guardrails & Risk Evaluation Engine](#49-guardrails--risk-evaluation-engine)
   - 4.10 [Observability, Tracing & Token Metering](#410-observability-tracing--token-metering)
   - 4.11 [AI Evaluation Engine](#411-ai-evaluation-engine)
   - 4.12 [Notification & Event Dispatcher](#412-notification--event-dispatcher)
5. [Data Tier & Storage Architecture](#5-data-tier--storage-architecture)
   - 5.1 [Relational Persistence (PostgreSQL with RLS)](#51-relational-persistence-postgresql-with-rls)
   - 5.2 [Vector Persistence (Qdrant Namespace Isolation)](#52-vector-persistence-qdrant-namespace-isolation)
   - 5.3 [Cache & Distributed State (Redis Cluster)](#53-cache--distributed-state-redis-cluster)
   - 5.4 [Blob & Object Storage (S3 / MinIO)](#54-blob--object-storage-s3--minio)
6. [End-to-End System Flows](#6-end-to-end-system-flows)
   - 6.1 [Authentication & Tenant Context Flow](#61-authentication--tenant-context-flow)
   - 6.2 [Knowledge Ingestion & Vector Indexing Flow](#62-knowledge-ingestion--vector-indexing-flow)
   - 6.3 [Workflow DAG Compilation & Step Execution Flow](#63-workflow-dag-compilation--step-execution-flow)
   - 6.4 [Cyclic Agent Reasoning & Tool Invocation Flow](#64-cyclic-agent-reasoning--tool-invocation-flow)
   - 6.5 [HITL Interruption, Approval & Resumption Flow](#65-hitl-interruption-approval--resumption-flow)
   - 6.6 [Failure Recovery, Backoff & Idempotent Resumption](#66-failure-recovery-backoff--idempotent-resumption)
7. [Component Attribute Matrix](#7-component-attribute-matrix)
8. [High-Availability, Scalability & Disaster Recovery](#8-high-availability-scalability--disaster-recovery)

---

## 1. EXECUTIVE ARCHITECTURAL SUMMARY

The **AI Workforce** platform is an autonomous business workflow automation platform engineered for enterprise multi-tenancy. It bridges high-level business goals with deterministic software execution by treating AI agents as autonomous digital workers operating inside governed, observable, and human-in-the-loop (HITL) workflows.

The system is architected as an **Event-Driven Modular Monolith transitioning to Microservices**, utilizing asynchronous queues, durable workflow state machines, and a sandboxed AI Gateway. It guarantees absolute tenant isolation, verifiable audit trails, and strict human oversight for sensitive operations.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AI WORKFORCE PLATFORM                                  │
│                                                                                        │
│   Web Console (React 18 + TS)         REST / SSE API Gateway (FastAPI / Fastify)       │
│                 │                                          │                           │
│                 ▼                                          ▼                           │
│   ┌───────────────────────────┐              ┌───────────────────────────┐             │
│   │   Workflow Orchestrator   │◄────────────►│   Agent Execution Engine  │             │
│   │   (Durable State Machine) │              │   (LangGraph ReAct Loop)  │             │
│   └─────────────┬─────────────┘              └─────────────┬─────────────┘             │
│                 │                                          │                           │
│                 ├────────────────────┬─────────────────────┤                           │
│                 ▼                    ▼                     ▼                           │
│   ┌───────────────────────────┐┌───────────┐ ┌───────────────────────────┐             │
│   │     Hybrid RAG Engine     ││HITL Engine│ │     Tool & MCP Router     │             │
│   │    (Qdrant + BM25 RRF)    ││ (Approval)│ │    (Sandboxed Workers)    │             │
│   └───────────────────────────┘└───────────┘ └───────────────────────────┘             │
│                 │                    │                     │                           │
│                 └────────────────────┼─────────────────────┘                           │
│                                      ▼                                                 │
│                        ┌───────────────────────────┐                                   │
│                        │    AI Gateway & Router    │                                   │
│                        │ (LiteLLM + BYOK Vault)    │                                   │
│                        └─────────────┬─────────────┘                                   │
│                                      ▼                                                 │
│                   External LLM Providers (OpenAI, Anthropic)                           │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. ARCHITECTURAL PRINCIPLES & NON-NEGOTIABLE CONSTRAINTS

1. **Mandatory Tenant Scoping (`organization_id`)**: Every database table, API request, cache key, vector collection, and background job must explicitly bind to an `organization_id`. Database-level Row-Level Security (RLS) is enabled across all relational tables.
2. **Durable State Machine**: Workflow executions and agent runs are persisted prior to step dispatch. Any unexpected node crash allows the runner to resume from the last known safe state without re-executing completed side-effects.
3. **Zero Direct LLM Access**: Services do not make raw HTTP calls to OpenAI, Anthropic, or external model providers. All model invocations must pass through the **AI Gateway**, which enforces token budgets, rate limits, PII redaction, and audit logging.
4. **Governed Tool Execution**: External side-effects are categorized into risk tiers (`Low`, `Medium`, `High`, `Critical`). High and Critical actions halt execution and invoke the **HITL Engine**, awaiting signed human approval.
5. **Zero Mock/Test Data in Production**: Production infrastructure (`aiwf_prod`) never hosts test fixtures, demo organizations, or simulated runs. Ephemeral test containers are used during CI/CD.

---

## 3. C4 ARCHITECTURE MODELS

### 3.1 C4 Level 1: System Context Diagram

```mermaid
C4Context
    title System Context Diagram - AI Workforce Platform

    Person(biz_user, "Business User / Operator", "Monitors runs, manages approvals, interacts with deployed agents.")
    Person(workflow_builder, "Workflow Builder / AI Engineer", "Designs agents, authors workflows, uploads knowledge, configures tools.")
    Person(org_admin, "Organization Admin", "Manages organization settings, user seats, billing, and BYOK credentials.")

    System(ai_workforce, "AI Workforce Platform", "Executes autonomous workflows, coordinates multi-agent systems, enforces guardrails, and tracks token costs.")

    System_Ext(llm_providers, "LLM Model Providers", "OpenAI, Anthropic, Google Vertex AI (via BYOK or Platform Credits).")
    System_Ext(mcp_servers, "External Tools & MCP Servers", "GitHub, Slack, Jira, HubSpot, Salesforce, PostgreSQL, Custom REST APIs.")
    System_Ext(smtp_slack, "Notification Channels", "SMTP Email Server, Slack Webhooks for approvals and alerts.")
    System_Ext(idp, "Identity Providers", "Google OAuth, Microsoft Entra ID, SAML 2.0 / OIDC.")

    Rel(biz_user, ai_workforce, "Reviews approvals, inspects runs, triggers workflows", "HTTPS")
    Rel(workflow_builder, ai_workforce, "Configures agents, builds DAG workflows, uploads docs", "HTTPS")
    Rel(org_admin, ai_workforce, "Configures tenant, RBAC, and vault secrets", "HTTPS")

    Rel(ai_workforce, llm_providers, "Dispatches prompt completions, embeddings", "HTTPS/mTLS")
    Rel(ai_workforce, mcp_servers, "Dispatches tool actions via MCP JSON-RPC", "HTTPS/SSE/stdio")
    Rel(ai_workforce, smtp_slack, "Dispatches approval notifications and alerts", "SMTP/HTTPS")
    Rel(ai_workforce, idp, "Authenticates users via SSO/OAuth2", "HTTPS")
```

### 3.2 C4 Level 2: Container Diagram

```mermaid
C4Container
    title Container Diagram - AI Workforce Platform

    Container(spa, "Web Application (SPA)", "React 18, TypeScript, Tailwind CSS, React Flow", "Provides the UI for workflow building, agent studio, approval queue, and analytics.")
    Container(api_gateway, "API Gateway & Reverse Proxy", "Nginx / Envoy / Traefik", "Handles TLS termination, routing, rate limiting, and CORS.")
    Container(core_api, "Core API Backend", "FastAPI / Node.js (TypeScript)", "Provides REST & SSE endpoints for identity, organization, configuration, and run management.")
    Container(workflow_worker, "Workflow & Agent Worker Pool", "Temporal.io Worker / BullMQ Async Runner", "Executes workflow DAGs, coordinates cyclic ReAct agent steps, and manages state transitions.")
    Container(ai_gateway, "AI Gateway Service", "LiteLLM / Python Async Service", "Manages BYOK keys, token budgeting, prompt guardrails, and model failover.")
    Container(sandbox_worker, "Tool Execution Sandbox", "gVisor / Firecracker / Isolated Container", "Executes custom code, bash tools, and external MCP tool payloads in an isolated sandbox.")

    ContainerDb(postgres, "Primary Database", "PostgreSQL 16 with RLS", "Stores tenants, users, workflows, agents, runs, approvals, and audit logs.")
    ContainerDb(qdrant, "Vector Database", "Qdrant Cluster", "Stores document vector embeddings and chunk metadata partitioned by tenant collections.")
    ContainerDb(redis, "Cache & Message Broker", "Redis 7.2 Cluster", "Provides distributed locks, session storage, rate limiting counters, and pub/sub message bus.")
    ContainerDb(s3, "Object Storage", "AWS S3 / MinIO", "Stores uploaded documents, generated run artifacts, and trace dumps.")

    Rel(spa, api_gateway, "API calls & SSE streams", "HTTPS / WSS")
    Rel(api_gateway, core_api, "Proxies requests", "HTTP")
    Rel(core_api, postgres, "Reads/writes configuration & runs", "SQL / RLS")
    Rel(core_api, redis, "Publishes jobs, caches sessions", "RESP")
    Rel(core_api, s3, "Direct document uploads (Presigned URLs)", "HTTPS")

    Rel(workflow_worker, postgres, "Updates run state & execution steps", "SQL / RLS")
    Rel(workflow_worker, redis, "Pulls queue items, acquires locks", "RESP")
    Rel(workflow_worker, qdrant, "Vector similarity search", "gRPC / HTTP")
    Rel(workflow_worker, ai_gateway, "Model inference requests", "HTTP / mTLS")
    Rel(workflow_worker, sandbox_worker, "Dispatches untrusted tool invocations", "gRPC / Unix Socket")

    Rel(ai_gateway, postgres, "Reads encrypted BYOK credentials", "SQL / KMS")
```

### 3.3 C4 Level 3: Component Diagram (Core Engine)

```mermaid
C4Component
    title Component Diagram - Workflow & Agent Execution Engine

    Component(dag_parser, "DAG Compiler & Validator", "Validates node connectivity, acyclic dependencies, and input/output contracts.")
    Component(state_mgr, "Durable State Manager", "Snapshots step outputs, manages checkpoints, and restores state on recovery.")
    Component(agent_loop, "LangGraph ReAct Controller", "Coordinates Thought -> Action -> Observation cycle with step limits.")
    Component(rag_retriever, "Hybrid RAG Retriever", "Dense vector query + BM25 keyword search with Reciprocal Rank Fusion.")
    Component(risk_engine, "Risk & Governance Evaluator", "Classifies tool calls into risk tiers and checks guardrail policies.")
    Component(approval_hook, "Approval Interceptor", "Suspends workflow execution and registers approval requests.")
    Component(tool_client, "MCP Tool Dispatcher", "Encapsulates JSON-RPC tool schemas, validates inputs, and executes calls.")
    Component(telemetry_hook, "OpenTelemetry & Langfuse Hook", "Emits spans, token counts, model latency, and prompt traces.")

    Rel(dag_parser, state_mgr, "Initializes execution graph")
    Rel(state_mgr, agent_loop, "Dispatches agent step")
    Rel(agent_loop, rag_retriever, "Fetches relevant knowledge context")
    Rel(agent_loop, risk_engine, "Submits proposed tool action")
    Rel(risk_engine, approval_hook, "If High/Critical, triggers pause")
    Rel(risk_engine, tool_client, "If Low/Medium, permits execution")
    Rel(tool_client, agent_loop, "Returns tool observation")
    Rel(agent_loop, telemetry_hook, "Emits span data and token usage")
```

---

## 4. SUBSYSTEM & SERVICE BOUNDARY SPECIFICATIONS

### 4.1 Edge & Ingress Gateway
- **Responsibility**: Ingress routing, SSL/TLS termination, DDoS mitigation, IP rate limiting, and CORS policy enforcement.
- **Inputs**: Incoming public HTTPS requests from browsers, webhooks, and third-party integrations.
- **Outputs**: Authenticated/clean HTTP requests forwarded to internal services.
- **Dependencies**: AWS ALB / Nginx / Cloudflare.
- **Security Boundary**: Edge perimeter. Terminates public traffic; forwards client IP headers (`X-Forwarded-For`).
- **Failure Behavior**: Returns HTTP 502/504 on internal gateway failure. Employs Cloudflare fallback pages.
- **Scaling Strategy**: Stateless horizontal scaling with automated cloud load balancing.

### 4.2 API Service & IAM Layer
- **Responsibility**: User authentication (Email/Password, MFA, SAML SSO), Session/JWT issuance, RBAC/ABAC authorization, and organization onboarding.
- **Inputs**: REST requests from Web SPA and Developer APIs.
- **Outputs**: JSON responses, Server-Sent Event (SSE) execution streams, and signed JWT tokens.
- **Dependencies**: PostgreSQL (user records), Redis (session cache), AWS KMS (JWT signing keys).
- **Security Boundary**: Extracts `organization_id` from JWT; sets `app.current_organization_id` session variable in PostgreSQL.
- **Failure Behavior**: Returns standard RFC 7807 Problem Details; invalid sessions rejected with HTTP 401.
- **Scaling Strategy**: Horizontal replication behind API Gateway; statelessly scales to 50+ replicas.

### 4.3 Workflow Engine (DAG & Execution Orchestrator)
- **Responsibility**: Parses workflow definitions, validates DAG graphs, schedules topological steps, coordinates step dependencies, and manages execution checkpoints.
- **Inputs**: Workflow execution triggers (Manual, Webhook, Schedule, Agent Delegation).
- **Outputs**: Step execution commands dispatched to workers; run status state updates.
- **Dependencies**: Temporal.io or BullMQ (Redis-backed queue), PostgreSQL (run persistence).
- **Security Boundary**: Enforces tenant-isolated queues; workflow runs can only access tools and agents belonging to the same tenant.
- **Failure Behavior**: Transient step failures trigger exponential backoff retry; persistent failures halt the branch, mark step as `FAILED`, and invoke on-failure paths.
- **Scaling Strategy**: Worker pools scale horizontally based on queue depth metrics (`queue_depth > 100`).

### 4.4 Agent Execution Engine (LangGraph ReAct Loop)
- **Responsibility**: Executes cyclic reasoning loops for individual AI agents:
  $$\text{Input} \longrightarrow \text{Context Assembly} \longrightarrow \text{LLM Call} \longrightarrow \text{Tool Decision} \longrightarrow \text{Observation} \longrightarrow \text{Terminal Output}$$
- **Inputs**: Task prompt, agent configuration (system prompt, temperature, tools, knowledge collections), run budget.
- **Outputs**: Structured agent output, tool execution requests, memory updates.
- **Dependencies**: AI Gateway, RAG Engine, Tool Dispatcher, Redis (scratchpad memory).
- **Security Boundary**: Bounded execution loops (max 15 iterations); execution budget watchdog aborts tasks exceeding token or timeout limits.
- **Failure Behavior**: Model errors trigger provider fallback; unrecoverable tool errors are reflected into agent context for reasoning-based error correction.
- **Scaling Strategy**: Distributed agent worker processes scale dynamically across Kubernetes nodes.

### 4.5 AI Gateway & Model Router
- **Responsibility**: Manages multi-provider LLM integrations (OpenAI, Anthropic, Google Vertex AI), retrieves encrypted BYOK keys from the credential vault, calculates token expenditure, and redacts PII before external transmission.
- **Inputs**: Unified prompt payloads, model parameters, tenant context.
- **Outputs**: Standardized LLM completions, streaming token deltas, usage token counts.
- **Dependencies**: AWS KMS (key decryption), External Model APIs, Redis (rate limit counters).
- **Security Boundary**: Strict egress boundary. Outbound HTTP requests to approved provider endpoints only. API keys are decrypted in-memory only and never logged.
- **Failure Behavior**: Automatic circuit breaking: if OpenAI returns 5xx/429 for >3 consecutive calls, traffic fails over to Anthropic Claude models.
- **Scaling Strategy**: Async I/O service capable of sustaining 10,000+ concurrent outbound streaming connections.

### 4.6 Knowledge Ingestion & Hybrid RAG Pipeline
- **Responsibility**: Multi-format document parsing (PDF, DOCX, TXT, MD), semantic text chunking (500 tokens, 50-token overlap), embedding generation, vector storage in Qdrant, and hybrid retrieval (Dense + Sparse BM25 with Reciprocal Rank Fusion).
- **Inputs**: Document files uploaded to S3, query strings from agents.
- **Outputs**: Ranked context snippets with source document metadata and relevance scores.
- **Dependencies**: S3 (file storage), Embedding Model API, Qdrant (vector index), PostgreSQL (chunk catalog).
- **Security Boundary**: Qdrant collections are strictly isolated by organization namespace (`org_{id}_{collection_id}`). Cross-organization vector queries are architecturally blocked.
- **Failure Behavior**: Failed document chunking marks document status as `FAILED` with actionable error reasons; RAG query timeouts fall back to keyword-only search.
- **Scaling Strategy**: Document ingestion offloaded to dedicated background workers; Qdrant cluster horizontally partitioned across shards.

### 4.7 Model Context Protocol (MCP) & Tool Dispatcher
- **Responsibility**: Manages registration, discovery, schema validation, and execution of tools complying with the Anthropic Model Context Protocol (MCP).
- **Inputs**: Tool invocation requests (tool name, JSON argument payload, tenant context).
- **Outputs**: Structured tool execution observation JSON.
- **Dependencies**: External APIs, Database Connectors, Tool Execution Sandbox.
- **Security Boundary**: Custom code and system command tools execute inside an isolated micro-sandbox. Network access is restricted to tenant-allowed domains.
- **Failure Behavior**: Tool execution timeouts enforced at 30 seconds; HTTP errors encapsulated in observation payloads for agent comprehension.
- **Scaling Strategy**: Sandboxed worker nodes autoscale based on tool execution queue backlog.

### 4.8 Human-in-the-Loop (HITL) & Approval Engine
- **Responsibility**: Intercepts High/Critical risk actions, suspends workflow execution, persists execution snapshots, dispatches notifications, and validates approval signatures.
- **Inputs**: Approval requests emitted by Risk Engine.
- **Outputs**: Approval tasks persisted to database, notification webhooks/emails dispatched, workflow resumption events.
- **Dependencies**: PostgreSQL (approval state), Notification Service, Redis (state wait hooks).
- **Security Boundary**: Approval actions require authenticated sessions with `APPROVE_WORKFLOW` permission. Self-approval is blocked if segregation-of-duties policy is active.
- **Failure Behavior**: If approval expires (default 48h), the approval transitions to `EXPIRED` and triggers the configured timeout behavior (default: workflow halted).
- **Scaling Strategy**: Event-driven architecture with zero persistent compute overhead during approval wait periods.

### 4.9 Guardrails & Risk Evaluation Engine
- **Responsibility**: Static and dynamic risk classification of proposed actions; prompt injection detection; regex and spaCy NER PII masking.
- **Inputs**: System prompts, user inputs, proposed tool arguments.
- **Outputs**: Risk classification (`Low`, `Medium`, `High`, `Critical`), sanitized inputs/arguments, policy block decisions.
- **Dependencies**: Local regex rule sets, LLM safety classifiers, PostgreSQL (organization guardrail policies).
- **Security Boundary**: Operates in-line prior to any tool execution or model invocation.
- **Failure Behavior**: Fail-secure policy: if the risk engine encounters an internal error, the action is escalated to `High Risk` and sent for human review.
- **Scaling Strategy**: High-speed in-memory evaluation with microsecond execution overhead.

### 4.10 Observability, Tracing & Token Metering
- **Responsibility**: Collects OpenTelemetry distributed traces, records step-by-step LLM inputs/outputs to Langfuse, calculates real-time token costs, and meters tenant quotas.
- **Inputs**: Telemetry events emitted across all platform components.
- **Outputs**: Trace visualization waterfalls, tenant token consumption metrics, Prometheus metrics.
- **Dependencies**: Langfuse / OpenTelemetry Collector, PostgreSQL (`token_metering_records`), Redis (real-time usage counters).
- **Security Boundary**: PII scrubbing engine redacts sensitive credentials and personal data prior to persisting trace payloads.
- **Failure Behavior**: Telemetry logging is asynchronous and non-blocking; telemetry backend failure never disrupts workflow execution.
- **Scaling Strategy**: Kafka / Redis stream buffering handles high-volume telemetry ingestion.

### 4.11 AI Evaluation Engine
- **Responsibility**: Evaluates quality of AI agent outputs and RAG retrieval using the RAG Triad (Context Relevance, Groundedness, Answer Relevance) and rule-based semantic metrics.
- **Inputs**: Completed execution traces, evaluation datasets.
- **Outputs**: Quantitative evaluation scores (0.0 to 1.0), regression alerts.
- **Dependencies**: PostgreSQL (`eval_runs`, `eval_scores`), AI Gateway (evaluator LLM).
- **Security Boundary**: Evaluator executions run asynchronously under tenant context using the tenant's model key.
- **Failure Behavior**: Individual eval calculation failure logs warning without affecting production workflows.
- **Scaling Strategy**: Batch background workers scheduled during off-peak hours or triggered post-execution.

### 4.12 Notification & Event Dispatcher
- **Responsibility**: Formats and dispatches transactional emails, Slack alerts, and webhook notifications for approvals, run failures, and usage alerts.
- **Inputs**: Internal system domain events (e.g., `approval.created`, `workflow.failed`, `quota.threshold_reached`).
- **Outputs**: Outbound SMTP emails, Slack API messages, HTTP webhook deliveries.
- **Dependencies**: Redis queue, SendGrid / SMTP, Third-party webhook endpoints.
- **Security Boundary**: Outbound webhooks execute with HMAC-SHA256 signatures (`X-AIWF-Signature`); targets validated against SSRF blocklists.
- **Failure Behavior**: Failed webhook deliveries retry 3 times with exponential backoff (10s, 60s, 300s).
- **Scaling Strategy**: Dedicated async worker pool with rate-limited outbound queues.

---

## 5. DATA TIER & STORAGE ARCHITECTURE

### 5.1 Relational Persistence (PostgreSQL with RLS)
- **Engine**: PostgreSQL 16+ with PgBouncer connection pooling.
- **Isolation Mechanism**: Multi-tenant Shared Database with Row-Level Security:
  ```sql
  -- Core RLS enforcement model
  ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
  CREATE POLICY tenant_isolation_policy ON agents
    FOR ALL
    USING (organization_id = NULLIF(current_setting('app.current_organization_id', true), '')::uuid);
  ```
- **Clustering & Replication**: Primary-Replica architecture across Multiple Availability Zones (Multi-AZ) with automated failover and read replicas for analytics queries.

### 5.2 Vector Persistence (Qdrant Namespace Isolation)
- **Engine**: Distributed Qdrant Cluster.
- **Isolation Mechanism**: Logical Collection Prefix Isolation:
  - Format: `org_{organization_id}_coll_{collection_id}`
  - Payloads store document ID, chunk index, creation timestamp, and text snippet.
- **Indexing**: Hierarchical Navigable Small World (HNSW) graphs with cosine distance metric for embeddings (e.g., `text-embedding-3-small`, 1536 dimensions).

### 5.3 Cache & Distributed State (Redis Cluster)
- **Engine**: Redis 7.2+ Cluster (Primary with in-memory replicas).
- **Key Taxonomy**:
  - Sessions: `session:{session_id} -> {user_id, organization_id, roles}` (TTL: 24h)
  - Rate Limiting: `ratelimit:{organization_id}:{endpoint} -> count` (TTL: 1m)
  - Distributed Locks: `lock:workflow_run:{run_id}` (TTL: 60s with heartbeat)
  - Idempotency Keys: `idempotency:{organization_id}:{key} -> response_payload` (TTL: 24h)

### 5.4 Blob & Object Storage (S3 / MinIO)
- **Engine**: AWS S3 (Production) / MinIO (Local & Testing).
- **Encryption**: Server-Side Encryption with AWS KMS (SSE-KMS).
- **Bucket Hierarchy**:
  - Documents: `aiwf-documents-{env}/org_{organization_id}/knowledge_{collection_id}/{document_id}.pdf`
  - Trace Dumps: `aiwf-traces-{env}/org_{organization_id}/run_{run_id}/trace.json`
  - Exports: `aiwf-exports-{env}/org_{organization_id}/export_{export_id}.zip`

---

## 6. END-TO-END SYSTEM FLOWS

### 6.1 Authentication & Tenant Context Flow
```mermaid
sequenceDiagram
    autonumber
    actor User as Client Browser
    participant GW as API Gateway
    participant Auth as Auth Service
    participant DB as PostgreSQL
    participant Redis as Redis Cache

    User->>GW: POST /api/v1/auth/login (email, password)
    GW->>Auth: Forward Login Request
    Auth->>DB: Query user by email
    DB-->>Auth: Return User + Password Hash + Salt
    Auth->>Auth: Verify Argon2id Password Hash
    alt MFA Enabled
        Auth-->>User: Return 200 { mfa_required: true, temp_token }
        User->>Auth: POST /api/v1/auth/mfa/verify (totp_code, temp_token)
        Auth->>Auth: Validate TOTP Token
    end
    Auth->>DB: Fetch Organizations & User Roles
    Auth->>Redis: Set Session Key session:{id} (TTL 24h)
    Auth-->>User: Set-Cookie: access_token (JWT), refresh_token (HttpOnly)
    User->>GW: GET /api/v1/agents (Cookie: access_token, X-Organization-ID)
    GW->>Auth: Validate Token & Org Context
    Auth->>DB: SET LOCAL app.current_organization_id = 'org_uuid'
    Auth->>DB: SELECT * FROM agents (RLS Filters to org_uuid)
    DB-->>User: Return 200 OK [agents]
```

### 6.2 Knowledge Ingestion & Vector Indexing Flow
```mermaid
sequenceDiagram
    autonumber
    actor Admin as Workspace Admin
    participant API as Core API
    participant S3 as Object Storage (S3)
    participant Worker as Background Ingestion Worker
    participant Ext as Unstructured Extractor
    participant Emb as OpenAI Embedding API
    participant Qdrant as Qdrant Vector DB
    participant DB as PostgreSQL

    Admin->>API: POST /api/v1/knowledge/{id}/documents (file metadata)
    API->>DB: Create document record (Status: PENDING_UPLOAD)
    API-->>Admin: Return Presigned S3 Upload URL
    Admin->>S3: PUT /documents/... (Binary File Upload)
    S3-->>Admin: 200 OK Uploaded
    Admin->>API: POST /api/v1/knowledge/{id}/documents/{doc_id}/process
    API->>DB: Update document status: QUEUED
    API->>Worker: Enqueue document_ingestion_job
    Worker->>S3: Download file bytes
    Worker->>Ext: Extract text, headings, tables
    Ext-->>Worker: Clean document text
    Worker->>Worker: Semantic Chunking (500 tokens, 50 overlap)
    Worker->>Emb: POST /v1/embeddings (batch of 100 chunks)
    Emb-->>Worker: 1536-dim vector embeddings
    Worker->>Qdrant: Upsert vectors into collection org_{id}_coll_{id}
    Worker->>DB: Batch insert chunk records & update document status: INDEXED
    Worker-->>API: Emit SSE event: document.indexed
    API-->>Admin: Push UI update: Ingestion Complete
```

### 6.3 Workflow DAG Compilation & Step Execution Flow
```mermaid
sequenceDiagram
    autonumber
    actor Trigger as Webhook / Manual Trigger
    participant API as Core API
    participant Engine as Workflow Engine
    participant DB as PostgreSQL
    participant Worker as Execution Worker Pool
    participant Guard as Risk Engine

    Trigger->>API: POST /api/v1/workflows/{id}/run { inputs }
    API->>DB: Verify Workflow Status == PUBLISHED
    API->>Engine: Initialize Workflow Run (DAG definition)
    Engine->>DB: Insert workflow_runs (Status: RUNNING)
    Engine->>Engine: Topologically sort DAG nodes
    loop For Each Ready Step in DAG
        Engine->>DB: Insert workflow_step_runs (Status: RUNNING)
        Engine->>Worker: Dispatch step execution task
        Worker->>Guard: Evaluate Step Inputs against Guardrail Rules
        alt Guardrail Violation Detected
            Guard-->>Worker: Reject execution (Policy Violation)
            Worker->>DB: Update step status: BLOCKED
            Worker->>Engine: Halt Workflow Branch
        else Guardrail Passed
            Worker->>Worker: Execute Step Logic (Agent / Tool / Condition)
            Worker->>DB: Save step output & update status: COMPLETED
            Worker-->>Engine: Step Complete Signal
            Engine->>Engine: Unblock Dependent Downstream Steps
        end
    end
    Engine->>DB: Update workflow_runs (Status: COMPLETED)
```

### 6.4 Cyclic Agent Reasoning & Tool Invocation Flow
```mermaid
sequenceDiagram
    autonumber
    participant Agent as LangGraph ReAct Agent
    participant RAG as RAG Retrieval Engine
    participant Gateway as AI Gateway (LiteLLM)
    participant Model as External LLM (Claude 3.5 / GPT-4o)
    participant Risk as Risk & Governance Engine
    participant Tool as Tool Dispatcher

    Agent->>RAG: Hybrid Search(query="Customer return policy")
    RAG-->>Agent: Return top-3 relevant context chunks
    loop ReAct Loop (Max 15 iterations)
        Agent->>Gateway: POST /chat/completions (Prompt + System + Tools + Context)
        Gateway->>Model: Forward Request with BYOK Header
        Model-->>Gateway: Output: Thought + Action(tool="refund_customer", amount=150)
        Gateway-->>Agent: Return Tool Call Proposal
        Agent->>Risk: Evaluate Action: refund_customer(amount=150)
        alt Action Risk == HIGH
            Risk-->>Agent: Halt Execution -> Requires Human Approval
            Agent->>Agent: Suspend Agent Run (State: WAITING_APPROVAL)
        else Action Risk <= MEDIUM
            Risk-->>Agent: Action Permitted
            Agent->>Tool: Execute refund_customer(amount=150)
            Tool-->>Agent: Observation: {"status": "success", "tx_id": "tx_9921"}
            Agent->>Agent: Append Observation to Message History
        end
    end
    Agent->>Gateway: Final Synthesis Call
    Gateway->>Model: Generate Final Response
    Model-->>Agent: "The refund of $150 was processed successfully."
```

### 6.5 HITL Interruption, Approval & Resumption Flow
```mermaid
sequenceDiagram
    autonumber
    participant Agent as Agent / Workflow Engine
    participant HITL as Approval Service
    participant DB as PostgreSQL
    participant Notif as Notification Service
    actor Approver as Designated Approver (Human)
    participant UI as Approval Console

    Agent->>HITL: Request Approval for High-Risk Tool Execution
    HITL->>DB: Insert approval_requests (Status: PENDING, Snapshot JSON)
    HITL->>DB: Update workflow_run (Status: WAITING_APPROVAL)
    HITL->>Notif: Dispatch Approval Notification (Email + Slack)
    Notif-->>Approver: Send email with deep link: /approvals/app_8812
    Approver->>UI: Navigate to Approval Review Screen
    UI->>HITL: GET /api/v1/approvals/app_8812
    HITL-->>UI: Return Action Payload, Diff, Risk Justification, Agent Trace
    alt Approver Clicks "Approve"
        Approver->>UI: Click "Approve" (with optional note)
        UI->>HITL: POST /api/v1/approvals/app_8812/approve
        HITL->>DB: Update approval_requests (Status: APPROVED, approver_id, timestamp)
        HITL->>DB: Update workflow_run (Status: RUNNING)
        HITL->>Agent: Resume Execution Signal
        Agent->>Agent: Execute Suspended Tool Call
    else Approver Clicks "Reject"
        Approver->>UI: Click "Reject" (Mandatory reason: "Exceeds daily budget")
        UI->>HITL: POST /api/v1/approvals/app_8812/reject { reason }
        HITL->>DB: Update approval_requests (Status: REJECTED)
        HITL->>Agent: Abort Action Signal
        Agent->>Agent: Branch to Failure / Alternate Handling
    end
```

### 6.6 Failure Recovery, Backoff & Idempotent Resumption
```mermaid
sequenceDiagram
    autonumber
    participant Worker as Execution Worker
    participant Tool as External API / Model
    participant Queue as Durable Queue (Temporal / BullMQ)
    participant DB as PostgreSQL

    Worker->>Tool: Invoke API Call (with Idempotency-Key: idemp_1102)
    alt Network Failure / 503 Service Unavailable
        Tool-->>Worker: HTTP 503 / Timeout (30s)
        Worker->>DB: Log Step Attempt (Attempt 1: FAILED)
        Worker->>Queue: Re-schedule task with Exponential Backoff (Backoff: 2s, 4s, 8s)
        Note over Worker,Queue: Worker process experiences unexpected SIGKILL / crash
        Queue->>Queue: Heartbeat timeout detected (Worker dead)
        Queue->>Worker: Reschedule task on alternate healthy worker
        Worker->>DB: Read last safe step checkpoint
        Worker->>Tool: Re-invoke API Call (Idempotency-Key: idemp_1102)
        Tool-->>Worker: HTTP 200 OK (Processed cleanly without duplicate charge)
        Worker->>DB: Update step status: COMPLETED
    end
```

---

## 7. COMPONENT ATTRIBUTE MATRIX

| Component | Responsibility | Primary Inputs | Primary Outputs | Key Dependencies | Security Boundary | Failure Behavior | Scaling Strategy |
|---|---|---|---|---|---|---|---|
| **API Gateway** | Ingress, TLS, Rate Limiting | Public HTTPS | Internal HTTP | Envoy/Nginx | Perimeter Edge | Return 502/504 Bad Gateway | Autoscale on CPU / Conn Count |
| **IAM & Auth Service** | Identity, Sessions, RBAC | Credentials, OAuth, Tokens | JWT, User Context | PostgreSQL, Redis | Tenant Context Isolator | 401 Unauthorized / Lockout | Stateless Horizontal (HPA) |
| **Workflow Engine** | DAG Scheduling, State Machine | Workflow Triggers, Step Events | Step Tasks, Run Updates | Temporal/BullMQ, PostgreSQL | Tenant Queue Separation | Durable Checkpoint & Replay | Autoscale on Queue Lag |
| **Agent ReAct Loop** | Cyclic Reasoning, Planning | Prompts, Tools, Context | Tool Calls, Answers | AI Gateway, Redis | Step & Token Budget Watchdog | Fallback Provider / Halt | Kubernetes Pod Autoscaling |
| **AI Gateway** | BYOK Vault, Model Routing | Prompts, Model Configs | Streaming Tokens, Usage | AWS KMS, LLM Providers | Strict Egress Controller | Circuit Breaker & Failover | High Async Concurrency |
| **Hybrid RAG** | Vector & Keyword Retrieval | Search Query, Filters | Ranked Text Chunks | Qdrant, S3, Embedding API | Namespace `org_{id}_coll_{id}` | Keyword Fallback on Qdrant Fail | Sharded Vector Partitioning |
| **MCP Dispatcher** | Tool Schema & Execution | JSON-RPC Invocations | Tool Observations | Micro-Sandbox, Remote APIs | Network & Syscall Sandboxing | 30s Timeout, Return Error Obs | Autoscale on Task Backlog |
| **HITL Engine** | Approval Pause & Resumption | Risk Triggers, Approvals | Approval Tasks, Resumes | PostgreSQL, Mail/Slack | Role `APPROVE_WORKFLOW` Check | Timeout Auto-Reject/Escalate | Event-Driven (Zero Idle Cost) |
| **Guardrails** | Safety & PII Sanitization | Text, Tool Arguments | Sanitized Text, Blocks | Regex Engine, PII Scrubber | In-line Synchronous Gate | Fail-Secure (Escalate to High) | Low-Latency In-Memory Execution |
| **Observability** | Traces, Cost & Token Metering | Telemetry Events | Traces, Invoices, Metrics | Langfuse, PostgreSQL, Redis | PII Redaction on Payloads | Async Non-Blocking Buffering | Kafka / Redis Buffer Scaling |

---

## 8. HIGH-AVAILABILITY, SCALABILITY & DISASTER RECOVERY

### 8.1 High-Availability Architecture (99.9% SLA Target)
- **Multi-AZ Deployment**: All stateful services (PostgreSQL, Redis, Qdrant) are deployed across a minimum of three AWS Availability Zones with automated cross-zone replication.
- **Stateless Tier Redundancy**: API Gateway, Core API, and Workflow Worker instances maintain a minimum of 3 replicas across disparate availability zones.
- **Health Checks & Circuit Breaking**: Liveness (`/healthz`) and readiness (`/readyz`) probes execute every 10 seconds. Circuit breakers trip automatically when downstream dependencies experience elevated error rates (>5% for 30s).

### 8.2 Disaster Recovery Targets
- **Recovery Point Objective (RPO)**: $\le 1 \text{ hour}$ for point-in-time database restoration.
- **Recovery Time Objective (RTO)**: $\le 4 \text{ hours}$ for cold regional failover.
- **Backup Regimen**:
  - PostgreSQL: Continuous WAL archiving to S3 + daily automated physical snapshots (retained for 30 days).
  - Qdrant: Automated daily vector collection snapshots synced to S3.
  - S3 Storage: Cross-region replication (CRR) enabled for all tenant document stores.

---

*End of System Architecture Specification*  
*Document Version: 1.0.0 | Status: FINAL & APPROVED*
