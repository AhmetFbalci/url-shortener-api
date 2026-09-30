

from sqlalchemy import Column,String,INTEGER,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from app.db.database import Base

class Url(Base):
    __tablename__="Url"
    id:Mapped[int]=mapped_column(primary_key=True)
    original_url:Mapped[str]=mapped_column(String,nullable=False)
    short_code:Mapped[str]=mapped_column(String(10),unique=True,nullable=False)
    created_at:Mapped[DateTime]=mapped_column(DateTime(timezone=True),nullable=False)
    expired_at:Mapped[DateTime]=mapped_column(DateTime(timezone=True),nullable=False)
    click_count:Mapped[int]=mapped_column(INTEGER,default=0,nullable=False)


