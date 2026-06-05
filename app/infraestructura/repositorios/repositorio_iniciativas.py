from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dominio.iniciativa_entity import IniciativaEntity
from app.dominio.enums.estado_iniciativa import EstadoIniciativaEnum
from app.dominio.interfaces.repositorio_iniciativa import IRepositorioIniciativas
from app.infraestructura.database.models.iniciativa import Iniciativa

class RepositorioIniciativas(IRepositorioIniciativas):
    def __init__(self, db: Session) -> None:
        self._db = db

    def obtener_por_id(self, iniciativa_id: str) -> Optional[IniciativaEntity]:
        try:
            iid = int(iniciativa_id)
        except ValueError:
            return None
        iniciativa_orm = self._db.get(Iniciativa, iid)
        return self._to_entity(iniciativa_orm) if iniciativa_orm else None

    def listar_activas(self) -> List[IniciativaEntity]:
        stmt = select(Iniciativa).where(
            Iniciativa.estado == EstadoIniciativaEnum.ACTIVA
        )
        iniciativas_orm = self._db.scalars(stmt).all()
        return [self._to_entity(i) for i in iniciativas_orm]

    def actualizar(self, iniciativa: IniciativaEntity) -> IniciativaEntity:
        iniciativa_orm = self._db.get(Iniciativa, iniciativa.id)
        if not iniciativa_orm:
            raise ValueError(f"Iniciativa con ID {iniciativa.id} no encontrada")
        
        iniciativa_orm.titulo = iniciativa.titulo
        iniciativa_orm.descripcion = iniciativa.descripcion
        iniciativa_orm.estado = iniciativa.estado
        iniciativa_orm.total_firmas = iniciativa.total_firmas
        iniciativa_orm.sellado_hash = iniciativa.sellado_hash
        
        self._db.flush()
        return self._to_entity(iniciativa_orm)

    @staticmethod
    def _to_entity(iniciativa_orm: Iniciativa) -> IniciativaEntity:
        return IniciativaEntity(
            id=iniciativa_orm.id,
            titulo=iniciativa_orm.titulo,
            descripcion=iniciativa_orm.descripcion,
            estado=iniciativa_orm.estado,
            total_firmas=iniciativa_orm.total_firmas,
            fecha_inicio=iniciativa_orm.fecha_inicio,
            fecha_limite=iniciativa_orm.fecha_limite,
            sellado_hash=iniciativa_orm.sellado_hash
        )
