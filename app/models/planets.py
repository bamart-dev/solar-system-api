from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from app.db import db


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    atmosphere: Mapped[str]
    system_id: Mapped[Optional[int]] = mapped_column(ForeignKey("system.id"))
    system: Mapped[Optional["System"]] = relationship(back_populates="planets")


    def to_dict(self):
        """Return dictionary representation of Planet object."""
        planet = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "atmosphere": self.atmosphere,
        }

        if self.system:
            planet["system"] = self.system

        return planet


    @classmethod
    def generate_planet(cls, planet_data):

        return cls(
            name = planet_data["name"],
            description = planet_data["description"],
            atmosphere = planet_data["atmosphere"],
            system_id = planet_data.get("system_id"),
        )
