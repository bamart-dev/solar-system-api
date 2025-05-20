from sqlalchemy.orm import Mapped, mapped_column
from app.db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    atmosphere: Mapped[str]


    def to_dict(self):
        """Return dictionary representation of Planet object."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "atmosphere": self.atmosphere,
        }


    @classmethod
    def generate_planet(cls, planet_data):

        return cls(
            name = planet_data["name"],
            description = planet_data["description"],
            atmosphere = planet_data["atmosphere"],
        )
