# =============================================================================
# Opus Orchestrator AI - Dockerfile
# =============================================================================
# Build: docker build -t opus-orchestrator .
# Run:   docker run -p 8080:8080 -p 8000:8000 -e OPENAI_API_KEY=sk-... opus-orchestrator
# =============================================================================

FROM python:3.12-slim

# Labels
LABEL maintainer="mark@thefoldwithin.earth"
LABEL description="AI-powered book generation system"
LABEL version="0.2.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md install.sh ./
COPY opus_orchestrator/ ./opus_orchestrator/
COPY config.example.yaml ./

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir -e ".[all]"

# Create non-root user
RUN useradd -m -u 1000 opus && \
    chown -R opus:opus /app

# Switch to non-root user
USER opus

# Expose ports
EXPOSE 8000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command: start web UI
CMD ["python", "-m", "opus_orchestrator", "ui", "--port", "8080"]
