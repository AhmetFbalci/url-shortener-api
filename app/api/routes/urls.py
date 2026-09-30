from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemes.url import UrlCreate
from app.services.url_service import create_short_url,redirect_link


router = APIRouter()


@router.post("/urls")
def create_url(data:UrlCreate,db:Session=Depends(get_db)):
    return create_short_url(
        db=db,
        original_url=str(data.original_url)
    )


@router.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    return redirect_link(
        db=db,
        code=short_code
    )