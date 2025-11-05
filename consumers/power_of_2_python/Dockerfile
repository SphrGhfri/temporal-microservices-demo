FROM python:3.12-slim 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY consumers/power_of_2_python ./consumers/power_of_2_python

ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "-m", "consumers.power_of_2_python.main"]