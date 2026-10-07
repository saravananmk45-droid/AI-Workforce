# DATABASE DESIGN & DDL SPECIFICATION
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** DDS-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** FINAL & APPROVED  
**Classification:** Confidential — Engineering & Architecture  
**Target Engine:** PostgreSQL 16+ with Row-Level Security (RLS)  

---

## TABLE OF CONTENTS
1. [Database Architecture & Design Principles](#1-database-architecture--design-principles)
2. [Multi-Tenant Isolation & Row-Level Security (RLS) Pattern](#2-multi-tenant-isolation--row-level-security-rls-pattern)
3. [Schema Entity-Relationship Overview](#3-schema-entity-relationship-overview)
4. [Migration & Dependency Execution Sequence](#4-migration--dependency-execution-sequence)
5. [Complete Production-Ready SQL DDL](#5-complete-production-ready-sql-ddl)
   - 5.1 [Extensions & Global Functions](#51-extensions--global-functions)
   - 5.2 [Identity, Tenant & Access Control (IAM)](#52-identity-tenant--access-control-iam)
   - 5.3 [AI Model Credentials & Integrations](#53-ai-model-credentials--integrations)
   - 5.4 [Knowledge & Document Ingestion](#54-knowledge--document-ingestion)
   - 5.5 [Tools & Model Context Protocol (MCP)](#55-tools--model-context-protocol-mcp)
   - 5.6 [AI Agent Management & Versioning](#56-ai-agent-management--versioning)
   - 5.7 [Workflow Builder & Versioning](#57-workflow-builder--versioning)
   - 5.8 [Execution Engine & Run Tracking](#58-execution-engine--run-tracking)
   - 5.9 [Human-in-the-Loop & Approvals](#59-human-in-the-loop--approvals)
   - 5.10 [Guardrails & Governance](#510-guardrails--governance)
   - 5.11 [Telemetry, Traces & Token Metering](#511-telemetry-traces--token-metering)
   - 5.12 [AI Evaluation & Datasets](#512-ai-evaluation--datasets)
   - 5.13 [Audit Logging & Compliance](#513-audit-logging--compliance)
   - 5.14 [Billing, Quotas & Subscriptions](#514-billing-quotas--subscriptions)
6. [PostgreSQL Row-Level Security (RLS) Policies](#6-postgresql-row-level-security-rls-policies)
7. [Database Performance, Indexing & Maintenance Strategy](#7-database-performance-indexing--maintenance-strategy)
8. [Data Retention & Environment Isolation Enforcement](#8-data-retention--environment-isolation-enforcement)

---

## 1. DATABASE ARCHITECTURE & DESIGN PRINCIPLES

1. **Deterministic Primary Keys**: Every table uses universally unique identifiers (`UUIDv7` or `gen_random_uuid()`) for primary keys to ensure global uniqueness and avoid ID enumeration attacks.
2. **Mandatory Tenant Scoping**: Every tenant-owned table features a non-nullable `organization_id UUID` column bound by foreign key constraints to the `organizations` table.
3. **Database-Level Defense-in-Depth (RLS)**: Row-Level Security is enabled across all tenant tables. Application connections execute `SET LOCAL app.current_organization_id = '...'` before query dispatch.
4. **Strict Audit Immutability**: The `audit_events` and `token_metering_records` tables are strictly append-only. No `UPDATE` or `DELETE` permissions are granted to the application role.
5. **Soft Deletion Pattern**: Critical business assets (`workflows`, `agents`, `knowledge_collections`, `documents`) implement soft-deletion via `deleted_at TIMESTAMPTZ NULL` to preserve execution lineage and audit history.
6. **Immutable Versioning**: Modifying an agent prompt or workflow graph produces a new immutable record in `agent_versions` or `workflow_versions`. Running executions bind to specific version IDs.
7. **Zero Mock/Test Data Policy**: Under no circumstances shall development fixtures, test seeds, or synthetic tenants exist within the production schema.

---

## 2. MULTI-TENANT ISOLATION & ROW-LEVEL SECURITY (RLS) PATTERN

Every query issued by the application layer operates within a tenant transaction boundary:

```sql
-- Pattern applied by the API middleware on each request
BEGIN;
SET LOCAL app.current_organization_id = '018f3a9e-4b21-7299-8832-7492cbb3e100';
-- Application queries execute here
COMMIT;
```

A reusable session validation function enforces the active tenant context:

```sql
CREATE OR REPLACE FUNCTION get_current_organization_id() RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(current_setting('app.current_organization_id', true), '')::UUID;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;
```

---

## 3. SCHEMA ENTITY-RELATIONSHIP OVERVIEW

```
  ┌──────────────────┐       1:N       ┌────────────────────────┐
  │  organizations   ├────────────────►│  organization_members  │
  └────────┬─────────┘                 └────────────────────────┘
           │
           ├───────────────┬────────────────────────┬────────────────────────┐
           ▼ 1:N           ▼ 1:N                    ▼ 1:N                    ▼ 1:N
  ┌────────────────┐┌────────────────────┐┌──────────────────┐┌───────────────────────┐
  │     agents     ││     workflows      ││  knowledge_coll  ││  encrypted_secrets   │
  └────────┬───────┘└─────────┬──────────┘└────────┬─────────┘└───────────────────────┘
           │ 1:N              │ 1:N                │ 1:N
           ▼                  ▼                    ▼
  ┌────────────────┐┌────────────────────┐┌──────────────────┐
  │ agent_versions ││ workflow_versions  ││    documents     │
  └────────┬───────┘└─────────┬──────────┘└────────┬─────────┘
           │                  │                    │ 1:N
           ▼                  ▼                    ▼
  ┌────────────────┐┌────────────────────┐┌──────────────────┐
  │   agent_runs   ││   workflow_runs    ││ document_chunks  │
  └────────┬───────┘└─────────┬──────────┘└──────────────────┘
           │                  │ 1:N
           │                  ▼
           │        ┌────────────────────┐
           │        │ workflow_step_runs │
           │        └─────────┬──────────┘
           ▼                  ▼
  ┌──────────────────────────────────────┐
  │           tool_executions            │
  └──────────────────┬───────────────────┘
                     │ 1:1
                     ▼
  ┌──────────────────────────────────────┐
  │          approval_requests           │
  └──────────────────────────────────────┘
```

---

## 4. MIGRATION & DEPENDENCY EXECUTION SEQUENCE

Migrations must execute in this exact topological order to guarantee foreign key integrity:

```
001_extensions_and_helpers.sql   (pgcrypto, uuid-ossp, session helper functions)
002_iam_and_tenancy.sql          (users, organizations, members, roles, permissions, sessions)
003_secrets_and_models.sql       (encrypted_secrets, model_providers, tenant_model_configs)
004_knowledge_and_documents.sql  (knowledge_collections, documents, document_chunks)
005_tools_and_mcp.sql            (tools, mcp_servers, tool_definitions)
006_agents_and_versioning.sql    (agents, agent_versions, agent_tools, agent_memories)
007_workflows_and_nodes.sql      (workflows, workflow_versions)
008_execution_engine.sql         (workflow_runs, workflow_step_runs, agent_runs, tool_executions)
009_hitl_and_approvals.sql       (approval_requests, approval_actions, approval_policies)
010_guardrails_and_rules.sql     (guardrail_policies, risk_rules, blocked_action_logs)
011_telemetry_and_tokens.sql     (traces, spans, token_metering_records)
012_evaluations_and_datasets.sql (eval_datasets, eval_dataset_items, eval_runs, eval_scores)
013_audit_and_compliance.sql     (audit_events)
014_billing_and_quotas.sql       (subscription_plans, tenant_subscriptions, usage_quotas)
015_enable_rls_policies.sql      (ENABLE RLS on all tenant tables + create policies)
```

---

## 5. COMPLETE PRODUCTION-READY SQL DDL

### 5.1 Extensions & Global Functions

```sql
-- 001_extensions_and_helpers.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Function to retrieve current tenant ID from session context
CREATE OR REPLACE FUNCTION current_org_id() RETURNS UUID AS $$
BEGIN
    RETURN NULLIF(current_setting('app.current_organization_id', true), '')::UUID;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- Trigger function for automatic updated_at maintenance
CREATE OR REPLACE FUNCTION update_timestamp_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### 5.2 Identity, Tenant & Access Control (IAM)

```sql
-- 002_iam_and_tenancy.sql

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    avatar_url TEXT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_system_admin BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret_encrypted TEXT NULL,
    email_verified_at TIMESTAMPTZ NULL,
    failed_login_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ NULL
);

CREATE INDEX idx_users_email ON users(email);

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL,
    slug VARCHAR(64) NOT NULL UNIQUE,
    domain VARCHAR(255) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    plan_tier VARCHAR(32) NOT NULL DEFAULT 'STARTER' CHECK (plan_tier IN ('STARTER', 'PROFESSIONAL', 'ENTERPRISE')),
    max_workflows INT NOT NULL DEFAULT 10,
    max_agents INT NOT NULL DEFAULT 5,
    max_monthly_runs INT NOT NULL DEFAULT 500,
    max_monthly_tokens BIGINT NOT NULL DEFAULT 1000000,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ NULL
);

CREATE INDEX idx_organizations_slug ON organizations(slug);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(64) NOT NULL,
    description TEXT NULL,
    is_system_role BOOLEAN NOT NULL DEFAULT FALSE,
    permissions JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_org_role_name UNIQUE (organization_id, name)
);

CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_org_user UNIQUE (organization_id, user_id)
);

CREATE INDEX idx_org_members_user ON organization_members(user_id);
CREATE INDEX idx_org_members_org ON organization_members(organization_id);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    last_active_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user_org ON sessions(user_id, organization_id);
CREATE INDEX idx_sessions_expires ON sessions(expires_at);

CREATE TABLE invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    role_id UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    invited_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expires_at TIMESTAMPTZ NOT NULL,
    accepted_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invitations_org ON invitations(organization_id);
CREATE INDEX idx_invitations_token ON invitations(token_hash);
```

### 5.3 AI Model Credentials & Integrations

```sql
-- 003_secrets_and_models.sql

CREATE TABLE encrypted_secrets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    secret_type VARCHAR(64) NOT NULL CHECK (secret_type IN ('AI_MODEL_KEY', 'OAUTH_TOKEN', 'API_KEY', 'WEBHOOK_SECRET')),
    encrypted_value TEXT NOT NULL,
    key_fingerprint VARCHAR(64) NOT NULL,
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_org_secret_name UNIQUE (organization_id, name)
);

CREATE TABLE tenant_model_configs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    provider_name VARCHAR(64) NOT NULL CHECK (provider_name IN ('OPENAI', 'ANTHROPIC', 'GOOGLE_VERTEX', 'AZURE_OPENAI')),
    model_identifier VARCHAR(128) NOT NULL,
    secret_id UUID NULL REFERENCES encrypted_secrets(id) ON DELETE SET NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    is_platform_managed BOOLEAN NOT NULL DEFAULT FALSE,
    cost_per_input_million NUMERIC(10, 4) NOT NULL DEFAULT 2.5000,
    cost_per_output_million NUMERIC(10, 4) NOT NULL DEFAULT 10.0000,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_org_model UNIQUE (organization_id, provider_name, model_identifier)
);

CREATE INDEX idx_tenant_model_configs_org ON tenant_model_configs(organization_id);
```

### 5.4 Knowledge & Document Ingestion

```sql
-- 004_knowledge_and_documents.sql

CREATE TABLE knowledge_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    description TEXT NULL,
    embedding_model VARCHAR(128) NOT NULL DEFAULT 'text-embedding-3-small',
    qdrant_collection_name VARCHAR(128) NOT NULL UNIQUE,
    document_count INT NOT NULL DEFAULT 0,
    total_chunks INT NOT NULL DEFAULT 0,
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ NULL,
    CONSTRAINT uq_org_collection_name UNIQUE (organization_id, name)
);

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    collection_id UUID NOT NULL REFERENCES knowledge_collections(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    mime_type VARCHAR(128) NOT NULL,
    s3_storage_path TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'PROCESSING', 'INDEXED', 'FAILED')),
    error_message TEXT NULL,
    chunk_count INT NOT NULL DEFAULT 0,
    uploaded_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ NULL
);

CREATE INDEX idx_documents_org_coll ON documents(organization_id, collection_id);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    collection_id UUID NOT NULL REFERENCES knowledge_collections(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    token_count INT NOT NULL,
    qdrant_point_id UUID NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_document_chunks_doc ON document_chunks(document_id);
CREATE INDEX idx_document_chunks_org ON document_chunks(organization_id);
```

### 5.5 Tools & Model Context Protocol (MCP)

```sql
-- 005_tools_and_mcp.sql

CREATE TABLE mcp_servers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    transport_type VARCHAR(32) NOT NULL CHECK (transport_type IN ('HTTP_SSE', 'STDIO')),
    endpoint_url TEXT NULL,
    auth_secret_id UUID NULL REFERENCES encrypted_secrets(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    mcp_server_id UUID NULL REFERENCES mcp_servers(id) ON DELETE SET NULL,
    name VARCHAR(120) NOT NULL,
    display_name VARCHAR(120) NOT NULL,
    description TEXT NOT NULL,
    tool_type VARCHAR(32) NOT NULL CHECK (tool_type IN ('BUILTIN', 'REST_API', 'MCP_SERVER', 'CUSTOM_SCRIPT')),
    risk_level VARCHAR(16) NOT NULL DEFAULT 'LOW' CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    input_schema JSONB NOT NULL,
    output_schema JSONB NULL,
    execution_timeout_seconds INT NOT NULL DEFAULT 30,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ NULL,
    CONSTRAINT uq_org_tool_name UNIQUE (organization_id, name)
);

CREATE INDEX idx_tools_org ON tools(organization_id);
```

### 5.6 AI Agent Management & Versioning

```sql
-- 006_agents_and_versioning.sql

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    role_description VARCHAR(255) NOT NULL,
    current_version INT NOT NULL DEFAULT 1,
    status VARCHAR(32) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'TESTING', 'PUBLISHED', 'DEPRECATED', 'ARCHIVED')),
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ NULL,
    CONSTRAINT uq_org_agent_name UNIQUE (organization_id, name)
);

CREATE INDEX idx_agents_org ON agents(organization_id);

CREATE TABLE agent_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    version INT NOT NULL,
    system_prompt TEXT NOT NULL,
    model_config_id UUID NOT NULL REFERENCES tenant_model_configs(id) ON DELETE RESTRICT,
    temperature NUMERIC(3, 2) NOT NULL DEFAULT 0.70 CHECK (temperature >= 0.0 AND temperature <= 2.0),
    max_steps INT NOT NULL DEFAULT 10 CHECK (max_steps >= 1 AND max_steps <= 25),
    timeout_seconds INT NOT NULL DEFAULT 120,
    memory_type VARCHAR(32) NOT NULL DEFAULT 'STATELESS' CHECK (memory_type IN ('STATELESS', 'SESSION', 'LONG_TERM')),
    changelog TEXT NULL,
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_agent_version UNIQUE (agent_id, version)
);

CREATE TABLE agent_version_tools (
    agent_version_id UUID NOT NULL REFERENCES agent_versions(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE RESTRICT,
    PRIMARY KEY (agent_version_id, tool_id)
);

CREATE TABLE agent_version_knowledge (
    agent_version_id UUID NOT NULL REFERENCES agent_versions(id) ON DELETE CASCADE,
    collection_id UUID NOT NULL REFERENCES knowledge_collections(id) ON DELETE RESTRICT,
    PRIMARY KEY (agent_version_id, collection_id)
);
```

### 5.7 Workflow Builder & Versioning

```sql
-- 007_workflows_and_nodes.sql

CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    description TEXT NULL,
    current_version INT NOT NULL DEFAULT 1,
    status VARCHAR(32) NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT', 'PUBLISHED', 'DISABLED', 'ARCHIVED')),
    trigger_type VARCHAR(32) NOT NULL DEFAULT 'MANUAL' CHECK (trigger_type IN ('MANUAL', 'SCHEDULE', 'WEBHOOK', 'EVENT')),
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ NULL,
    CONSTRAINT uq_org_workflow_name UNIQUE (organization_id, name)
);

CREATE INDEX idx_workflows_org ON workflows(organization_id);

CREATE TABLE workflow_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    version INT NOT NULL,
    graph_definition JSONB NOT NULL, -- Stores React Flow nodes & edges
    changelog TEXT NULL,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_workflow_version UNIQUE (workflow_id, version)
);
```

### 5.8 Execution Engine & Run Tracking

```sql
-- 008_execution_engine.sql

CREATE TABLE workflow_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    workflow_version_id UUID NOT NULL REFERENCES workflow_versions(id) ON DELETE RESTRICT,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'RUNNING', 'WAITING_APPROVAL', 'COMPLETED', 'FAILED', 'CANCELLED')),
    triggered_by_user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    trigger_type VARCHAR(32) NOT NULL,
    idempotency_key VARCHAR(128) NULL,
    input_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_payload JSONB NULL,
    error_details JSONB NULL,
    total_tokens_consumed BIGINT NOT NULL DEFAULT 0,
    estimated_cost_usd NUMERIC(10, 6) NOT NULL DEFAULT 0.000000,
    started_at TIMESTAMPTZ NULL,
    completed_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_org_run_idempotency UNIQUE (organization_id, idempotency_key)
);

CREATE INDEX idx_workflow_runs_org_status ON workflow_runs(organization_id, status);
CREATE INDEX idx_workflow_runs_workflow ON workflow_runs(workflow_id);

CREATE TABLE workflow_step_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_run_id UUID NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
    step_id VARCHAR(64) NOT NULL, -- Logical node ID in the graph definition
    step_type VARCHAR(32) NOT NULL CHECK (step_type IN ('AGENT', 'TOOL', 'CONDITION', 'HUMAN_APPROVAL', 'TERMINAL')),
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'SKIPPED')),
    input_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    output_payload JSONB NULL,
    error_message TEXT NULL,
    started_at TIMESTAMPTZ NULL,
    completed_at TIMESTAMPTZ NULL,
    duration_ms INT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_step_runs_workflow_run ON workflow_step_runs(workflow_run_id);

CREATE TABLE agent_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    agent_version_id UUID NOT NULL REFERENCES agent_versions(id) ON DELETE RESTRICT,
    workflow_step_run_id UUID NULL REFERENCES workflow_step_runs(id) ON DELETE CASCADE,
    status VARCHAR(32) NOT NULL DEFAULT 'RUNNING' CHECK (status IN ('RUNNING', 'COMPLETED', 'FAILED')),
    step_count INT NOT NULL DEFAULT 0,
    total_tokens_consumed INT NOT NULL DEFAULT 0,
    reasoning_trace JSONB NOT NULL DEFAULT '[]'::jsonb,
    final_output TEXT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ NULL
);

CREATE INDEX idx_agent_runs_step ON agent_runs(workflow_step_run_id);

CREATE TABLE tool_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES tools(id) ON DELETE RESTRICT,
    agent_run_id UUID NULL REFERENCES agent_runs(id) ON DELETE CASCADE,
    workflow_step_run_id UUID NULL REFERENCES workflow_step_runs(id) ON DELETE CASCADE,
    risk_level VARCHAR(16) NOT NULL,
    input_arguments JSONB NOT NULL,
    output_observation JSONB NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'EXECUTING', 'COMPLETED', 'FAILED')),
    error_message TEXT NULL,
    duration_ms INT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tool_executions_agent_run ON tool_executions(agent_run_id);
```

### 5.9 Human-in-the-Loop & Approvals

```sql
-- 009_hitl_and_approvals.sql

CREATE TABLE approval_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    description TEXT NULL,
    min_risk_level VARCHAR(16) NOT NULL CHECK (min_risk_level IN ('MEDIUM', 'HIGH', 'CRITICAL')),
    required_role_id UUID NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    timeout_hours INT NOT NULL DEFAULT 48,
    timeout_action VARCHAR(16) NOT NULL DEFAULT 'REJECT' CHECK (timeout_action IN ('REJECT', 'ESCALATE', 'APPROVE')),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE approval_requests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_run_id UUID NOT NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
    workflow_step_run_id UUID NOT NULL REFERENCES workflow_step_runs(id) ON DELETE CASCADE,
    tool_execution_id UUID NOT NULL REFERENCES tool_executions(id) ON DELETE CASCADE,
    policy_id UUID NULL REFERENCES approval_policies(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    risk_justification TEXT NOT NULL,
    action_payload JSONB NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'CHANGES_REQUESTED', 'EXPIRED')),
    revision_count INT NOT NULL DEFAULT 0,
    expires_at TIMESTAMPTZ NOT NULL,
    responded_by_user_id UUID NULL REFERENCES users(id) ON DELETE RESTRICT,
    response_reason TEXT NULL,
    responded_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_approval_requests_org_status ON approval_requests(organization_id, status);
