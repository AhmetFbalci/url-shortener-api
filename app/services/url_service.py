
import secrets
import string
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from fastapi.responses import RedirectResponse
from app.db.redis import redis_client
from sqlalchemy.orm import Session
from app.models.url_models import  Url

from app.models.url_models import Url


def generate_short_code(len:int=6):
    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(len)
    )



def create_short_url(db: Session, original_url: str) -> Url:
    while True:
        short_code = generate_short_code()

        existing = (
            db.query(Url)
            .filter(Url.short_code == short_code)
            .first()
        )

        if not existing:
            break

    url = Url(
        original_url=original_url,
        short_code=short_code,
        created_at=datetime.now(timezone.utc),
        expired_at=datetime.now(timezone.utc)+timedelta(days=1)


    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url


def redirect_link(db:Session,code:str):
    cached_url=redis_client.get(f"url:{code}")

    if cached_url:
        return RedirectResponse(
            url=cached_url,
            status_code=302
        )

    url_db=db.query(Url).filter(Url.short_code==code).first()

    if not url_db:
        raise HTTPException(status_code=404,detail="Url bulunamadı")

    now =datetime.now(timezone.utc)

    if url_db.expired_at and url_db.expired_at<=now:
        raise HTTPException(status_code=410,
            detail="URL'nin süresi dolmuş"
        )

    if url_db.expired_at:
        remaining_seconds = int(
            (url_db.expired_at - now).total_seconds()
        )

        redis_client.set(
            f"url:{code}",
            url_db.original_url,
            ex=remaining_seconds
        )

        # Tıklanma sayısını artır
    url_db.click_count += 1
    db.commit()

    return RedirectResponse(
        url=url_db.original_url,
        status_code=302
    )