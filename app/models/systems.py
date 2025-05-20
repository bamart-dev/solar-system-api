from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import db

class System(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    planets: Mapped[list["Planet"]] = relationship(back_populates="system")


    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "planets": self.planets if self.planets else None,
        }


    @classmethod
    def generate_system(cls, system_data):

        return cls(name = system_data["name"])