CREATE INDEX idx_approval_requests_run ON approval_requests(workflow_run_id);
```

### 5.10 Guardrails & Governance

```sql
-- 010_guardrails_and_rules.sql

CREATE TABLE guardrail_policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    description TEXT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    pii_masking_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    prompt_injection_check_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    blocked_keywords JSONB NOT NULL DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blocked_action_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_run_id UUID NULL REFERENCES workflow_runs(id) ON DELETE SET NULL,
    agent_id UUID NULL REFERENCES agents(id) ON DELETE SET NULL,
    violation_type VARCHAR(64) NOT NULL CHECK (violation_type IN ('PROMPT_INJECTION', 'PII_DETECTED', 'BLOCKED_KEYWORD', 'TOOL_RISK_LIMIT')),
    violating_input TEXT NOT NULL,
    action_taken VARCHAR(32) NOT NULL DEFAULT 'BLOCKED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_blocked_actions_org ON blocked_action_logs(organization_id);
```

### 5.11 Telemetry, Traces & Token Metering

```sql
-- 011_telemetry_and_tokens.sql

CREATE TABLE traces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_run_id UUID NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
    agent_run_id UUID NULL REFERENCES agent_runs(id) ON DELETE CASCADE,
    trace_id VARCHAR(64) NOT NULL UNIQUE, -- OpenTelemetry / Langfuse trace identifier
    latency_ms INT NOT NULL,
    total_tokens INT NOT NULL DEFAULT 0,
    cost_usd NUMERIC(10, 6) NOT NULL DEFAULT 0.000000,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_traces_org ON traces(organization_id);
