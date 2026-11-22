# ETAPA 1: Construcción
FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90 AS builder

WORKDIR /build

# Copiar las dependencias con versiones fijadas
COPY requirements.lock.txt .

# Instalar las versiones exactas
RUN pip install --no-cache-dir \
    --prefix=/install \
    -r requirements.lock.txt


# ETAPA 2: Ejecución
FROM python:3.13-slim@sha256:e48f59cdba69a3cbd9ed2cf0f348d90d45a8d350d98134cf1070bc106ee9ed90

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar únicamente las dependencias instaladas
COPY --from=builder /install /usr/local

# Copiar el código de la aplicación
COPY app/ ./app/

# Crear usuario sin privilegios con UID y GID fijos
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --no-create-home appuser

# Ejecutar sin privilegios de root
USER 10001:10001

# Puerto del microservicio
EXPOSE 8001

# Iniciar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
