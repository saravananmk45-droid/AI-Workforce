# AI Workforce — Autonomous Business Workflow Automation Platform

> Multi-tenant SaaS platform where businesses create AI agents, connect company knowledge and tools, visually build workflows, execute tasks autonomously, require human approval for high-risk actions, and monitor/evaluate every AI run.

---

## Project Status

- **Architecture Status**: **APPROVED & AUDITED** (Architecture Decision Baseline v1.1.0, BRD v1.0.0, User Story Catalogue v1.0.0, System Architecture v1.0.0, Database DDL v1.0.0, API Specification v1.0.0).
- **Development Status**: **PRE-DEVELOPMENT INITIALIZATION** (Environment, dependencies, Docker infrastructure, and security baselines established).
- **Implementation Status**: Application source-code development has not yet begun. Strict pre-development readiness phase.

---

## Documentation Index

All primary technical specifications and architecture deliverables are located in the [`docs/`](./docs) directory:

1. [Business Requirements Document (BRD)](./docs/BRD_AI_Workforce_Platform.md)
2. [User Story Catalogue (92 Stories)](./docs/User_Story_Catalogue_AI_Workforce.md)
3. [Architecture Decision Baseline](./docs/Architecture_Decision_Baseline.md)
4. [System Architecture Specification](./docs/System_Architecture_Specification.md)
5. [Database Design & DDL Specification](./docs/Database_Design_Specification.md)
6. [API Specification (OpenAPI 3.1)](./docs/API_Specification.md)
7. [UI/UX Design System Specification](./docs/UI_UX_Design_System_Specification.md)
8. [DevSecOps & Deployment Specification](./docs/DevSecOps_Deployment_Specification.md)
9. [Environment Configuration Requirements](./docs/ENVIRONMENT_CONFIGURATION_REQUIREMENTS.md)
10. [Tool Sandboxing Specification](./docs/Tool_Sandboxing_Specification.md)
11. [Requirements-to-Implementation Traceability](./docs/Requirements_to_Implementation_Traceability.md)
12. [Executive Interactive PDFs](./docs/pdf)

---

## Pre-Development Environment & Governance Documents

- [Pre-Development Technology Inventory](./PRE_DEVELOPMENT_TECHNOLOGY_INVENTORY.md)
- [Stack Consistency Validation](./STACK_CONSISTENCY_VALIDATION.md)
- [Environment Variable Master Inventory](./ENVIRONMENT_VARIABLE_MASTER.md)
- [Dependency Installation Matrix](./DEPENDENCY_INSTALLATION_MATRIX.md)
- [Local Infrastructure Requirements](./LOCAL_INFRASTRUCTURE_REQUIREMENTS.md)
- [Credential Setup Guide](./CREDENTIAL_SETUP_GUIDE.md)
- [Missing Credentials Register](./MISSING_CREDENTIALS.md)
- [Secrets Security Checklist](./SECRETS_SECURITY_CHECKLIST.md)
- [Developer Machine Requirements](./DEVELOPER_MACHINE_REQUIREMENTS.md)
- [Version Compatibility Report](./VERSION_COMPATIBILITY_REPORT.md)
- [Developer Setup Guide](./DEVELOPMENT_SETUP_GUIDE.md)
- [Pre-Development Validation Report](./PRE_DEVELOPMENT_VALIDATION_REPORT.md)

---

## Setup Status

- **Git & Governance**: Configured (`.gitignore`, zero secret commitment).
- **Frontend Manifests**: `frontend/package.json`, `tsconfig.json`, `vite.config.ts`, `tailwind.config.js`.
- **Backend Manifests**: `backend/requirements.txt`, `requirements-worker.txt`, `pyproject.toml`, `alembic.ini`.
- **Infrastructure Orchestration**: `docker-compose.yml`, `infrastructure/postgres/init.sql`.
- **CI Pipeline**: `.github/workflows/ci.yml`.
