# Multi-stage Dockerfile for Snake Game
# Stage 1: Build frontend
FROM node:20-alpine as frontend-builder
WORKDIR /app/frontend

# Copy frontend files
COPY package*.json ./
RUN npm ci

# Build frontend (output to dist)
RUN npm run build 2>/dev/null || echo "No build script, copying static files"

# Stage 2: Build backend with Python
FROM python:3.13-slim as backend-builder
WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy backend files
COPY backend/pyproject.toml backend/uv.lock* ./
RUN uv sync --frozen

# Copy application code
COPY backend/ .

# Stage 3: Final runtime image
FROM python:3.13-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Copy Python virtual environment from builder
COPY --from=backend-builder /app/backend/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy backend application
COPY --from=backend-builder /app/backend /app/backend
WORKDIR /app/backend

# Copy frontend static files (if built) or original files
COPY --from=frontend-builder /app/frontend /app/frontend

# Expose ports
# 8000: FastAPI backend
# 3000: Frontend (if needed for development)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start FastAPI backend
# Frontend files will be served via FastAPI static file handler
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
