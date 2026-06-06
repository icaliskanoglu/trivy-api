# Trivy Scanner API - Project Instructions

FastAPI-based REST API wrapping Trivy vulnerability scanner. See @README.md for full documentation.

## Project Structure

```
app/main.py           # FastAPI application with /scan and /health endpoints
Dockerfile            # Uses aquasec/trivy:0.71.0 base image
requirements.txt      # Production dependencies (all pinned)
requirements-dev.txt  # Dev tools: black, isort, flake8, pytest
.github/workflows/    # CI (lint, build, test) and Release (tag-triggered)
```

## Version Pinning Policy

**CRITICAL:** Always pin all dependency versions - never use `latest` or unpinned versions.

- **Trivy**: Update `TRIVY_VERSION` ARG in Dockerfile (currently `0.71.0`)
- **Python packages**: Specify exact versions in requirements files
- **GitHub Actions**: Pin to major versions (e.g., `@v6`, `@v4`)

**Reason:** Ensures reproducible builds and consistent scan results across all environments.

## Code Quality Standards

**Before committing, always run:**
```bash
black app/           # Format code (88 char line length)
isort app/           # Sort imports (profile: "black")
flake8 app/          # Lint code
```

**Import sorting:** Blank line required between stdlib and third-party imports.

**Logging:** Use `logger.info/error/debug` extensively throughout code.

## Git Commit Format

```
Short description (imperative mood)

- Bullet point details
- Multiple lines OK

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Build Commands

```bash
# Local development
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Docker
docker-compose up --build -d
docker-compose logs -f

# Code quality
black app/ && isort app/ && flake8 app/
```

## Release Process

**Trigger:** Create GitHub release with tag `v{major}.{minor}.{patch}`

**GitHub UI:**
1. Releases → Create new release
2. Create tag: `v1.0.0` (semantic versioning)
3. Add description
4. Publish

**CLI:**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**Auto-triggers:** Multi-platform build (amd64, arm64), push to ghcr.io, release notes update.

## CI/CD Workflows

**CI (`.github/workflows/ci.yml`):**
- Triggers: Push/PR to main
- Runs: flake8, black --check, isort --check, docker build+test

**Release (`.github/workflows/release.yml`):**
- Triggers: Tag push matching `v*`
- Runs: Multi-platform build, push to GitHub Container Registry

## Critical Technical Details

**Dockerfile:**
- Must clear `ENTRYPOINT []` (Trivy base image sets it to `trivy`)
- Use `--break-system-packages` for pip (safe in containers)
- ARG `TRIVY_VERSION` for version control

**Docker Build in CI:**
- Must use `load: true` to make image available for testing

**FastAPI:**
- Scan timeout: 300 seconds (configurable in app/main.py:135)
- Temp file cleanup: Always unlink after use
- Error handling: Use HTTPException with appropriate status codes

## Common Pitfalls

1. **Forgot to run black/isort** → CI fails
2. **Used `latest` tag** → Breaks reproducibility
3. **Missing `load: true` in CI** → Docker test fails with "image not found"
4. **Changed ENTRYPOINT** → Container doesn't start correctly

## File Locations

- FastAPI app: `app/main.py`
- Dockerfile: `Dockerfile` (TRIVY_VERSION at line 3)
- Dependencies: `requirements.txt` and `requirements-dev.txt`
- CI config: `.github/workflows/ci.yml`
- Release config: `.github/workflows/release.yml`
- User docs: `README.md`
- Changelog: `CHANGELOG.md`

## Dependency Versions (as of June 2026)

**Production:**
- fastapi==0.136.3
- uvicorn[standard]==0.49.0
- pydantic==2.13.4
- python-multipart==0.0.32

**Development:**
- black==26.5.1
- isort==7.0.0
- flake8==7.3.0
- pytest==9.0.3
- pytest-asyncio==1.4.0
- httpx==0.28.1

**Docker Base:**
- aquasec/trivy:0.71.0
