# install dependencies
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \ 
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

# default use of the venv
ENV PATH="/app/.venv/bin:$PATH"

COPY . .

# runs using Uvicorn
CMD ["Uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]