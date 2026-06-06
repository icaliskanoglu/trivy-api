# Trivy Scanner API - Claude Code Documentation

This document provides comprehensive information about the Trivy Scanner API project for AI assistants and developers.

## Project Overview

**Name:** Trivy Scanner API
**Repository:** https://github.com/icaliskanoglu/trivy-api
**Purpose:** REST API service for scanning Docker images using Aqua Security's Trivy scanner
**Technology Stack:** Python 3.14, FastAPI, Docker, Trivy
**Container Registry:** GitHub Container Registry (ghcr.io)

### What This Project Does

Provides a web service that wraps Trivy (a vulnerability scanner) in a REST API, allowing users to:
- Scan Docker images for vulnerabilities via HTTP POST requests
- Configure severity levels (UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL)
- Choose scanner types (vulnerabilities, secrets, configs, licenses)
- Get results as structured JSON responses
- Check service health via dedicated endpoint

## Project Structure

```
trivy-api/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Continuous Integration workflow
│       └── release.yml         # Build and Release workflow
├── app/
│   ├── __init__.py            # Python package marker
│   └── main.py                # FastAPI application (core logic)
├── .dockerignore              # Docker build exclusions
├── .gitignore                 # Git exclusions
├── CHANGELOG.md               # Version history
├── claude.md                  # This file - AI assistant documentation
├── Dockerfile                 # Container image definition
├── docker-compose.yml         # Local deployment configuration
├── README.md                  # User-facing documentation
├── requirements.txt           # Production Python dependencies
└── requirements-dev.txt       # Development Python dependencies
```

## Core Components

### 1. FastAPI Application (`app/main.py`)

**Endpoints:**
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint (verifies Trivy availability)
- `POST /scan` - Main scanning endpoint
- `GET /docs` - Auto-generated Swagger/OpenAPI documentation
- `GET /redoc` - Auto-generated ReDoc documentation

**Key Features:**
- Comprehensive logging for all operations
- Temporary file management for scan results
- Proper error handling with HTTP status codes
- Pydantic models for request/response validation
- 5-minute timeout for large image scans

### 2. Dockerfile

**Base Image:** `aquasec/trivy:0.71.0` (pinned version)
**Build Strategy:**
- ARG-based version control for Trivy
- Multi-stage approach not used (single stage for simplicity)
- Python installed via Alpine apk
- Break-system-packages flag used (safe in containers)

**Important:** Trivy version is pinned via `TRIVY_VERSION` ARG to ensure consistency across all releases.

### 3. Docker Compose

**Purpose:** Local development and testing
**Features:**
- Mounts Docker socket for scanning local images
- Persistent volume for Trivy cache
- Port 8000 exposed
- Restart policy: unless-stopped

## Development Methodology

### Version Pinning Strategy

**Philosophy:** All dependencies are pinned to specific versions for:
- Reproducible builds across all environments
- Consistent behavior in production
- Controlled upgrades with proper testing
- Easier debugging and troubleshooting

**Pinned Components:**
1. **Trivy Version** (Dockerfile ARG): `0.71.0`
2. **Python Dependencies** (requirements.txt): All packages pinned
3. **Development Tools** (requirements-dev.txt): All packages pinned
4. **GitHub Actions**: All actions use specific versions (v6, v4, etc.)

### Code Quality Standards

**Formatters & Linters:**
- **Black** (v26.5.1): Code formatting, enforced in CI
- **isort** (v7.0.0): Import sorting with Black compatibility
- **Flake8** (v7.3.0): Linting and style checking

**Configuration:**
- isort profile: "black" (for compatibility)
- Black line length: default (88 characters)
- Flake8: E9, F63, F7, F82 errors fail build

**Testing:**
- **pytest** (v9.0.3): Testing framework
- **pytest-asyncio** (v1.4.0): Async test support
- **httpx** (v0.28.1): HTTP client for testing FastAPI

### Git Workflow

**Branching:**
- `main` branch: Production-ready code
- Feature branches: Not required (small project)
- Direct commits to main allowed

**Commit Messages:**
- Clear, descriptive commit messages
- Multi-line format with bullet points for details
- Co-authored by Claude Code notation

