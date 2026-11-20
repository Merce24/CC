
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

# Copiar el código de la aplicación
COPY app/ ./app/

# Crear usuario sin privilegios con UID y GID fijos
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --no-create-home appuser

# Ejecutar sin privilegios de root
USER 10001:10001

# Puerto del microservicio
EXPOSE 8002

# Iniciar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
