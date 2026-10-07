You are the Principal Software Architect, DevOps Engineer, Security Engineer, and Repository Initialization Engineer for the project:

AI WORKFORCE — Autonomous Business Workflow Automation Platform

IMPORTANT:
DO NOT START APPLICATION FEATURE DEVELOPMENT YET.

Your current responsibility is ONLY to complete the complete PRE-DEVELOPMENT ENVIRONMENT, DEPENDENCY, CONFIGURATION, INFRASTRUCTURE, SECURITY, AND GITHUB REPOSITORY INITIALIZATION phase.

The project must be development-ready before application source-code implementation begins.

============================================================
1. SOURCE OF TRUTH
============================================================

Before doing anything, inspect and understand ALL available project documents.

Mandatory source documents:

1. BRD_AI_Workforce_Platform.md
2. User_Story_Catalogue_AI_Workforce.md
3. Architecture_Decision_Baseline.md
4. System_Architecture_Specification.md
5. Database_Design_Specification.md
6. API_Specification.md
7. UI_UX_Design_System_Specification.md
8. DevSecOps_Deployment_Specification.md
9. ENVIRONMENT_CONFIGURATION_REQUIREMENTS.md
10. Tool_Sandboxing_Specification.md
11. Requirements_to_Implementation_Traceability.md
12. FINAL PRE-DEVELOPMENT MASTER AUDIT REPORT

Do NOT invent technologies that are not required by the approved architecture.

If any architecture document contains unresolved alternatives such as:

A or B
Temporal or BullMQ
FastAPI or Node.js
Qdrant or pgvector
etc.

DO NOT silently choose one.

First determine whether the Architecture Decision Baseline already resolves it.

If it is still unresolved, stop and report the conflict before installation.

============================================================
2. PRIMARY OBJECTIVE
============================================================

Prepare the entire development environment for AI Workforce.

The final result must allow the project team to start actual development immediately after this phase without discovering missing:

- dependencies
- packages
- SDKs
- runtimes
- system tools
- environment variables
- databases
- queues
- vector database
- object storage
- AI provider configuration
- authentication configuration
- observability configuration
- MCP configuration
- Git configuration
- repository configuration
- Docker configuration
- development scripts

The goal is:

DOCUMENTS → STACK FREEZE → ENVIRONMENT → DEPENDENCIES → INFRASTRUCTURE → SECURITY → GITHUB → VALIDATION → DEVELOPMENT READY

============================================================
3. FIRST: CREATE A COMPLETE TECHNOLOGY INVENTORY
============================================================

Read all architecture documents and create a complete inventory.

Create:

PRE_DEVELOPMENT_TECHNOLOGY_INVENTORY.md

Include:

A. Frontend
B. Backend
C. AI/LLM
D. Agent orchestration
E. RAG
F. Vector database
G. PostgreSQL
H. Redis
I. Workflow engine
J. MCP
K. Authentication
L. Object storage
M. Observability
N. Evaluation
O. API documentation
P. Testing
Q. Security
R. DevOps
S. Docker
T. Kubernetes/Helm if required
U. CI/CD
V. Developer tooling

For every technology specify:

- Technology
- Version
- Purpose
- Where it is used
- Required/Optional
- Local development requirement
- Production requirement
- Package/dependency name
- Installation method
- Configuration requirement

Do not install unnecessary technologies.

============================================================
4. STACK CONSISTENCY CHECK
============================================================

Before installing anything, perform a stack consistency audit.

Verify:

Frontend framework
Backend framework(s)
Database
ORM
Authentication
AI gateway
LLM providers
Embedding providers
Vector database
Cache
Queue
Workflow engine
Object storage
MCP
Observability
Evaluation
Testing
Containerization
Deployment
CI/CD

Every technology must have a clear purpose.

If the architecture contains two technologies solving the same responsibility, identify it.

Example:

Temporal vs BullMQ
FastAPI vs Node.js
Qdrant vs pgvector
etc.

Do not install both merely because both appear somewhere in an old document.

Use the latest approved architecture decision.

Create:

STACK_CONSISTENCY_VALIDATION.md

Status must be:

PASS

or

BLOCKED

Do not proceed if a critical architecture conflict exists.

============================================================
5. ENVIRONMENT VARIABLE MASTER INVENTORY
============================================================

Create:

ENVIRONMENT_VARIABLE_MASTER.md

Scan ALL approved project documents and identify EVERY environment variable required by the project.

Categorize them:

