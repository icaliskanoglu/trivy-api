# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial Trivy Scanner API implementation
- REST API for scanning Docker images using Trivy
- FastAPI-based web service with automatic documentation
- `/scan` endpoint for image scanning with configurable severity and scanners
- `/health` endpoint for service health checks
- Comprehensive logging for monitoring and debugging
- Docker support using aquasec/trivy base image
- Multi-platform Docker images (amd64, arm64)
- GitHub Actions CI/CD pipeline
- Automated Docker image builds on release
- Docker Compose configuration for easy deployment
- Development dependencies and code quality tools (flake8, black, isort)