CREATE INDEX idx_traces_run ON traces(workflow_run_id);

CREATE TABLE token_metering_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    workflow_run_id UUID NULL REFERENCES workflow_runs(id) ON DELETE CASCADE,
    agent_id UUID NULL REFERENCES agents(id) ON DELETE SET NULL,
    model_name VARCHAR(128) NOT NULL,
    prompt_tokens INT NOT NULL,
    completion_tokens INT NOT NULL,
    total_tokens INT NOT NULL,
    cost_usd NUMERIC(10, 6) NOT NULL,
    is_platform_managed_key BOOLEAN NOT NULL DEFAULT FALSE,
    billed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_token_metering_org_date ON token_metering_records(organization_id, billed_at);
```

### 5.12 AI Evaluation & Datasets

```sql
-- 012_evaluations_and_datasets.sql

CREATE TABLE eval_datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(120) NOT NULL,
    description TEXT NULL,
    item_count INT NOT NULL DEFAULT 0,
    created_by_user_id UUID NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE eval_dataset_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID NOT NULL REFERENCES eval_datasets(id) ON DELETE CASCADE,
    input_prompt TEXT NOT NULL,
    expected_output TEXT NULL,
    context_reference TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE eval_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    dataset_id UUID NOT NULL REFERENCES eval_datasets(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    agent_version_id UUID NOT NULL REFERENCES agent_versions(id) ON DELETE RESTRICT,
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED')),
    average_score NUMERIC(4, 3) NULL, -- Normalized score 0.000 to 1.000
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ NULL
);

