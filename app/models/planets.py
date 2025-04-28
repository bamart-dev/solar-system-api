from sqlalchemy.orm import Mapped, mapped_column
from app.db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    atmosphere: Mapped[str]


# planets = [
#     Planet(1, "Cat Head Planet", "cat head shaped planet with large red spots", "cat's bathhouse cafe"),
#     Planet(2, "Clown Planet", "clown shaped planet", "scary yet fun and full of balloons"),
#     Planet(3, "Donut Planet", "donut shaped planet with a black hole in the center", "non-existant"),
#     Planet(4, "Jelly Cube", "perfect pink cube shaped planet with a sugared cherry at the bottom", "cannibalistic"),
#     Planet(5, "Palm Planet", "shaped like a large etheral palm with its fingers folded upward", "surface is a mixtrue of blue and purple gas")
# ]
