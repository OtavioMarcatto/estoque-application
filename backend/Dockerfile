# Stage 1: dependências
FROM python:3.12-slim AS deps
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -e "."

# Stage 2: produção
FROM python:3.12-slim AS production
WORKDIR /app

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY backend/app ./app
COPY backend/alembic ./alembic
COPY backend/alembic.ini .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:8000"]
