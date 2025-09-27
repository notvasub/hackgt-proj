FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir fastapi uvicorn[standard] pydantic pydantic-settings orjson httpx python-jose[cryptography] sse-starlette

COPY app ./app
COPY Makefile ./

ENV APP_PORT=8080 APP_HOST=0.0.0.0

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

