from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.dominio.firma_entity import FirmaEntity
from app.dominio.interfaces.repositorio_firma import IRepositorioFirmas
from app.infraestructura.database.models.firma import Firma


class RepositorioFirmas(IRepositorioFirmas):
    def __init__(self, db: Session) -> None:
        self._db = db

    def obtener_por_ciudadano_e_iniciativa(
        self, ciudadano_id: int, iniciativa_id: int
    ) -> Optional[FirmaEntity]:
        stmt = select(Firma).where(
            Firma.ciudadano_id == ciudadano_id,
            Firma.iniciativa_id == iniciativa_id,
        )
        firma_orm = self._db.scalars(stmt).first()
        return self._to_entity(firma_orm) if firma_orm else None

    def guardar(self, firma: FirmaEntity) -> FirmaEntity:
        firma_orm = Firma(
            ciudadano_id=firma.ciudadano_id,
            iniciativa_id=firma.iniciativa_id,
            es_valida=firma.es_valida,
        )
        self._db.add(firma_orm)
        self._db.flush()
        return self._to_entity(firma_orm)

    def contar_por_iniciativa(self, iniciativa_id: int) -> int:
        stmt = select(func.count()).select_from(Firma).where(
            Firma.iniciativa_id == iniciativa_id,
            Firma.es_valida.is_(True),
        )
        return self._db.scalar(stmt) or 0

    @staticmethod
    def _to_entity(firma_orm: Firma) -> FirmaEntity:
        return FirmaEntity(
            id=firma_orm.id,
            ciudadano_id=firma_orm.ciudadano_id,
            iniciativa_id=firma_orm.iniciativa_id,
            es_valida=firma_orm.es_valida,
        )
