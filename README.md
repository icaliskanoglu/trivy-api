# Trivy Scanner API

[![CI](https://github.com/icaliskanoglu/trivy-api/actions/workflows/ci.yml/badge.svg)](https://github.com/icaliskanoglu/trivy-api/actions/workflows/ci.yml)
[![Build and Release](https://github.com/icaliskanoglu/trivy-api/actions/workflows/release.yml/badge.svg)](https://github.com/icaliskanoglu/trivy-api/actions/workflows/release.yml)

A REST API service for scanning Docker images using [Trivy](https://github.com/aquasecurity/trivy), built with FastAPI and Python.

## Features

- Scan Docker images for vulnerabilities and security issues
- RESTful API with JSON responses
- Configurable severity levels and scanner types
- Built on the official Trivy Docker image
- Automatic API documentation with Swagger/OpenAPI
- Health check endpoint
- Comprehensive logging for monitoring and debugging
- Multi-platform Docker images (amd64, arm64)
- Automated CI/CD with GitHub Actions

## Quick Start

### Using Pre-built Docker Image (Easiest)

Pull and run the latest release from GitHub Container Registry:

```bash
# Pull the latest image
docker pull ghcr.io/icaliskanoglu/trivy-api:latest

# Run the container
docker run -d \
  -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --name trivy-api \
  ghcr.io/icaliskanoglu/trivy-api:latest
```

Or use a specific version:
```bash
docker pull ghcr.io/icaliskanoglu/trivy-api:v1.0.0
```

The API will be available at `http://localhost:8000`

### Using Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

The API will be available at `http://localhost:8000`

### Using Docker

```bash
# Build the image
docker build -t trivy-api .

# Run the container
docker run -d \
  -p 8000:8000 \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --name trivy-api \
  trivy-api
```

### Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Trivy (if not already installed)
# See: https://aquasecurity.github.io/trivy/latest/getting-started/installation/

# Run the application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### Health Check

```bash
GET /health
```

Returns the health status of the service and Trivy version.

Example:
```bash
curl http://localhost:8000/health
```

### Scan Docker Image

```bash
POST /scan
```

Scan a Docker image and return vulnerabilities as JSON.

**Request Body:**
```json
{
  "image": "nginx:latest",
  "severity": "HIGH,CRITICAL",
  "scanners": "vuln,secret"
}
```

**Parameters:**
- `image` (required): Docker image to scan (e.g., `nginx:latest`, `alpine:3.18`)
- `severity` (optional): Comma-separated severities (default: `UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL`)
- `scanners` (optional): Comma-separated scanners (default: `vuln,secret`)
  - Available: `vuln`, `secret`, `config`, `license`

**Example:**
```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "image": "nginx:latest",
    "severity": "HIGH,CRITICAL"
  }'
```

**Response:**
```json
{
  "image": "nginx:latest",
  "scan_result": {
    "SchemaVersion": 2,
    "ArtifactName": "nginx:latest",
    "Results": [
      {
        "Target": "nginx:latest (debian 12.5)",
        "Vulnerabilities": [...]
      }
    ]
  }
}
```

### API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Examples

### Scan for Critical Vulnerabilities Only

```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "image": "alpine:3.18",
    "severity": "CRITICAL"
  }'
```

### Scan for Vulnerabilities and Secrets

```bash
curl -X POST http://localhost:8000/scan \
  -H "Content-Type: application/json" \
  -d '{
    "image": "myapp:latest",
    "scanners": "vuln,secret"
  }'
```

### Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/scan",
    json={
        "image": "nginx:latest",
        "severity": "HIGH,CRITICAL"
    }
)

result = response.json()
print(f"Scanned: {result['image']}")
print(f"Results: {result['scan_result']}")
```

## Configuration

### Environment Variables

- `TRIVY_CACHE_DIR`: Directory for Trivy cache (default: `/root/.cache/trivy`)

### Volume Mounts

- `/var/run/docker.sock`: Required for scanning local Docker images
- Trivy cache volume: Improves performance by caching vulnerability database

## Project Structure

```
trivy-api/
├── .github/
│   └── workflows/
│       ├── ci.yml        # Continuous Integration
│       └── release.yml   # Build and Release workflow
├── app/
│   ├── __init__.py
│   └── main.py           # FastAPI application
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Development dependencies
├── .gitignore
├── .dockerignore
└── README.md
```

## Development

### Setting Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run the application in development mode
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Code Quality Tools

```bash
# Run linting
flake8 app/

# Format code
black app/

# Sort imports
isort app/
```

### Viewing Logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f trivy-api

# View last 100 lines
docker-compose logs --tail=100 trivy-api
```

## CI/CD and Releases

This project uses GitHub Actions for continuous integration and automated releases.

### Continuous Integration

Every push and pull request triggers:
- Code linting with flake8
- Code formatting checks with black
- Import sorting checks with isort
- Docker image build test
- Container health check test

### Releases

Creating a release from the GitHub UI automatically builds and publishes Docker images:

#### Create a Release

1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Click **Choose a tag** and create a new tag (e.g., `v1.0.0`)
   - Use semantic versioning: `v{major}.{minor}.{patch}`
   - Examples: `v1.0.0`, `v1.2.3`, `v2.0.0`
4. Fill in release title and description
5. Click **Publish release**

#### What Happens Automatically

When you publish a release, GitHub Actions will:
- Trigger on the new tag
- Build multi-platform Docker images (amd64, arm64)
- Push images to GitHub Container Registry with tags:
  - `v1.0.0` - Specific version
  - `1.0` - Major.minor version
  - `1` - Major version
  - `latest` - Latest release
  - `sha-abc1234` - Specific commit
- Update the release notes with Docker pull commands and quick start guide

### Available Image Tags

- `latest` - Latest release
- `v1.0.0` - Specific version tags (e.g., v1.2.3)
- `sha-abc1234` - Specific commit SHA

Pull images from:
```bash
ghcr.io/icaliskanoglu/trivy-api:latest
ghcr.io/icaliskanoglu/trivy-api:v1.0.0
```

## Troubleshooting

### Trivy database download fails

If you see errors about downloading the vulnerability database, ensure your container has internet access.

### Permission denied for Docker socket

Ensure the Docker socket is mounted with appropriate permissions:
```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock:ro ...
```

### Scan timeout

Large images may take time to scan. The default timeout is 5 minutes. You can modify this in `app/main.py:101`.

## License

This project is provided as-is for educational and development purposes.

## Credits

- [Trivy](https://github.com/aquasecurity/trivy) by Aqua Security
- [FastAPI](https://fastapi.tiangolo.com/)
