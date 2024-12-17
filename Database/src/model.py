from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import database

class Track(database.db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    artist: Mapped[str]

    