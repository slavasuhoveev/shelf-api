# Base image for building (shared by dev and prod)
FROM python:3.12.4-slim AS base_build

# Set working directory inside the container
WORKDIR /app

# Environment variables
ENV \
    PYTHONPATH=/app/src \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

# Install system dependencies and Poetry
RUN apt-get update && apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
    libpq-dev \
    gcc \
    curl \
    && curl -sSL 'https://install.python-poetry.org' | python3 - \
    && poetry --version \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy lockfile and pyproject to leverage Docker cache
COPY poetry.lock pyproject.toml ./

# -----------------------
# Development build stage
# -----------------------
FROM base_build AS development

# Install all dependencies including dev dependencies
RUN poetry install --no-interaction --no-ansi

# Copy application code and migration files
COPY src/ ./src
COPY alembic.ini ./
COPY alembic/ ./alembic/

# --------------------
# Production build stage
# --------------------
FROM base_build AS production

# Install only main dependencies for production
RUN poetry install --no-interaction --no-ansi --only main

# Copy only necessary source code and config
COPY src/ ./src
COPY alembic.ini ./
COPY alembic/ ./alembic/

# --------------------
# Final runtime stage
# --------------------
FROM python:3.12.4-slim AS final

# Set working directory
WORKDIR /app

# Copy Python environment and app from previous stage (prod or dev)
COPY --from=development /usr/local /usr/local
COPY --from=development /app /app

# Set Python path to recognize 'src' structure
ENV PYTHONPATH=/app/src
