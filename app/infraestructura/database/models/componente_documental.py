from __future__ import annotations
from app.infraestructura.database.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from app.infraestructura.database.models.propuesta import Propuesta

class ComponenteDocumental(BaseModel):
    __tablename__ = "componentes_documentales"

    tipo: Mapped[str] = mapped_column(String(50)) # 'Seccion' o 'Articulo'
    titulo: Mapped[str] = mapped_column(String(512), nullable=False)
    contenido: Mapped[Optional[str]] = mapped_column(String(4096), nullable=True)
    orden: Mapped[int] = mapped_column(Integer, default=0)

    propuesta_id: Mapped[int] = mapped_column(ForeignKey("propuestas.id"))
    padre_id: Mapped[Optional[int]] = mapped_column(ForeignKey("componentes_documentales.id"), nullable=True)

    # Usamos strings para las relaciones para evitar errores de carga circular
    propuesta: Mapped["Propuesta"] = relationship("Propuesta", back_populates="componentes")
    hijos: Mapped[List["ComponenteDocumental"]] = relationship(
        "ComponenteDocumental",
        cascade="all, delete-orphan",
        back_populates="padre"
    )
    padre: Mapped[Optional["ComponenteDocumental"]] = relationship(
        "ComponenteDocumental",
        back_populates="hijos", 
        remote_side="ComponenteDocumental.id"
    )
