FROM python:3.11-slim

# Reproducibilidad / ruido mínimo
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# deps del sistema mínimos
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
  && rm -rf /var/lib/apt/lists/*

# Instala tooling Python (ruff/pytest/coverage/uv opcional)
RUN python -m pip install -U pip setuptools wheel \
 && python -m pip install -U ruff pytest coverage hypothesis

# Copia repo
COPY . .

# Instala tu paquete en modo editable (src/)
RUN python -m pip install -e ".[dev]"

# Default: gates (igual que CI)
CMD python -m ruff format --check . && \
    python -m ruff check . && \
    python -m pytest -q && \
    python -m coverage run --source=src -m pytest -q && \
    python -m coverage report -m --fail-under=95
