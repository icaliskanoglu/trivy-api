FROM aquasec/trivy:latest

# Install Python and pip
RUN apk add --no-cache python3 py3-pip python3-dev build-base

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
# Using --break-system-packages is safe in containers (isolated environment)
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Override the base image's ENTRYPOINT to run our app instead of trivy
ENTRYPOINT []

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
