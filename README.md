# 🔗 URL Shortener API

FastAPI, PostgreSQL ve Redis kullanılarak geliştirilmiş, hızlı, sade ve yüksek performanslı bir **URL Kısaltma REST API** servisi.

Uzun web bağlantılarını benzersiz kısa kodlara dönüştürür, Redis önbelleklemesi (caching) ile yüksek hızda yönlendirme yapar ve tıklanma istatistiklerini takip eder.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

---

## ✨ Özellikler

- **URL Kısaltma:** Uzun bağlantıları 6 karakterlik rastgele ve benzersiz kısa kodlara dönüştürür.
- **Yüksek Hızlı Yönlendirme (Redis Cache):** Popüler linkler Redis önbelleğinde tutulur; veritabanına yük bindirmeden anında yönlendirilir.
- **Tıklanma Sayacı:** Her yönlendirmede linkin toplam kaç kez tıklandığı veritabanında güncellenir.
- **Süre Sınırı (Expiration):** Kısaltılan bağlantılar için geçerlilik süresi belirlenebilir; süresi dolan bağlantılar otomatik olarak kapatılır.
- **Docker Desteği:** PostgreSQL ve Redis bağımlılıkları Docker Compose ile tek komutla ayağa kaldırılabilir.
- **Otomatik Dokümantasyon:** Swagger UI (`/docs`) ve ReDoc (`/redoc`) üzerinden interaktif API testi.

---

## 🛠️ Teknolojiler

- **Backend:** Python 3.12, FastAPI, Uvicorn
- **Veritabanı & ORM:** PostgreSQL, SQLAlchemy, Alembic (Migration)
- **Önbellek:** Redis
- **Veri Doğrulama:** Pydantic v2
- **Konteynerizasyon:** Docker & Docker Compose

---

## 🚀 Hızlı Başlangıç

### Yöntem 1: Docker ile Çalıştırma (Önerilen)

Projeyi PostgreSQL ve Redis ile birlikte tek komutla başlatmak için:

```bash
docker compose up -d
```

Servisler ayağa kalktıktan sonra API [http://localhost:8000](http://localhost:8000) adresinden erişilebilir olacaktır.

---

### Yöntem 2: Yerel Ortamda Çalıştırma (Local Development)

#### 1. Depoyu klonlayın ve dizine gidin:
```bash
git clone https://github.com/KULLANICI_ADINIZ/url-shortener-api.git
cd url-shortener-api
```

#### 2. Sanal ortamı oluşturun ve aktifleştirin:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows için: .venv\Scripts\activate
```

#### 3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

#### 4. Ortam değişkenlerini ayarlayın:
`.env.example` dosyasını `.env` olarak kopyalayın:
```bash
cp .env.example .env
```
`.env` dosyasını kendi PostgreSQL ve Redis bağlantı bilgilerinize göre düzenleyin:
```ini
POSTGRES_PASSWORD=1234
DATABASE_URL=postgresql+psycopg://url_user:1234@localhost:5432/url_shortener
REDIS_URL=redis://localhost:6379
```

#### 5. PostgreSQL ve Redis'i başlatın:
Eğer sisteminizde kurulu değilse Docker Compose ile sadece veritabanlarını başlatabilirsiniz:
```bash
docker compose up -d postgres redis
```

#### 6. Veritabanı tablolarını oluşturun:
```bash
alembic upgrade head
```

#### 7. Sunucuyu başlatın:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📡 API Uç Noktaları (Endpoints)

### 1. URL Kısalt
- **Endpoint:** `POST /urls`
- **Açıklama:** Uzun bir URL alır ve kısaltılmış link bilgisini döner.

**Örnek İstek (cURL):**
```bash
curl -X POST "http://localhost:8000/urls" \
     -H "Content-Type: application/json" \
     -d '{"original_url": "https://www.google.com"}'
```

**Örnek İstek Gövdesi (JSON):**
```json
{
  "original_url": "https://www.google.com"
}
```

**Örnek Başarılı Yanıt (200 OK):**
```json
{
  "id": 1,
  "original_url": "https://www.google.com/",
  "short_code": "k7Xy9Z",
  "created_at": "2026-10-01T00:00:00Z",
  "expired_at": "2026-10-02T00:00:00Z",
  "click_count": 0
}
```

---

### 2. Kısa Link ile Yönlendirme
- **Endpoint:** `GET /{short_code}`
- **Açıklama:** Kısa kodu hedef orijinal adrese yönlendirir (`302 Found`).
- **Örnek:** Tarayıcınızda veya istekte `http://localhost:8000/k7Xy9Z` adresine gittiğinizde orijinal linke yönlenirsiniz.

---

### 3. Sistem Sağlık Kontrolü
- **Endpoint:** `GET /health`
- **Açıklama:** PostgreSQL ve Redis bağlantılarının çalışır durumda olduğunu doğrular.

**Örnek Yanıt:**
```json
{
  "status": "ok",
  "postgres": "connected",
  "redis": "connected"
}
```

---

### 4. İnteraktif API Dokümantasyonu
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📂 Proje Yapısı

```text
Url-Shortener-Api/
├── alembic/                # Veritabanı göç (migration) dosyaları
├── app/
│   ├── api/
│   │   └── routes/         # API endpoint rotaları (/urls, /{short_code})
│   ├── core/               # Konfigürasyon ve ayarlar (.env)
│   ├── db/                 # Veritabanı ve Redis bağlantı motorları
│   ├── models/             # SQLAlchemy ORM modelleri
│   ├── schemes/            # Pydantic doğrulama şemaları
│   ├── services/           # İş mantığı (kod üretimi, redis, yönlendirme)
│   └── main.py             # FastAPI uygulama başlangıcı
├── docker-compose.yml      # Postgres ve Redis konteyner ayarları
├── requirements.txt        # Python bağımlılıkları
└── README.md
```

---

