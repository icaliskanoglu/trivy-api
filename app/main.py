import json
import logging
import subprocess
import tempfile
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Trivy Scanner API",
    description="REST API for scanning Docker images using Trivy",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Log application startup"""
    logger.info("Starting Trivy Scanner API")
    logger.info("API version: 1.0.0")
    logger.info("Ready to accept requests")


class ScanRequest(BaseModel):
    image: str = Field(
        ..., description="Docker image to scan (e.g., 'nginx:latest', 'alpine:3.18')"
    )
    severity: Optional[str] = Field(
        default="UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL",
        description="Comma-separated list of severities to include (UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL)",
    )
    scanners: Optional[str] = Field(
        default="vuln,secret",
        description="Comma-separated list of scanners to use (vuln,secret,config,license)",
    )


class ScanResponse(BaseModel):
    image: str
    scan_result: dict


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Trivy Scanner API",
        "version": "1.0.0",
        "endpoints": {
            "/scan": "POST - Scan a Docker image",
            "/health": "GET - Health check",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    logger.info("Health check requested")
    try:
        # Check if trivy is available
        result = subprocess.run(
            ["trivy", "--version"], capture_output=True, text=True, timeout=5
        )
        trivy_available = result.returncode == 0

        if trivy_available:
            logger.info(f"Health check passed - Trivy version: {result.stdout.strip()}")
        else:
            logger.warning("Health check degraded - Trivy not responding correctly")

        return {
            "status": "healthy" if trivy_available else "degraded",
            "trivy_available": trivy_available,
            "trivy_version": result.stdout.strip() if trivy_available else None,
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e)}


@app.post("/scan", response_model=ScanResponse)
async def scan_image(request: ScanRequest):
    """
    Scan a Docker image using Trivy and return vulnerabilities as JSON

    Args:
        request: ScanRequest containing image name and scan options

    Returns:
        ScanResponse with scan results
    """
    logger.info(f"Received scan request for image: {request.image}")
    logger.info(
        f"Scan parameters - Severity: {request.severity}, Scanners: {request.scanners}"
    )

    try:
        # Create a temporary file to store the JSON output
        with tempfile.NamedTemporaryFile(
            mode="w+", suffix=".json", delete=False
        ) as tmp_file:
            output_file = tmp_file.name

        logger.debug(f"Created temporary output file: {output_file}")

        # Build trivy command
        trivy_cmd = [
            "trivy",
            "image",
            "--format",
            "json",
            "--output",
            output_file,
            "--severity",
            request.severity,
            "--scanners",
            request.scanners,
            request.image,
        ]

        logger.info(f"Executing Trivy command: {' '.join(trivy_cmd)}")

        # Run trivy scan
        logger.info(f"Starting scan of image: {request.image}")
        result = subprocess.run(
            trivy_cmd, capture_output=True, text=True, timeout=300  # 5 minutes timeout
        )

        logger.info(f"Trivy scan completed with return code: {result.returncode}")

        if result.stdout:
            logger.debug(f"Trivy stdout: {result.stdout}")
        if result.stderr:
            logger.debug(f"Trivy stderr: {result.stderr}")

        # Read the JSON output
        logger.info("Reading scan results from output file")
        with open(output_file, "r") as f:
            scan_result = json.load(f)

        # Clean up temp file
        import os

        os.unlink(output_file)
        logger.debug(f"Cleaned up temporary file: {output_file}")

        # Check if scan completed successfully
        if result.returncode != 0 and not scan_result:
            logger.error(
                f"Trivy scan failed for image {request.image}: {result.stderr}"
            )
            raise HTTPException(
                status_code=500, detail=f"Trivy scan failed: {result.stderr}"
            )

        # Count vulnerabilities if available
        vuln_count = 0
        if "Results" in scan_result:
            for res in scan_result.get("Results", []):
                if "Vulnerabilities" in res and res["Vulnerabilities"]:
                    vuln_count += len(res["Vulnerabilities"])

        logger.info(
            f"Scan completed successfully for {request.image}. Found {vuln_count} vulnerabilities"
        )

        return ScanResponse(image=request.image, scan_result=scan_result)

    except subprocess.TimeoutExpired:
        logger.error(f"Scan timeout exceeded for image: {request.image}")
        raise HTTPException(status_code=504, detail="Scan timeout exceeded (5 minutes)")
    except FileNotFoundError:
        logger.error("Trivy executable not found")
        raise HTTPException(
            status_code=500, detail="Trivy not found. Please ensure Trivy is installed."
        )
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Trivy JSON output: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to parse Trivy output: {str(e)}"
        )
    except Exception as e:
        logger.error(
            f"Unexpected error during scan of {request.image}: {str(e)}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
