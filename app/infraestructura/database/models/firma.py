from __future__ import annotations
from app.infraestructura.database.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, Boolean
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infraestructura.database.models.ciudadano import Ciudadano
    from app.infraestructura.database.models.iniciativa import Iniciativa


class Firma(BaseModel):
    __tablename__ = "firmas"
    __table_args__ = (
        UniqueConstraint("ciudadano_id", "iniciativa_id", name="uq_firma_ciudadano_iniciativa"),
    )

    ciudadano_id: Mapped[int] = mapped_column(ForeignKey("ciudadanos.id"))
    iniciativa_id: Mapped[int] = mapped_column(ForeignKey("iniciativas.id"))
    es_valida: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    ciudadano: Mapped[Ciudadano] = relationship(back_populates="firmas")
    iniciativa: Mapped[Iniciativa] = relationship(back_populates="firmas")
