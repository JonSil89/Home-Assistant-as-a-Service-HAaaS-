# =============================================================================
# HAaaS AI Agent – Docker image
# Build context: repo root (so Python package imports resolve correctly)
# =============================================================================

FROM python:3.11-slim

# Security: run as non-root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Install dependencies first (layer cache-friendly)
COPY ai/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the AI package — keeps the image lean and the build context small
COPY ai/ ./ai/

# Switch to non-root user
USER appuser

# Expose the agent port
EXPOSE 8100

# Health check (aligns with the /health endpoint in agent.py)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8100/health')"

CMD ["uvicorn", "ai.agent.agent:app", "--host", "0.0.0.0", "--port", "8100"]