**Example:**
```
Fix code formatting and CI Docker build test

- Format code with black to pass CI checks
- Add load: true to CI workflow
- This fixes the Docker image not found error

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## CI/CD Pipeline

### Continuous Integration (ci.yml)

**Triggers:**
- Push to main branch
- Pull requests to main

**Jobs:**

1. **lint** (Python 3.14, Ubuntu latest)
   - Install dependencies from requirements-dev.txt
   - Run flake8 (errors and warnings)
   - Check Black formatting
   - Check isort import sorting

2. **docker-build** (Ubuntu latest)
   - Build Docker image with Buildx
   - Load image for testing (`load: true`)
   - Run container
   - Test health endpoint with curl
   - View logs

**GitHub Actions Versions:**
- actions/checkout@v6
- actions/setup-python@v6
- docker/setup-buildx-action@v4
- docker/build-push-action@v7

### Release Workflow (release.yml)

**Trigger:** Tag push (pattern: `v*`)

**Process:**
1. Extract version from tag (e.g., v1.0.0 → 1.0.0)
2. Build multi-platform images (linux/amd64, linux/arm64)
3. Push to GitHub Container Registry
4. Tag images with:
   - Specific version (e.g., 1.0.0)
   - Major.minor (e.g., 1.0)
   - Major (e.g., 1)
   - latest
   - SHA
5. Update release notes with Docker pull commands

**GitHub Actions Versions:**
- actions/checkout@v6
- docker/setup-buildx-action@v4
- docker/login-action@v3
- docker/metadata-action@v6
- docker/build-push-action@v7
- softprops/action-gh-release@v3

## Release Process

### How to Create a Release

**From GitHub UI (Recommended):**
1. Navigate to repository → Releases → "Create a new release"
2. Click "Choose a tag" → Create new tag (e.g., `v1.0.0`)
   - Use semantic versioning: `v{major}.{minor}.{patch}`
3. Fill in release title and description
4. Click "Publish release"

**From Command Line:**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

**What Happens Automatically:**
- GitHub Actions workflow triggers
- Multi-platform Docker images built
- Images pushed to ghcr.io/icaliskanoglu/trivy-api
- Release notes updated with Docker commands
- Multiple image tags created

### Semantic Versioning

**Format:** `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking API changes
- **MINOR:** New features (backwards compatible)
- **PATCH:** Bug fixes (backwards compatible)

**Example:** v1.2.3
- 1 = Major version
- 2 = Minor version
- 3 = Patch version

## Dependency Management

### Current Versions (as of June 2026)

**Production Dependencies (requirements.txt):**
```
fastapi==0.136.3
uvicorn[standard]==0.49.0
pydantic==2.13.4
python-multipart==0.0.32
```

**Development Dependencies (requirements-dev.txt):**
```
-r requirements.txt
flake8==7.3.0
black==26.5.1
isort==7.0.0
pytest==9.0.3
pytest-asyncio==1.4.0
httpx==0.28.1
```

**Docker Base Image:**
```
aquasec/trivy:0.71.0
```

**GitHub Actions:**
- checkout: v6
- setup-python: v6
- setup-buildx-action: v4
- build-push-action: v7
- metadata-action: v6
- login-action: v3
- action-gh-release: v3

### Updating Dependencies

**Python Dependencies:**
1. Update version in requirements.txt or requirements-dev.txt
2. Test locally
3. Update in commit message
4. Ensure CI passes

**Trivy Version:**
1. Update `TRIVY_VERSION` ARG in Dockerfile
2. Update version in README.md (Configuration section)
3. Update CHANGELOG.md
4. Test Docker build locally
5. Create release

