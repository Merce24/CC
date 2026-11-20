
# ETAPA 1: Construcción
FROM python:3.13-slim AS builder

WORKDIR /build

# Instalar dependencias
COPY requirements.txt .

RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.txt


# ETAPA 2: Ejecución
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar las dependencias instaladas
COPY --from=builder /install /usr/local

# Copiar el código del microservicio
COPY app/ ./app/

# Crear usuario sin privilegios
RUN groupadd --system appuser \
    && useradd --system --gid appuser appuser

USER appuser

# Puerto del microservicio
EXPOSE 8003

# Arrancar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
