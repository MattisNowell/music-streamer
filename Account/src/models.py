from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary
from flask_login import UserMixin
from src import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    picture: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

# The tag user_loader allows flask to execute this function when flask needs to retrieve the user.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

