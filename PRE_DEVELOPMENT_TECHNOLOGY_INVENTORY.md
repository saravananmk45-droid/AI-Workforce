# PRE-DEVELOPMENT TECHNOLOGY INVENTORY
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** PTI-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** STACK FROZEN & VERIFIED  
**Audience:** Principal Engineering, DevOps, Infrastructure, Security  

---

## 1. EXECUTIVE SUMMARY & INVENTORY SCOPE

This Technology Inventory defines the exact, canonical technology stack baseline for **AI Workforce**. Every layer has been audited against the approved foundational specifications:
- `BRD_AI_Workforce_Platform.md`
- `User_Story_Catalogue_AI_Workforce.md`
- `Architecture_Decision_Baseline.md` (ADR v1.1.0)
- `System_Architecture_Specification.md`
- `Database_Design_Specification.md`
- `API_Specification.md`
- `UI_UX_Design_System_Specification.md`
- `DevSecOps_Deployment_Specification.md`
- `Tool_Sandboxing_Specification.md`

All technologies are explicitly bound to their runtime tier, license profile, installation method, and configuration requirements.

---

## 2. DETAILED TECHNOLOGY INVENTORY MATRIX

| Category | Technology | Canonical Version | Purpose & Layer | Req / Opt | Local Dev Requirement | Production Requirement | Package / Dependency Name | Installation Method | Configuration Requirement |
|---|---|---|---|---|---|---|---|---|---|
| **A. Frontend** | React | 18.3.1 | Core UI declarative component library | Required | Node.js 20+ runtime | Compiled static bundle (Nginx runner) | `react`, `react-dom` | `npm install react react-dom` | `vite.config.ts` |
| **A. Frontend** | TypeScript | 5.6.3 | Static typing, interface verification | Required | Node.js 20+ | Build-time compilation check (`tsc`) | `typescript`, `@types/react` | `npm install -D typescript @types/react` | `tsconfig.json` (strict: true) |
| **A. Frontend** | Vite | 6.0.0 | Next-generation frontend build tool & HMR | Required | Local dev server (`npm run dev`) | Production bundle minification | `vite`, `@vitejs/plugin-react` | `npm install -D vite @vitejs/plugin-react` | `vite.config.ts`, port 5173 |
| **A. Frontend** | Tailwind CSS | 3.4.14 | Utility-first CSS engine with design tokens | Required | JIT CSS compilation | PostCSS production build | `tailwindcss`, `postcss`, `autoprefixer` | `npm install -D tailwindcss postcss autoprefixer` | `tailwind.config.js`, `index.css` |
| **A. Frontend** | Radix UI | Latest primitives | Headless accessible UI primitives (WCAG 2.1 AA) | Required | Bundled in frontend | Bundled in frontend | `@radix-ui/react-*` | `npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu ...` | Unstyled headless primitives styled via Tailwind tokens |
| **A. Frontend** | React Flow | 12.3.6 | Visual DAG workflow canvas builder | Required | Bundled in frontend | Bundled in frontend | `@xyflow/react` | `npm install @xyflow/react` | Custom node renderers, ELK/Dagre auto-layout |
| **A. Frontend** | Zustand | 5.0.1 | Global client-side UI and canvas state | Required | Bundled in frontend | Bundled in frontend | `zustand` | `npm install zustand` | DevTools middleware, local storage persist |
| **A. Frontend** | TanStack Query | 5.60.5 | Server-state caching, synchronization & optimistic UI | Required | Bundled in frontend | Bundled in frontend | `@tanstack/react-query` | `npm install @tanstack/react-query` | `QueryClientProvider`, staleTime policies |
| **A. Frontend** | Lucide React | 0.460.0 | Enterprise icon set | Required | Bundled in frontend | Bundled in frontend | `lucide-react` | `npm install lucide-react` | SVG tree shaking |
| **A. Frontend** | Recharts | 2.13.3 | Execution metric charts, latency & cost curves | Required | Bundled in frontend | Bundled in frontend | `recharts` | `npm install recharts` | ResponsiveContainer wrapper |
| **B. Backend** | Python | 3.11.9+ | Primary backend execution runtime | Required | Python 3.11 CLI & venv | `python:3.11-slim-bookworm` container | `python` | System package / pyenv / Docker | `PYTHONPATH`, `PYTHONUNBUFFERED=1` |
| **B. Backend** | FastAPI | 0.115.4 | High-performance async REST & SSE API gateway | Required | Local uvicorn process | Multi-worker uvicorn in container | `fastapi`, `uvicorn[standard]` | `pip install fastapi uvicorn[standard]` | `app/main.py`, OpenAPI 3.1 schema |
| **B. Backend** | Pydantic | 2.9.2 | Strict schema validation & serialization | Required | Bundled in Python env | Bundled in Python env | `pydantic`, `pydantic-settings` | `pip install pydantic pydantic-settings` | `BaseSettings`, strict mode |
| **B. Backend** | SQLAlchemy | 2.0.36 | Async ORM & SQL expression builder | Required | Bundled in Python env | Bundled in Python env | `sqlalchemy[asyncio]`, `asyncpg`, `psycopg2-binary` | `pip install sqlalchemy[asyncio] asyncpg psycopg2-binary` | Async engine, connection pooling |
| **B. Backend** | Alembic | 1.14.0 | Database schema migrations engine | Required | Local CLI migrations | Pre-deployment container hook | `alembic` | `pip install alembic` | `alembic.ini`, `migrations/` |
| **C. AI/LLM** | LiteLLM | 1.52.0 | Unified model proxy, retry, fallback & cost metering | Required | Bundled in Python env | In-app gateway layer | `litellm` | `pip install litellm` | Model routing table, budget enforcement |
| **C. AI/LLM** | OpenAI SDK | 1.54.0 | Provider SDK for GPT-4o, embeddings | Required | Bundled in Python env | API client | `openai` | `pip install openai` | `OPENAI_API_KEY` (BYOK & platform fallback) |
| **C. AI/LLM** | Anthropic SDK | 0.39.0 | Provider SDK for Claude 3.5 Sonnet | Required | Bundled in Python env | API client | `anthropic` | `pip install anthropic` | `ANTHROPIC_API_KEY` (BYOK & fallback) |
| **D. Agent Orchestration** | LangGraph | 0.2.45 | Cyclic stateful agent graph execution engine | Required | Bundled in Python env | Worker execution loops | `langgraph` | `pip install langgraph` | StateGraph definitions, budget caps |
| **D. Agent Orchestration** | LangChain Core | 0.3.15 | Agent base abstractions & runnables | Required | Bundled in Python env | Core abstractions | `langchain-core` | `pip install langchain-core` | BaseTool, ToolMessage, AIMessage |
| **E. RAG** | LangChain Text Splitters | 0.3.2 | Document chunking with semantic boundaries | Required | Bundled in Python env | Ingestion pipeline | `langchain-text-splitters` | `pip install langchain-text-splitters` | RecursiveCharacterTextSplitter |
| **F. Vector Database** | Qdrant | 1.9.0+ | Vector index & similarity search engine | Required | Local Docker (`qdrant/qdrant:v1.9.0`) | Distributed Qdrant cluster | `qdrant-client` | `pip install qdrant-client` | Collection-per-tenant, HNSW cosine, port 6333 |
| **G. Relational Database** | PostgreSQL | 16.2+ | Primary ACID relational datastore with RLS | Required | Local Docker (`postgres:16-alpine`) | AWS RDS PostgreSQL 16 (Multi-AZ) | `postgresql-client` / container | `docker run postgres:16-alpine` | `POSTGRES_DB=aiwf_dev`, port 5432, RLS enabled |
| **H. Redis & Broker** | Redis | 7.2-alpine | Distributed cache, rate limiter & Celery broker | Required | Local Docker (`redis:7.2-alpine`) | AWS ElastiCache Redis Cluster | `redis` | `pip install redis` | Port 6379, appendonly yes, maxmemory policy |
| **I. Workflow Engine** | Celery | 5.4.0 | Distributed async task execution & scheduling | Required | Local Celery worker | Dedicated worker containers | `celery[redis]` | `pip install celery[redis]` | Worker concurrency, task queues |
| **J. Model Context Protocol** | Anthropic MCP SDK | 1.1.2 | Standardized JSON-RPC 2.0 tool execution | Required | Python MCP client | Sandboxed tool runners | `mcp` | `pip install mcp` | stdio / SSE transport, schema validator |
| **K. Authentication** | Python-JOSE / PyJWT | 2.9.0 | JWT verification, signing & token refresh | Required | Bundled in Python env | API auth middleware | `pyjwt[crypto]`, `passlib[bcrypt]` | `pip install pyjwt[crypto] passlib[bcrypt]` | HMAC-SHA256, 64-byte secret |
| **L. Object Storage** | MinIO (Dev) / AWS S3 (Prod) | RELEASE.2024-03-30 | S3-compatible tenant document & trace storage | Required | Local Docker (`minio/minio`) | AWS S3 with SSE-KMS | `boto3` | `pip install boto3` | Port 9000/9001, bucket policies |
| **M. Observability** | OpenTelemetry | 1.28.0 | Vendor-neutral distributed tracing & metrics | Required | Local OTLP collector | AWS Distro for OpenTelemetry / Datadog | `opentelemetry-api`, `opentelemetry-sdk`, `opentelemetry-instrumentation-fastapi` | `pip install opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi` | `OTEL_EXPORTER_OTLP_ENDPOINT` |
| **N. Evaluation & Tracing** | Langfuse | 2.53.0 | LLM step tracing, latency, token attribution & eval | Required | Langfuse Cloud / Local container | Langfuse Cloud / Managed | `langfuse` | `pip install langfuse` | `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` |
| **O. API Documentation** | OpenAPI 3.1 / Swagger | 3.1.0 | Machine-readable API contracts & docs | Required | Auto-served at `/docs` | Served behind auth in prod | Built-in to FastAPI | Native FastAPI feature | Swagger UI / ReDoc |
| **P. Testing** | Pytest | 8.3.3 | Backend unit, integration & async test suite | Required | Local test runner (`pytest`) | GitHub Actions CI stage 2 | `pytest`, `pytest-asyncio`, `pytest-cov`, `httpx` | `pip install pytest pytest-asyncio pytest-cov httpx` | `pyproject.toml`, test fixtures |
| **P. Testing** | Vitest | 2.1.4 | Frontend unit & component testing suite | Required | Local test runner (`npm run test`) | GitHub Actions CI stage 2 | `vitest`, `@testing-library/react`, `jsdom` | `npm install -D vitest @testing-library/react jsdom` | `vitest.config.ts` |
| **Q. Security** | Cryptography | 43.0.3 | AES-256-GCM envelope encryption for BYOK secrets | Required | Bundled in Python env | KMS client + AES wrapper | `cryptography` | `pip install cryptography` | Master Key 256-bit, IV 96-bit |
| **R. DevOps & Runtime** | Docker Engine & Compose | 26.0+ / v2.27+ | Multi-container local orchestration | Required | Docker Desktop / Colima | EKS / GKE Kubernetes nodes | System CLI | Docker installer | `docker-compose.yml` |
| **S. Web Server** | Nginx | 1.25-alpine | Frontend SPA reverse proxy & static asset server | Required | Bundled in frontend container | Frontend Pod container | System image | Multi-stage Dockerfile | `nginx/default.conf`, non-root user |
| **T. Kubernetes** | Helm / K8s Manifests | 1.29+ | Container orchestration & ingress (Phase 2 / Prod) | Optional in Local Dev | Not required locally | EKS / GKE clusters | `kubectl`, `helm` | System installer | Namespaced deployments, ConfigMaps |
| **U. CI/CD** | GitHub Actions | Standard | Automated CI/CD pipeline | Required | Local git hooks / act | Cloud GitHub runners | `.github/workflows/*.yml` | Git commit | Lint, SAST, Unit Test, Build |
| **V. Developer Tooling** | Node.js | 20.x or 24.x | Frontend runtime and package management | Required | Installed on dev host | Builder stage in Docker | `node`, `npm` | Node installer | `node -v` (v24.18.0 detected) |
| **V. Developer Tooling** | Git | 2.40+ | Distributed version control | Required | Installed on dev host | CI runner | `git` | Git installer | `git version 2.54.0` detected |

---

*Verified & Signed Off by Principal Enterprise Solution Architect*
