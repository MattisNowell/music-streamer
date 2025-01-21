from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary
from datetime import date
from src import db

class Track(db.Model):
    __tablename__ = "track"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    artist: Mapped[str] = mapped_column(unique=False) # To become an attribute linking to a user in the future user/account table 
    data: Mapped[bytes] = mapped_column(LargeBinary)
    cover: Mapped[bytes] = mapped_column(LargeBinary)
    release_date: Mapped[date] = mapped_column(nullable=True)