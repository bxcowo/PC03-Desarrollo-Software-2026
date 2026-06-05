from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dominio.propuesta import Propuesta as PropuestaEntity
from app.dominio.seccion import Seccion as SeccionEntity
from app.dominio.articulo import Articulo as ArticuloEntity
from app.dominio.interfaces.componente_documental import ComponenteDocumental
from app.dominio.interfaces.repositorio_propuesta import IRepositorioPropuestas
from app.infraestructura.database.models.iniciativa import Iniciativa as IniciativaModel
from app.infraestructura.database.models.propuesta import Propuesta as PropuestaModel
from app.infraestructura.database.models.componente_documental import ComponenteDocumental as ComponenteModel

class RepositorioPropuestas(IRepositorioPropuestas):
    def __init__(self, db: Session) -> None:
        self._db = db

    def obtener_por_iniciativa(self, iniciativa_id: int) -> Optional[PropuestaEntity]:
        stmt = select(PropuestaModel).where(PropuestaModel.iniciativa_id == iniciativa_id)
        propuesta_orm = self._db.scalars(stmt).first()
        if not propuesta_orm:
            return None

        propuesta_entity = PropuestaEntity(propuesta_orm.iniciativa_id, propuesta_orm.titulo)

        # Cargar componentes raíz (sin padre)
        raices_orm = [c for c in propuesta_orm.componentes if c.padre_id is None]
        # Ordenar raíces por el campo 'orden'
        raices_orm.sort(key=lambda x: x.orden)
        for c_orm in raices_orm:
            propuesta_entity.agregar(self._to_entity(c_orm))

        return propuesta_entity

    def guardar(self, propuesta: PropuestaEntity) -> PropuestaEntity:
        # Buscar si ya existe
        stmt = select(PropuestaModel).where(PropuestaModel.iniciativa_id == propuesta.iniciativa_id)
        propuesta_orm = self._db.scalars(stmt).first()

        if not propuesta_orm:
            propuesta_orm = PropuestaModel(
                iniciativa_id=propuesta.iniciativa_id,
                titulo=propuesta.titulo
            )
            self._db.add(propuesta_orm)
            self._db.flush()
        else:
            propuesta_orm.titulo = propuesta.titulo
            # Limpiar componentes antiguos para re-guardar el árbol
            for c in propuesta_orm.componentes:
                self._db.delete(c)
            self._db.flush()

        # Guardar el árbol de componentes
        for i, hijo in enumerate(propuesta.hijos):
            self._guardar_componente(hijo, propuesta_orm.id, None, i)

        self._db.flush()
        return propuesta

    def verificar_autoria(self, iniciativa_id: int, ciudadano_id: int) -> bool:
        stmt = select(IniciativaModel).where(
            IniciativaModel.id == iniciativa_id,
            IniciativaModel.creador_id == ciudadano_id
        )
        return self._db.scalars(stmt).first() is not None

    def _guardar_componente(self, entity: ComponenteDocumental, propuesta_id: int, padre_id: Optional[int], orden: int):
        tipo = "Seccion" if isinstance(entity, SeccionEntity) else "Articulo"
        contenido = getattr(entity, 'contenido', None) if tipo == "Articulo" else None

        c_orm = ComponenteModel(
            tipo=tipo,
            titulo=entity.titulo,
            contenido=contenido,
            orden=orden,
            propuesta_id=propuesta_id,
            padre_id=padre_id
        )
        self._db.add(c_orm)
        self._db.flush()

        if tipo == "Seccion" and hasattr(entity, 'hijos'):
            for i, hijo in enumerate(entity.hijos):
                self._guardar_componente(hijo, propuesta_id, c_orm.id, i)

    def _to_entity(self, c_orm: ComponenteModel):
        if c_orm.tipo == "Seccion":
            seccion = SeccionEntity(c_orm.titulo)
            # Ordenar hijos por el campo 'orden'
            hijos_sorted = sorted(c_orm.hijos, key=lambda x: x.orden)
            for hijo_orm in hijos_sorted:
                seccion.agregar(self._to_entity(hijo_orm))
            return seccion
        else:
            return ArticuloEntity(c_orm.titulo, c_orm.contenido or "")