CREATE TABLE eval_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    eval_run_id UUID NOT NULL REFERENCES eval_runs(id) ON DELETE CASCADE,
    dataset_item_id UUID NOT NULL REFERENCES eval_dataset_items(id) ON DELETE CASCADE,
    metric_name VARCHAR(64) NOT NULL CHECK (metric_name IN ('CONTEXT_RELEVANCE', 'GROUNDEDNESS', 'ANSWER_RELEVANCE', 'LATENCY')),
    score NUMERIC(4, 3) NOT NULL,
    reasoning TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 5.13 Audit Logging & Compliance

```sql
-- 013_audit_and_compliance.sql

CREATE TABLE audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    actor_user_id UUID NULL REFERENCES users(id) ON DELETE SET NULL,
    actor_email VARCHAR(255) NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent TEXT NULL,
    action VARCHAR(128) NOT NULL, -- e.g. "agent.created", "workflow.published", "approval.approved"
    resource_type VARCHAR(64) NOT NULL,
    resource_id UUID NOT NULL,
    payload_before JSONB NULL,
    payload_after JSONB NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Immutable append-only audit trail
CREATE INDEX idx_audit_events_org_created ON audit_events(organization_id, created_at);
CREATE INDEX idx_audit_events_resource ON audit_events(resource_type, resource_id);
```

