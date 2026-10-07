# DEPENDENCY INSTALLATION MATRIX
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** DIM-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** APPROVED & PINNED  
**Audience:** Full-Stack Engineers, DevOps Engineers, Security Review  

---

## 1. ECOSYSTEM DEPENDENCY SPECIFICATION

Every software dependency required across all platform layers is cataloged below with pinned versions, ecosystem, purpose, installation command, environment target, and license compliance.

---

### Layer A: Frontend Ecosystem (Node.js / React / TypeScript)

| Package Name | Pinned Version | Ecosystem | Purpose | Used By | Installation Command | Req / Opt | Target | License |
|---|---|---|---|---|---|:---:|---|---|
| `react` | `^18.3.1` | npm | UI component library | Frontend App | `npm install react` | Req | Prod | MIT |
| `react-dom` | `^18.3.1` | npm | React DOM renderer | Frontend App | `npm install react-dom` | Req | Prod | MIT |
| `@xyflow/react` | `^12.3.6` | npm | React Flow DAG workflow canvas | Workflow Builder | `npm install @xyflow/react` | Req | Prod | MIT |
| `zustand` | `^5.0.1` | npm | Client-side UI & canvas state | State Management | `npm install zustand` | Req | Prod | MIT |
| `@tanstack/react-query`| `^5.60.5` | npm | Server-state caching & sync | Data Fetching | `npm install @tanstack/react-query` | Req | Prod | MIT |
| `lucide-react` | `^0.460.0` | npm | Enterprise UI icon suite | UI Components | `npm install lucide-react` | Req | Prod | ISC |
| `recharts` | `^2.13.3` | npm | Analytics & token cost charts | Analytics Views | `npm install recharts` | Req | Prod | MIT |
| `clsx` | `^2.1.1` | npm | Dynamic className composer | UI Components | `npm install clsx` | Req | Prod | MIT |
| `tailwind-merge` | `^2.5.4` | npm | Conflict-free Tailwind merges | UI Utilities | `npm install tailwind-merge` | Req | Prod | MIT |
| `@radix-ui/react-dialog` | `^1.1.2` | npm | Accessible modal dialogs | Modal Components | `npm install @radix-ui/react-dialog` | Req | Prod | MIT |
| `@radix-ui/react-dropdown-menu` | `^2.1.2` | npm | Accessible dropdown menus | Menu Components | `npm install @radix-ui/react-dropdown-menu` | Req | Prod | MIT |
| `@radix-ui/react-tooltip` | `^1.1.4` | npm | Accessible tooltips | Canvas Nodes | `npm install @radix-ui/react-tooltip` | Req | Prod | MIT |
| `@radix-ui/react-tabs` | `^1.1.1` | npm | Accessible tab panels | Settings Views | `npm install @radix-ui/react-tabs` | Req | Prod | MIT |
| `@radix-ui/react-toast` | `^1.2.2` | npm | Notification toasts | Feedback Engine | `npm install @radix-ui/react-toast` | Req | Prod | MIT |
| `typescript` | `^5.6.3` | npm | Static typing system | Developer Tooling | `npm install -D typescript` | Req | Dev | Apache-2.0 |
| `@types/react` | `^18.3.12` | npm | TypeScript type definitions | Developer Tooling | `npm install -D @types/react` | Req | Dev | MIT |
| `@types/react-dom` | `^18.3.1` | npm | DOM type definitions | Developer Tooling | `npm install -D @types/react-dom` | Req | Dev | MIT |
| `vite` | `^6.0.0` | npm | Build tool & dev server | Frontend Tooling | `npm install -D vite` | Req | Dev | MIT |
| `@vitejs/plugin-react` | `^4.3.4` | npm | React Fast Refresh Vite plugin | Build Tool | `npm install -D @vitejs/plugin-react` | Req | Dev | MIT |
| `tailwindcss` | `^3.4.14` | npm | Design token CSS engine | Styling Engine | `npm install -D tailwindcss` | Req | Dev | MIT |
| `postcss` | `^8.4.49` | npm | CSS post-processing | Styling Tooling | `npm install -D postcss` | Req | Dev | MIT |
| `autoprefixer` | `^10.4.20` | npm | CSS vendor prefixer | Styling Tooling | `npm install -D autoprefixer` | Req | Dev | MIT |
| `vitest` | `^2.1.4` | npm | Unit & component test runner | Test Suite | `npm install -D vitest` | Req | Dev | MIT |
| `@testing-library/react` | `^16.0.1` | npm | Component test utilities | Test Suite | `npm install -D @testing-library/react` | Req | Dev | MIT |
| `jsdom` | `^25.0.1` | npm | Headless DOM for test runner | Test Suite | `npm install -D jsdom` | Req | Dev | MIT |

---

### Layer B, C, D, E, F, G, H, I, J, K, Q: Backend Ecosystem (Python 3.11+)

