from __future__ import annotations
from app.infraestructura.database.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.infraestructura.database.models.iniciativa import Iniciativa
    from app.infraestructura.database.models.componente_documental import ComponenteDocumental

class Propuesta(BaseModel):
    __tablename__ = "propuestas"

    iniciativa_id: Mapped[int] = mapped_column(ForeignKey("iniciativas.id"), unique=True)
    titulo: Mapped[str] = mapped_column(String(512), nullable=False)

    # Usamos string para evitar problemas de circularidad en tiempo de ejecución
    componentes: Mapped[List["ComponenteDocumental"]] = relationship(
        "ComponenteDocumental",
        back_populates="propuesta", 
        cascade="all, delete-orphan"
    )
