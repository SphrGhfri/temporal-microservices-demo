FROM python:3.12-slim 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY producers/ ./producers

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "-m", "producers.main"]