FROM python:3.12-slim

# Python çalışma ortamı optimizasyonları
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Sağlık kontrolü ve ağ tanıları için curl kurulumu
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama ve veritabanı migration dosyalarını kopyala
COPY alembic.ini .
COPY alembic ./alembic
COPY app ./app

# Güvenlik için non-root kullanıcı oluştur
RUN addgroup --system appgroup && adduser --system --group appuser \
    && chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

# Sağlık kontrolü (Docker healthcheck)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Uvicorn ile FastAPI uygulamasını başlat
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'"]
