FROM python:3.9-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.11.19 /uv /uvx /bin/

WORKDIR /home/package

COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN uv sync --frozen --no-install-project
