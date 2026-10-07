# DEVELOPER SETUP & QUICKSTART GUIDE
## AI Workforce — Autonomous Business Workflow Automation Platform
**Document Identifier:** DSG-AIWF-2026-001  
**Version:** 1.0.0 | **Status:** PUBLISHED  
**Audience:** Platform Developers & Onboarding Engineers  

---

## 1. PREREQUISITES & REQUIRED SOFTWARE

Before starting, ensure the host system has the following runtimes and utilities installed:

| Software | Minimum Version | Recommended Version | Download / Installation Location |
|---|---|---|---|
| **Git** | 2.40+ | 2.50+ | [https://git-scm.com/](https://git-scm.com/) |
| **Node.js** | 20.x LTS | 20.x or 24.x | [https://nodejs.org/](https://nodejs.org/) |
| **Python** | 3.11.x | 3.11.9 | [https://www.python.org/downloads/](https://www.python.org/downloads/) |
| **Docker Desktop** | 24.0+ / Compose v2.20+ | Latest | [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/) |

---

## 2. REPOSITORY CLONING & GIT INITIALIZATION

```bash
# Clone the repository (replace with user repository URL)
git clone <REPOSITORY_URL> "AI Workforce"
cd "AI Workforce"

# Verify Git configuration
git config user.name "Saravanan MK"
git config user.email "saravananmk45@gmail.com"
```

---

## 3. ENVIRONMENT & CREDENTIAL SETUP

```bash
# 1. Copy the root environment template
cp .env.example .env

# 2. Copy the backend environment template
cp backend/.env.example backend/.env

# 3. Copy the frontend environment template
cp frontend/.env.example frontend/.env

# 4. Generate local cryptographic keys (if needed)
# On Linux/macOS or Git Bash:
# openssl rand -hex 32      -> Paste into MASTER_ENCRYPTION_KEY
# openssl rand -base64 64   -> Paste into JWT_SECRET_KEY
```

> **IMPORTANT**: Review `MISSING_CREDENTIALS.md` and `CREDENTIAL_SETUP_GUIDE.md` if configuring live OpenAI, Anthropic, or Langfuse keys.

---

## 4. LOCAL INFRASTRUCTURE STARTUP (DOCKER)

Start all backing datastores (PostgreSQL 16, Redis 7.2, Qdrant 1.9, MinIO, MailHog):

```bash
docker-compose up -d
```

Verify service health:
```bash
docker-compose ps
```

---

## 5. BACKEND DEPENDENCY INSTALLATION & MIGRATIONS

```bash
cd backend

# Create and activate Python virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate

# Install backend dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run initial database schema migrations (when DB is up)
alembic upgrade head
```

---

## 6. FRONTEND DEPENDENCY INSTALLATION

```bash
cd ../frontend

# Install dependencies via npm
npm install
```

---

## 7. STARTING SERVICES LOCALLY

### Start Backend API:
```bash
# From backend directory with active virtual environment:
uvicorn app.main:app --reload --port 8000
```
- OpenAPI Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Health Check: [http://localhost:8000/v1/healthz](http://localhost:8000/v1/healthz)

### Start Celery Worker (In separate terminal):
```bash
# From backend directory:
celery -A app.worker worker --loglevel=INFO
```

### Start Frontend Web App:
```bash
# From frontend directory:
npm run dev
```
- Web Application: [http://localhost:5173](http://localhost:5173)

---

## 8. SYSTEM VERIFICATION CHECKLIST

Verify each sub-service after startup:

1. **Database (PostgreSQL)**:
   ```bash
   docker exec -it aiwf-postgres-dev pg_isready -U aiwf_user -d aiwf_dev
   ```
2. **Cache & Broker (Redis)**:
   ```bash
   docker exec -it aiwf-redis-dev redis-cli ping
   ```
   *Expected response: `PONG`*
3. **Vector Database (Qdrant)**:
   Navigate to [http://localhost:6333/dashboard](http://localhost:6333/dashboard) or run:
   ```bash
   curl http://localhost:6333/readyz
   ```
4. **Object Storage (MinIO)**:
   Navigate to [http://localhost:9001](http://localhost:9001)  
   Login: `minio_admin` / `minio_password_123`
5. **Email Sandbox (MailHog)**:
   Navigate to [http://localhost:8025](http://localhost:8025)

---

## 9. CODE QUALITY, TESTING & BUILD COMMANDS

### Backend Tests & Linting:
```bash
cd backend
ruff check .           # Run Ruff linter
ruff format .          # Run Ruff code formatter
mypy .                 # Run static type checker
pytest                 # Execute Pytest suite
```

### Frontend Tests, Linting & Build:
```bash
cd frontend
npm run lint           # Run ESLint
npm run test           # Run Vitest test runner
npm run build          # Validate production bundle compilation
```

---

*AI Workforce Platform — Developer Onboarding Guide*
