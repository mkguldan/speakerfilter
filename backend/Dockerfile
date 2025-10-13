# Multi-stage build for optimized production image
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port (Cloud Run uses PORT environment variable, defaults to 8080)
EXPOSE 8080

# Set default port if not provided
ENV PORT=8080

# Run the application
# Note: --limit-max-requests removed (0 causes immediate shutdown)
# Cloud Run will use the PORT environment variable
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT} --timeout-keep-alive 300