### 5.14 Billing, Quotas & Subscriptions

```sql
-- 014_billing_and_quotas.sql

CREATE TABLE tenant_subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE UNIQUE,
    stripe_customer_id VARCHAR(128) NULL,
    stripe_subscription_id VARCHAR(128) NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('TRIAL', 'ACTIVE', 'PAST_DUE', 'CANCELLED')),
    current_period_start TIMESTAMPTZ NOT NULL,
    current_period_end TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usage_quotas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE UNIQUE,
    billing_period_start TIMESTAMPTZ NOT NULL,
    runs_executed INT NOT NULL DEFAULT 0,
    tokens_consumed BIGINT NOT NULL DEFAULT 0,
    storage_bytes_used BIGINT NOT NULL DEFAULT 0,
    last_reset_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6. POSTGRESQL ROW-LEVEL SECURITY (RLS) POLICIES

To prevent cross-tenant data leaks, RLS is enabled and enforced across all tenant tables:

```sql
-- 015_enable_rls_policies.sql

-- Helper macro to enable RLS and apply standard tenant policy
DO $$ 
DECLARE 
    t text;
    tables text[] := ARRAY[
        'roles', 'organization_members', 'encrypted_secrets', 'tenant_model_configs',
        'knowledge_collections', 'documents', 'document_chunks', 'mcp_servers', 'tools',
        'agents', 'agent_versions', 'workflows', 'workflow_versions', 'workflow_runs',
        'workflow_step_runs', 'agent_runs', 'tool_executions', 'approval_policies',
        'approval_requests', 'guardrail_policies', 'blocked_action_logs', 'traces',
        'token_metering_records', 'eval_datasets', 'eval_runs', 'audit_events',
        'tenant_subscriptions', 'usage_quotas'
    ];
