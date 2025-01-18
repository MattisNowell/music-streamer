from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary
from datetime import date

def create_track_model(db):
    class Track(db.Model):
        __tablename__ = "tracks"

        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column()
        artist: Mapped[str] = mapped_column()  # Placeholder for future relationships
        data: Mapped[bytes] = mapped_column(LargeBinary)
        cover: Mapped[bytes] = mapped_column(LargeBinary)
        release_date: Mapped[date] = mapped_column(nullable=True)

    return Track