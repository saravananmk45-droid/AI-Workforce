AI WORKFORCE — FINAL PRE-DEVELOPMENT SETUP

Before starting ANY application feature coding, fully prepare this project for development.

Use ALL available source documents as the source of truth:

- Final BRD PDF
- Final User Story Catalogue PDF
- Final Architecture Decision Baseline PDF
- All corresponding .md files
- System Architecture Specification
- Database Design Specification
- API Specification
- UI/UX Design Specification
- DevSecOps Specification
- Environment Configuration Requirements
- Tool Sandboxing Specification
- Requirements Traceability
- Final Audit Report

Complete EVERYTHING required for pre-development:

1. Freeze and validate the approved technology stack.
2. Identify and install ALL required frontend and backend dependencies with compatible versions.
3. Install required runtimes, SDKs, CLI tools and development tools.
4. Configure frontend and backend `.env` files.
5. Create/update `.env.example` files.
6. Use ONLY free-tier/free APIs and services wherever possible. If a service is not free, select a suitable free alternative.
7. Use the credentials I previously provided ONLY where an external login is genuinely required. Never hardcode or commit credentials.
8. Configure PostgreSQL/database, migrations and required infrastructure.
9. Configure Redis, Qdrant/vector DB, object storage and every other service required by the approved architecture.
10. Configure authentication/Keycloak if required.
11. Configure LLM/AI providers using free options wherever available.
12. Configure Swagger/OpenAPI so APIs can be tested directly from Swagger UI.
13. Verify database connectivity.
14. Verify all infrastructure/service health.
15. Verify frontend ↔ backend connectivity.
16. Verify Swagger API calls with safe test data only.
17. Configure Docker/local development environment if required.
18. Configure logging, OpenTelemetry/Langfuse and observability if required.
19. Configure MCP/tooling according to the approved architecture.
20. Configure testing, linting, formatting and type-checking.
21. Configure `.gitignore` and secret protection.
22. NEVER commit `.env`, passwords, API keys, tokens or private credentials.
23. Do NOT create fake/mock production data.
24. Keep development, test, staging and production environments separated.
25. Resolve any dependency/version/configuration mismatch before declaring readiness.
26. Do NOT change the approved architecture without documenting and validating the change.
27. Do NOT start feature/business-logic development yet.

After setup, run a COMPLETE pre-development validation covering:

- Environment
- Dependencies
- Frontend
- Backend
- Database
- Redis
- Qdrant
- Authentication
- AI providers
- Swagger
- API connectivity
- Docker/infrastructure
- MCP
- Observability
- Testing
- Security
- Git/GitHub readiness

Create/update all required setup and validation documentation.

FINAL REQUIREMENT:

Do not return "Development Ready" until everything required before coding is actually configured and tested.

If something is missing, do not hide it or invent it. Clearly identify the blocker and what is required.

Only when all critical checks PASS, return:

🟢 PRE-DEVELOPMENT COMPLETE — GOOD TO GO FOR DEVELOPMENT

Then provide a concise summary of:
- what was installed
- what was configured
- APIs verified
- database verified
- services verified
- remaining non-blocking items, if any
- exact command/steps to start frontend and backend development.

Before the next Git push, clean the repository tracking:

- Add all unnecessary `.md` files and PDFs inside `docs/` to `.gitignore`.
- Keep only the officially required project documentation files that are explicitly approved for Git.
- Do NOT delete the files locally.
- If any unnecessary `.md` files or PDFs are already tracked/committed, remove them from Git tracking using `git rm --cached` without deleting the local files.
- Verify `.gitignore` rules.
- Run `git status` and confirm no unwanted docs/PDFs are staged.
- Do NOT remove or modify required source code, configuration, `.env.example`, or approved documentation.
- Do NOT commit or push secrets.

After cleanup, commit and push only the intended repository files.