| Package Name | Pinned Version | Ecosystem | Purpose | Used By | Installation Command | Req / Opt | Target | License |
|---|---|---|---|---|---|:---:|---|---|
| `fastapi` | `0.115.4` | PyPI | Async REST & SSE web framework | Core API Gateway | `pip install fastapi==0.115.4` | Req | Prod | MIT |
| `uvicorn[standard]` | `0.32.0` | PyPI | ASGI production server | Web Server | `pip install uvicorn[standard]==0.32.0` | Req | Prod | BSD-3-Clause |
| `pydantic` | `2.9.2` | PyPI | Strict schema validation | Request/Response Models | `pip install pydantic==2.9.2` | Req | Prod | MIT |
| `pydantic-settings` | `2.6.1` | PyPI | Environment configuration parser | Application Settings | `pip install pydantic-settings==2.6.1` | Req | Prod | MIT |
| `sqlalchemy` | `2.0.36` | PyPI | Async SQL ORM & query builder | Database Layer | `pip install sqlalchemy==2.0.36` | Req | Prod | MIT |
| `asyncpg` | `0.30.0` | PyPI | High-performance PostgreSQL async driver | Database Connection Pool | `pip install asyncpg==0.30.0` | Req | Prod | Apache-2.0 |
| `psycopg2-binary` | `2.9.10` | PyPI | Synchronous PostgreSQL driver | Alembic Migrations | `pip install psycopg2-binary==2.9.10` | Req | Prod | LGPL |
| `alembic` | `1.14.0` | PyPI | Database schema migration engine | Migration Pipeline | `pip install alembic==1.14.0` | Req | Prod | MIT |
| `redis` | `5.2.0` | PyPI | Async Redis client for cache & locks | Cache / Distributed Locks | `pip install redis==5.2.0` | Req | Prod | MIT |
| `celery` | `5.4.0` | PyPI | Distributed asynchronous worker queue | Background Task Engine | `pip install celery==5.4.0` | Req | Prod | BSD-3-Clause |
| `qdrant-client` | `1.12.1` | PyPI | Qdrant vector database SDK | Vector Search & RAG | `pip install qdrant-client==1.12.1` | Req | Prod | Apache-2.0 |
| `litellm` | `1.52.0` | PyPI | Universal LLM gateway adapter & cost tracking | AI Gateway | `pip install litellm==1.52.0` | Req | Prod | MIT |
| `langgraph` | `0.2.45` | PyPI | Stateful cyclic agent execution graph | Agent Workflow Loops | `pip install langgraph==0.2.45` | Req | Prod | MIT |
| `langchain-core` | `0.3.15` | PyPI | Agent base abstractions & runnables | Agent Foundation | `pip install langchain-core==0.3.15` | Req | Prod | MIT |
| `langchain-text-splitters`| `0.3.2` | PyPI | Document chunking with semantic boundaries | Knowledge Ingestion | `pip install langchain-text-splitters==0.3.2` | Req | Prod | MIT |
| `mcp` | `1.1.2` | PyPI | Anthropic Model Context Protocol SDK | Sandboxed Tools | `pip install mcp==1.1.2` | Req | Prod | MIT |
| `boto3` | `1.35.54` | PyPI | AWS SDK for S3 / MinIO integration | Object Storage | `pip install boto3==1.35.54` | Req | Prod | Apache-2.0 |
| `cryptography` | `43.0.3` | PyPI | AES-256-GCM envelope encryption | Secret Vault | `pip install cryptography==43.0.3` | Req | Prod | Apache-2.0 / BSD |
| `pyjwt[crypto]` | `2.9.0` | PyPI | JWT token signing & verification | Authentication Middleware | `pip install pyjwt[crypto]==2.9.0` | Req | Prod | MIT |
| `passlib[bcrypt]` | `1.7.4` | PyPI | Password hashing engine | Identity Service | `pip install passlib[bcrypt]==1.7.4` | Req | Prod | BSD |
| `httpx` | `0.27.2` | PyPI | Async HTTP client for outbound webhooks | Webhook Engine | `pip install httpx==0.27.2` | Req | Prod | BSD-3-Clause |
| `opentelemetry-api` | `1.28.0` | PyPI | OpenTelemetry tracing API | Telemetry Provider | `pip install opentelemetry-api==1.28.0` | Req | Prod | Apache-2.0 |
| `opentelemetry-sdk` | `1.28.0` | PyPI | OpenTelemetry trace SDK | Telemetry Provider | `pip install opentelemetry-sdk==1.28.0` | Req | Prod | Apache-2.0 |
| `opentelemetry-instrumentation-fastapi` | `0.49b0` | PyPI | Automatic FastAPI route instrumentation | APM Monitoring | `pip install opentelemetry-instrumentation-fastapi==0.49b0` | Req | Prod | Apache-2.0 |
| `langfuse` | `2.53.0` | PyPI | LLM step tracing, evaluation & analytics | AI Observability | `pip install langfuse==2.53.0` | Req | Prod | MIT |
| `pytest` | `8.3.3` | PyPI | Testing framework | Test Suite | `pip install pytest==8.3.3` | Req | Dev | MIT |
| `pytest-asyncio` | `0.24.0` | PyPI | Async testing plugin for pytest | Test Suite | `pip install pytest-asyncio==0.24.0` | Req | Dev | Apache-2.0 |
| `pytest-cov` | `6.0.0` | PyPI | Code coverage reporter | Test Suite | `pip install pytest-cov==6.0.0` | Req | Dev | MIT |
| `ruff` | `0.7.2` | PyPI | Lightning-fast Python linter & formatter | Developer Tooling | `pip install ruff==0.7.2` | Req | Dev | MIT |
| `mypy` | `1.13.0` | PyPI | Static type checker for Python | Developer Tooling | `pip install mypy==1.13.0` | Req | Dev | MIT |

---

*Signed off by Principal Software Architect*
