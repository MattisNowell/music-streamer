from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary
from src import db

class Track(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False)
    artist: Mapped[str] = mapped_column(unique=False) # To become an attribute linking to a user in the future user/account table 
    data: Mapped[bytes] = mapped_column(LargeBinary)
