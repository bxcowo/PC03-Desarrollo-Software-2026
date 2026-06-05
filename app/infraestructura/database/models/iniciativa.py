from __future__ import annotations
from app.infraestructura.database.base import BaseModel
from app.dominio.enums.estado_iniciativa import EstadoIniciativaEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from datetime import datetime, UTC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infraestructura.database.models.firma import Firma

class Iniciativa(BaseModel):
    __tablename__ = "iniciativas"

    titulo: Mapped[str] = mapped_column(String(512), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(4096), nullable=False)
    estado: Mapped[EstadoIniciativaEnum] = mapped_column(
        nullable=False,
        default=EstadoIniciativaEnum.ACTIVA,
    )
    total_firmas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(UTC))
    fecha_limite: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    sellado_hash: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)

    firmas: Mapped[list[Firma]] = relationship(back_populates="iniciativa")
