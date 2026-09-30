from fastapi import FastAPI

from app.db.database import engine
from app.db.redis import redis_client

from app.api.routes.urls import router as url_router


app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
)
app.include_router(url_router)

@app.get("/")
def root():
    return {
        "message": "URL Shortener API çalışıyor"
    }


@app.get("/health")
def health_check():
    # Redis bağlantısını kontrol et
    redis_client.ping()

    # PostgreSQL bağlantısını kontrol et
    with engine.connect():
        pass

    return {
        "status": "ok",
        "postgres": "connected",
        "redis": "connected",
    }