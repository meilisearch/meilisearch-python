FROM python:3.9-buster

COPY pyproject.toml .
COPY uv.lock .

RUN apt-get update -y

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.16 /uv /uvx /bin/

# Install dependencies
RUN uv sync --frozen --no-install-project
