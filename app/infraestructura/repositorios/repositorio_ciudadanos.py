from typing import Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.dominio.ciudadano_entity import CiudadanoEntity
from app.dominio.interfaces.repositorio_ciudadano import IRepositorioCiudadanos
from app.infraestructura.database.models.ciudadano import Ciudadano

class RepositorioCiudadanos(IRepositorioCiudadanos):
    def __init__(self, db: Session) -> None:
        self._db = db

    def obtener_por_id(self, ciudadano_id: str) -> Optional[CiudadanoEntity]:
        # Si el ID es entero en la DB, lo convertimos
        try:
            cid = int(ciudadano_id)
        except ValueError:
            return None
        ciudadano_orm = self._db.get(Ciudadano, cid)
        return self._to_entity(ciudadano_orm) if ciudadano_orm else None

    def obtener_por_email(self, email: str) -> Optional[CiudadanoEntity]:
        stmt = select(Ciudadano).where(Ciudadano.email == email)
        ciudadano_orm = self._db.scalars(stmt).first()
        return self._to_entity(ciudadano_orm) if ciudadano_orm else None

    def obtener_por_dni_o_email(self, dni: str, email: str) -> Optional[CiudadanoEntity]:
        stmt = select(Ciudadano).where(
            or_(Ciudadano.dni == dni, Ciudadano.email == email)
        )
        ciudadano_orm = self._db.scalars(stmt).first()
        return self._to_entity(ciudadano_orm) if ciudadano_orm else None

    def guardar(self, ciudadano: CiudadanoEntity) -> CiudadanoEntity:
        ciudadano_orm = Ciudadano(
            dni=ciudadano.dni,
            nombre=ciudadano.nombre,
            email=ciudadano.email,
            hashed_password=ciudadano.hashed_password,
        )
        # Si ya tiene ID, es una actualización (aunque la interfaz guardar suele ser para nuevos o upsert)
        if ciudadano.id:
            ciudadano_orm.id = ciudadano.id
            self._db.merge(ciudadano_orm)
        else:
            self._db.add(ciudadano_orm)
        
        self._db.flush()
        return self._to_entity(ciudadano_orm)

    @staticmethod
    def _to_entity(ciudadano_orm: Ciudadano) -> CiudadanoEntity:
        return CiudadanoEntity(
            id=ciudadano_orm.id,
            dni=ciudadano_orm.dni,
            nombre=ciudadano_orm.nombre,
            email=ciudadano_orm.email,
            hashed_password=ciudadano_orm.hashed_password,
            created_at=ciudadano_orm.created_at
        )