1. Application
2. PostgreSQL
3. Redis
4. Qdrant
5. Object Storage
6. Authentication / Keycloak
7. AI Gateway / LiteLLM
8. OpenAI or other LLM providers
9. Embedding providers
10. Reranking providers
11. Langfuse
12. OpenTelemetry
13. MCP
14. Email
15. OAuth
16. Payments if approved
17. External integrations
18. Security
19. Encryption
20. JWT
21. Docker
22. Deployment
23. CI/CD

For each variable document:

VARIABLE_NAME
TYPE
REQUIRED/OPTIONAL
PURPOSE
USED BY
LOCAL DEVELOPMENT
STAGING
PRODUCTION
SECRET/NON-SECRET
DEFAULT VALUE IF SAFE
WHERE TO OBTAIN IT
ROTATION REQUIREMENT

Do NOT create fake production secrets.

Do NOT invent API keys.

============================================================
6. CREATE .env.example FILES
============================================================

Create appropriate .env.example files based on the actual architecture.

Possible structure:

.env.example

backend/.env.example

frontend/.env.example

services/<service>/.env.example

Only create files where the architecture actually requires them.

Every required environment variable must be represented.

Use safe placeholders:

YOUR_OPENAI_API_KEY=
YOUR_DATABASE_URL=
YOUR_QDRANT_API_KEY=

Never put real credentials in .env.example.

============================================================
7. CREATE LOCAL .ENV FILES
============================================================

If the user has provided actual development credentials or API keys during setup, place them ONLY in the appropriate local .env file.

Do NOT place secrets into source code.

Do NOT place secrets into:

- README
- documentation
- package.json
- Python files
- TypeScript files
- Dockerfile
- docker-compose committed configuration
- GitHub repository
- .env.example

If a required secret is not available:

DO NOT invent it.

Instead create:

MISSING_CREDENTIALS.md

with:

- Credential name
- Why it is needed
- Provider
- Official setup location
- Which environment uses it
- Whether development can continue without it
- Exact action required from the user

============================================================
8. CREDENTIAL COLLECTION WORKFLOW
============================================================

For every required external service, determine how credentials are obtained.

Examples may include:

- LLM provider
- Embedding provider
- Qdrant
- PostgreSQL
- Redis
- Keycloak
- Langfuse
- S3-compatible storage
- GitHub
- Email provider
- OAuth providers
- MCP integrations

Do NOT automatically assume every service requires an API key.

Classify credentials as:

- API Key
- Secret
- Username/Password
- OAuth Client ID
- OAuth Client Secret
- Database URL
- JWT secret
- Encryption key
- Service token
- Cloud credential
- SSH key
- Certificate

Create:

CREDENTIAL_SETUP_GUIDE.md

For each credential provide:

1. Provider
2. Account requirement
3. Setup steps
4. Required value
5. Environment variable
6. Local/staging/production usage
7. Security requirements
8. Rotation strategy

If a browser/login is required, explicitly tell the user what action is required.

Never claim that a credential was successfully obtained unless it actually exists.

============================================================
9. SECRET SECURITY
============================================================

Create:

SECRETS_SECURITY_CHECKLIST.md

Implement/prepare:

- .gitignore
- .env protection
- secret scanning
- prevention of accidental credential commits
- safe logging
- no secret values in error responses
- no secret values in telemetry
- no secret values in frontend bundles
- secret rotation documentation

Verify:

.env

is ignored.

Also verify:

.env.*

is handled correctly without accidentally ignoring .env.example.

Use a secure .gitignore pattern.

============================================================
10. COMPLETE DEPENDENCY INVENTORY
============================================================

Determine EVERY dependency required by the approved architecture.

Do not limit this to application libraries.

Include:

A. Frontend dependencies
B. Backend dependencies
C. AI dependencies
D. Agent dependencies
E. RAG dependencies
F. Database dependencies
G. Redis dependencies
H. MCP dependencies
I. Workflow dependencies
J. Observability dependencies
K. Testing dependencies
L. Dev tooling
M. CLI tools
N. System dependencies
O. Docker dependencies
P. Documentation tooling

Create:

DEPENDENCY_INSTALLATION_MATRIX.md

For every dependency:

- Name
- Version
- Ecosystem
- Purpose
- Used by
- Installation command
- Required/Optional
- Development/Production
- License consideration

============================================================
11. FRONTEND PACKAGE SETUP
============================================================

Inspect the approved frontend architecture.

Determine the exact dependencies required for:

- React
- TypeScript
- Vite if approved
- Tailwind if approved
- Radix UI
- Zustand
- TanStack Query
- React Router
- React Hook Form if required
- Zod if required
- React Flow
- Recharts/Tremor if approved
- SSE client
- Testing
- linting
- formatting
- accessibility
- build tooling

