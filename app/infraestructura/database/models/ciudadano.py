from __future__ import annotations
from app.infraestructura.database.base import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.infraestructura.database.models.firma import Firma

class Ciudadano(BaseModel):
    __tablename__ = "ciudadanos"

    dni: Mapped[str] = mapped_column(String(8), unique=True, nullable=False, index=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    firmas: Mapped[list[Firma]] = relationship(back_populates="ciudadano")