**GitHub Actions:**
1. Update version numbers in .github/workflows/*.yml
2. Test workflows in pull request
3. Merge when green

## Changelog Management

### Format

Based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

**Sections:**
- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Security fixes

### Process

1. Update `CHANGELOG.md` with changes under `[Unreleased]`
2. On release, move `[Unreleased]` items to new version section
3. Add release date
4. Create new `[Unreleased]` section

**Example:**
```markdown
## [Unreleased]

## [1.0.0] - 2026-06-06
### Added
- Initial release
- REST API for Trivy scanning
```

## Common Tasks

### Local Development

```bash
# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Run application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Code formatting
black app/
isort app/
flake8 app/

# Testing
pytest
```

### Docker Development

```bash
# Build locally
docker build -t trivy-api:local .

# Run locally
docker run -d -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  trivy-api:local

# Using docker-compose
docker-compose up --build -d
docker-compose logs -f
docker-compose down
```

### Testing the API

```bash
# Health check
curl http://localhost:8000/health

# Scan an image
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"image": "nginx:latest", "severity": "HIGH,CRITICAL"}'

# View API docs
open http://localhost:8000/docs
```

## Important Notes for AI Assistants

### When Working on This Project

1. **Always Pin Versions:** Never use `latest` or unpinned versions
2. **Test Locally First:** Ensure changes work before committing
3. **Run Code Quality Tools:** Black, isort, flake8 before committing
4. **Update Documentation:** Keep README.md and claude.md in sync
5. **Update CHANGELOG:** Document all changes
6. **Check CI:** Ensure all workflows pass

### Code Style Preferences

- **Logging:** Use logger.info/error/debug extensively
- **Error Handling:** Specific HTTPExceptions with appropriate status codes
- **Type Hints:** Use Optional, str, dict from typing
- **Docstrings:** Use triple-quoted strings for functions
- **Comments:** Explain "why" not "what"

### Common Pitfalls

1. **Docker ENTRYPOINT:** Must be cleared (`ENTRYPOINT []`) because Trivy base image sets it
2. **pip in Alpine:** Requires `--break-system-packages` flag (safe in containers)
3. **Docker Buildx:** Must use `load: true` to make image available for testing
4. **Import Sorting:** Must add blank line between stdlib and third-party imports

## Project History

### Initial Development

**Created:** June 2026
**Initial Developer:** Ihsan Caliskanoglu
**AI Assistant:** Claude Code (Anthropic)

**Initial Commits:**
```
da283f5 Initial implementation of Trivy Scanner API
fa63851 Fix code formatting and CI Docker build test
e6dac0d Fix import sorting with isort
1b611f3 Update dependencies and pin Trivy version
ae9dd6b Add Trivy version pinning for release consistency
```

### Key Decisions

1. **FastAPI over Flask:** Modern, async support, automatic docs
2. **Trivy Docker Image:** Official image, well-maintained
3. **Version Pinning:** Reproducibility and consistency
4. **GitHub Container Registry:** Free for public repos, integrated
5. **Multi-platform Builds:** Support both amd64 and arm64

## Troubleshooting Guide

### Common Issues

**Issue:** CI fails with "Black would reformat"
**Solution:** Run `black app/` locally and commit

**Issue:** CI fails with "Imports incorrectly sorted"
**Solution:** Run `isort app/` locally and commit

**Issue:** Docker build fails with pip error
**Solution:** Check `--break-system-packages` flag is present

**Issue:** Health check fails in CI
**Solution:** Ensure `load: true` is set in docker build action

**Issue:** Trivy scan timeout
**Solution:** Increase timeout in app/main.py (default: 300 seconds)

## Future Enhancements

Potential improvements to consider:

- [ ] Add authentication/API keys
- [ ] Support for scanning from private registries
- [ ] Database for scan history
- [ ] Webhook notifications for scan completion
- [ ] Rate limiting
- [ ] Metrics and monitoring (Prometheus)
- [ ] Support for SBOM generation
- [ ] Batch scanning support
- [ ] Scheduled scans
- [ ] Web UI for results visualization

## Contact & Support

**Repository:** https://github.com/icaliskanoglu/trivy-api
**Issues:** https://github.com/icaliskanoglu/trivy-api/issues
**Discussions:** https://github.com/icaliskanoglu/trivy-api/discussions

## License

This project is provided as-is for educational and development purposes.

---

**Last Updated:** June 6, 2026
**Document Version:** 1.0
**Maintained By:** Ihsan Caliskanoglu & Claude Code