BEGIN
    FOREACH t IN ARRAY tables LOOP
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY;', t);
        EXECUTE format('
            CREATE POLICY tenant_isolation_policy ON %I
            FOR ALL
            USING (organization_id = current_org_id())
            WITH CHECK (organization_id = current_org_id());
        ', t);
    END LOOP;
END $$;
```

---

## 7. DATABASE PERFORMANCE, INDEXING & MAINTENANCE STRATEGY

1. **PgBouncer Pooling**: Configured in transaction-pooling mode (`pool_mode = transaction`) with a maximum pool size of 150 connections.
2. **BRIN Indexing for Append-Only Tables**: `audit_events` and `token_metering_records` utilize Block Range Index (BRIN) on `created_at` / `billed_at` to achieve ultra-compact, high-speed range scans.
3. **Partitioning Strategy**: `audit_events` and `token_metering_records` are range-partitioned by month (`PARTITION BY RANGE (created_at)`), enabling zero-downtime historical purges via partition drops.
4. **Vacuum & Analyze Regimen**: Autovacuum is tuned for write-heavy tables (`autovacuum_vacuum_scale_factor = 0.05`, `autovacuum_analyze_scale_factor = 0.02`).

---

## 8. DATA RETENTION & ENVIRONMENT ISOLATION ENFORCEMENT

1. **Automated Data Purge Workers**: Nightly background workers drop partitions and purge records exceeding tenant retention thresholds:
   - Starter Tier: 7 days
   - Professional Tier: 30 days
   - Enterprise Tier: 365 days / Custom
2. **Zero-Test-Data Constraint**: Production databases strictly disallow fixture seeding. The database bootstrap script enforces:
   ```sql
   DO $$
   BEGIN
       IF current_database() = 'aiwf_prod' AND current_user != 'aiwf_migrator' THEN
           RAISE EXCEPTION 'Direct fixture injection prohibited on production database!';
       END IF;
   END $$;
   ```

---

*End of Database Design & DDL Specification*  
*Document Version: 1.0.0 | Status: FINAL & APPROVED*
