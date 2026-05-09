# --------------------
# Base image
# --------------------
FROM python:3.12.4-slim AS base_build

WORKDIR /app

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

# Copy dependency files
COPY poetry.lock pyproject.toml ./

# --------------------
# Development stage
# --------------------
FROM base_build AS development

RUN poetry install \
    --no-interaction \
    --no-ansi \
    --with dev

COPY src/ ./src
COPY alembic.ini ./
COPY alembic/ ./alembic/

# --------------------
# Test stage
# --------------------
FROM base_build AS tests

RUN poetry install \
    --no-interaction \
    --no-ansi \
    --with dev,test

COPY src/ ./src
COPY tests/ ./tests
COPY alembic.ini ./
COPY alembic/ ./alembic/

CMD ["pytest"]

# --------------------
# Production stage
# --------------------
FROM base_build AS production

RUN poetry install \
    --no-interaction \
    --no-ansi \
    --only main

COPY src/ ./src
COPY alembic.ini ./
COPY alembic/ ./alembic/

# --------------------
# Final runtime image
# --------------------
FROM python:3.12.4-slim AS final

WORKDIR /app

COPY --from=production /usr/local /usr/local
COPY --from=production /app /app

ENV PYTHONPATH=/app/src