Do NOT install packages merely because they are popular.

Only install packages justified by the architecture.

Create/update:

frontend/package.json

and lock file using the appropriate package manager.

Do NOT manually write fake dependency versions.

Use compatible versions.

============================================================
12. BACKEND PACKAGE SETUP
============================================================

Inspect the approved backend architecture.

Determine exact dependencies required for:

- FastAPI if approved
- Python runtime
- Pydantic
- SQLAlchemy/approved ORM
- PostgreSQL driver
- Redis client
- Qdrant client
- LangChain
- LangGraph
- LiteLLM
- MCP SDK
- OpenTelemetry
- Langfuse
- authentication
- JWT
- HTTP client
- async processing
- testing
- linting
- formatting
- migrations
- security

If Node.js/TypeScript services are approved, also determine:

- Node runtime
- TypeScript
- Express/NestJS if approved
- Prisma if approved
- Zod
- Redis client
- PostgreSQL client
- MCP SDK
- testing
- linting
- formatting

Do not create duplicate backend frameworks unnecessarily.

Create/update:

requirements.txt or pyproject.toml

and/or

package.json

according to the approved architecture.

============================================================
13. AI/LLM DEPENDENCY VALIDATION
============================================================

Verify all AI-related packages required by the architecture.

Check:

- LangChain
- LangGraph
- LiteLLM
- provider SDKs
- embedding SDKs
- tokenizer libraries
- structured output libraries
- evaluation libraries
- RAG libraries

Do NOT download huge local AI models unless explicitly required.

Do NOT install GPU-specific packages unless local architecture requires them.

The project must support API-based LLM execution where approved.

============================================================
14. INFRASTRUCTURE SERVICES
============================================================

Identify all required local development services.

Expected services may include:

PostgreSQL
Redis
Qdrant
Object storage
Keycloak
Langfuse
OpenTelemetry components
Workflow engine
AI gateway

But ONLY use services confirmed by the approved architecture.

Create:

LOCAL_INFRASTRUCTURE_REQUIREMENTS.md

For each service specify:

- Name
- Version
- Port
- Purpose
- Persistent storage
- Health check
- Dependency relationships
- Required environment variables
- Startup order
- Shutdown behavior

============================================================
15. DOCKER / LOCAL DEVELOPMENT
============================================================

Prepare Docker configuration according to DevSecOps specification.

Create/update:

docker-compose.yml

or approved compose structure.

Requirements:

- no hardcoded secrets
- health checks
- persistent volumes where required
- isolated networks
- service dependencies
- restart policies where appropriate
- non-root containers where applicable
- environment variables from .env
- development-only services clearly separated

Do NOT put production credentials into Docker Compose.

============================================================
16. DATABASE INITIALIZATION
============================================================

Prepare PostgreSQL connection configuration.

Verify:

- PostgreSQL version
- database name
- user
- password configuration
- connection pooling
- PgBouncer if approved
- migration system
- schema strategy
- RLS strategy

Do NOT create fake business data.

Only create:

- database
- schema
- extensions
- migration infrastructure
- required system-level setup

Do not insert mock employees, users, organizations, workflows, agents, documents, etc.

============================================================
17. QDRANT INITIALIZATION
============================================================

Prepare Qdrant according to architecture.

Verify:

- local connection
- collection configuration
- vector dimensions
- embedding model compatibility
- distance metric
- metadata strategy
- tenant isolation
- authentication
- persistence

Do NOT insert fake vectors or fake documents.

============================================================
18. REDIS INITIALIZATION
============================================================

Prepare Redis configuration for approved responsibilities:

- cache
- locks
- queues
- rate limiting
- session/state if approved

Verify:

- connection
- authentication if required
- persistence requirement
- health check
- namespace strategy

============================================================
19. OBJECT STORAGE
============================================================

Prepare approved S3-compatible storage.

Verify:

- endpoint
- bucket
- region
- access key
- secret key
- encryption
- lifecycle policy
- local development storage

Do not upload fake production documents.

============================================================
20. AUTHENTICATION / KEYCLOAK
============================================================

If Keycloak is approved:

Prepare:

- Keycloak configuration
- realm configuration strategy
- client configuration strategy
- redirect URLs
- roles
- scopes
- JWT configuration
- local development setup

Do not create insecure production credentials.

Document exactly what must be configured manually.

============================================================
21. OBSERVABILITY
============================================================

Prepare configuration for:

- OpenTelemetry
- Langfuse
- logs
- metrics
- traces
- AI generation traces
- token usage
- latency
- errors

Verify that secrets and PII are not accidentally logged.

Create:

