from sqlalchemy.orm import Mapped, mapped_column
from app.db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    atmosphere: Mapped[str]