OBSERVABILITY_ENVIRONMENT_SETUP.md

============================================================
22. MCP
============================================================

Prepare MCP development infrastructure according to:

Tool_Sandboxing_Specification.md

Verify:

- MCP SDK
- JSON-RPC 2.0
- local stdio
- authenticated HTTP if approved
- tool registration
- authentication
- authorization
- timeout
- sandboxing
- audit logging

Do not create unrestricted tool execution.

============================================================
23. SYSTEM TOOLING
============================================================

Identify required developer tools.

Examples:

Git
GitHub CLI if approved
Node.js
npm/pnpm
Python
pip/uv if approved
Docker
Docker Compose
PostgreSQL CLI
Redis CLI
Qdrant tools if required
kubectl if deployment phase requires it
Helm if required
OpenTelemetry tooling if required

Check installed versions.

Create:

DEVELOPER_MACHINE_REQUIREMENTS.md

Report:

INSTALLED
MISSING
WRONG VERSION
NOT REQUIRED

Do not install unrelated software.

============================================================
24. VERSION COMPATIBILITY CHECK
============================================================

After determining versions, perform compatibility validation.

Check:

Python ↔ dependencies
Node.js ↔ frontend dependencies
TypeScript ↔ tooling
React ↔ React ecosystem
PostgreSQL ↔ ORM
Redis ↔ clients
Qdrant ↔ SDK
LangChain ↔ LangGraph
LangGraph ↔ Langfuse
LiteLLM ↔ provider SDKs
MCP SDK ↔ runtime
Docker ↔ Compose

Create:

VERSION_COMPATIBILITY_REPORT.md

Any critical incompatibility = BLOCKED.

============================================================
25. PROJECT DIRECTORY STRUCTURE
============================================================

Before application development, establish the approved repository structure.

Example only — DO NOT blindly copy this:

ai-workforce/
├── frontend/
├── backend/
├── services/
├── packages/
├── infrastructure/
├── docker/
├── docs/
├── scripts/
├── tests/
├── .github/
├── .env.example
├── .gitignore
├── README.md
└── ...

The final structure must come from the approved architecture.

Do NOT create fake source-code implementations.

Create only:

- directory structure
- configuration
- package manifests
- tooling configuration
- infrastructure configuration
- documentation
- empty required module directories

============================================================
26. GITHUB REPOSITORY INITIALIZATION
============================================================

The user will provide a GitHub repository URL.

IMPORTANT:

Do not guess the repository URL.

When the user provides the GitHub URL:

1. Verify access.
2. Clone the repository OR initialize the existing repository safely.
3. Verify remote origin.
4. Configure Git identity.

Git identity:

User name:
Saravanan MK

GitHub email:
Saravanan MK 45 at Gmail dot com

Use the exact email supplied by the user for Git configuration.

Do not publish the email in application documentation unnecessarily.

============================================================
27. GITHUB REPOSITORY RULES
============================================================

Repository name:

AI Workforce

Use the repository URL supplied by the user.

Before first push:

Verify:

.gitignore
.env ignored
secrets ignored
credentials ignored
node_modules ignored
Python virtual environments ignored
__pycache__ ignored
build artifacts ignored
coverage ignored
IDE files ignored
OS files ignored
Docker local volumes ignored where appropriate

Add:

README.md

containing only:

- Project name
- Short description
- Architecture status
- Development status
- Documentation index
- Setup status

Do NOT claim the application is complete.

============================================================
28. SECRET SCANNING BEFORE FIRST PUSH
============================================================

Before pushing to GitHub:

Perform a repository secret scan.

Search for:

API keys
tokens
passwords
JWT secrets
private keys
cloud credentials
database credentials
OAuth secrets
AWS/S3 credentials
GitHub tokens
provider secrets

If any real secret is detected:

STOP.

Do not push.

Remove it from tracked files.

Rotate it if it was exposed.

============================================================
29. INITIAL GIT COMMIT
============================================================

After validation:

Create the first commit.

Suggested commit:

chore: initialize AI Workforce development environment

The commit must contain ONLY safe configuration and documentation.

Never include:

.env
real secrets
production credentials
private keys
fake production data
mock business data

============================================================
30. INITIAL GITHUB PUSH
============================================================

Push only after:

- secret scan PASS
- dependency validation PASS
- environment validation PASS
- repository validation PASS
- architecture consistency PASS

Push to the user-provided GitHub repository.

Verify:

git status
git remote -v
git branch
git log
GitHub repository contents

The first push must be clean.

============================================================
31. DEVELOPMENT DATABASE POLICY
============================================================

STRICT RULE:

Production database must NEVER contain mock/test/fixture data.

For automated tests:

Use isolated test database/container.

For integration tests:

Use ephemeral infrastructure where practical.

For local development:

Use explicitly labeled development databases.

Never mix:

development
test
staging
production

============================================================
32. CREATE DEVELOPMENT_SETUP_GUIDE.md
============================================================

Create a complete developer setup guide.

It must explain:

1. Prerequisites
2. Required software
3. Required versions
4. Clone repository
5. Environment setup
6. Credential setup
7. Install frontend dependencies
8. Install backend dependencies
9. Start infrastructure
10. Run migrations
11. Start backend
12. Start frontend
13. Verify health endpoints
14. Verify database
15. Verify Redis
16. Verify Qdrant
17. Verify authentication
18. Verify AI provider connectivity
19. Verify observability
20. Run tests
21. Run lint
22. Run type checks
23. Run build

No feature implementation is required.

============================================================
33. CREATE PRE_DEVELOPMENT_VALIDATION_REPORT.md
============================================================

After completing all setup, run a final validation.

Check:

[ ] Architecture stack consistent
[ ] Required runtimes installed
[ ] Required CLI tools installed
[ ] Frontend dependencies installed
[ ] Backend dependencies installed
[ ] AI dependencies installed
[ ] Infrastructure dependencies ready
[ ] PostgreSQL available
[ ] Redis available
[ ] Qdrant available
[ ] Object storage available if required
[ ] Keycloak available if required
[ ] AI gateway available if required
[ ] Observability configured
[ ] MCP environment ready
[ ] .env configured
[ ] .env.example complete
[ ] .gitignore correct
[ ] Secrets not committed
[ ] Git configured
[ ] GitHub remote configured
[ ] Initial repository pushed
[ ] No mock production data
[ ] Documentation complete

Each item must have:

PASS
FAIL
BLOCKED
NOT REQUIRED

============================================================
34. DO NOT START APPLICATION DEVELOPMENT
============================================================

STRICTLY DO NOT IMPLEMENT:

- authentication business logic
- agents
- workflows
- RAG
- UI pages
- API endpoints
- database business models
- MCP tools
- AI agents
- approval workflows
- business logic

unless required ONLY for environment validation.

This phase is infrastructure and development-readiness only.

============================================================
35. FINAL BLOCKER POLICY
============================================================

At the end, classify the project:

🟢 DEVELOPMENT READY

or

🟡 DEVELOPMENT READY WITH NON-BLOCKING ITEMS

or

🔴 NOT READY

Use 🔴 NOT READY if any critical item is missing:

- required credentials
- required runtime
- required dependency
- incompatible version
- unresolved architecture conflict
- broken infrastructure
- insecure secret handling
- GitHub repository access failure
- missing environment configuration
- critical documentation mismatch

Do NOT hide blockers.

============================================================
36. FINAL OUTPUT
============================================================

At the end provide:

A. Executive summary

B. Technology stack installed

C. Dependencies installed

D. System tools installed

E. Infrastructure services configured

F. Environment variables identified

G. Credentials available

H. Credentials still required

I. Files created

J. Files modified

K. GitHub repository status

L. Initial commit hash

M. Push status

N. Validation results

O. Remaining blockers

P. Exact next action

============================================================
37. IMPORTANT SAFETY RULES
============================================================

NEVER:

- invent credentials
- invent API keys
- invent passwords
- expose secrets
- commit .env
- commit private keys
- push secrets
- create fake production data
- silently resolve architecture conflicts
- install unnecessary packages
- change approved architecture without documenting it
- replace an approved technology without authorization
- start feature development in this phase

ALWAYS:

- use the approved architecture
- maintain environment separation
- use secure secret handling
- pin/lock compatible dependency versions
- document configuration
- validate everything
- stop on critical blockers
- keep Git history clean
- keep production data clean

============================================================
FINAL SUCCESS CONDITION
============================================================

The phase is successful ONLY when:

1. Technology stack is frozen and internally consistent.
2. All required runtimes are installed.
3. All required dependencies are installed.
4. All required local infrastructure is configured.
5. All environment variables are documented.
6. Available credentials are securely configured.
7. Missing credentials are explicitly documented.
8. .env.example files are complete.
9. .env is never committed.
10. GitHub repository is initialized correctly.
11. Git identity is configured.
12. Initial safe commit is created.
13. Initial safe push is completed.
14. Secret scan passes.
15. Environment validation passes.
16. No production mock/test data exists.
17. Development setup documentation is complete.
18. No critical blocker remains.

Only after this phase reports:

🟢 DEVELOPMENT READY

should the project proceed to actual application source-code implementation.