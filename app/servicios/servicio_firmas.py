import hashlib
from datetime import datetime, UTC
from typing import Any

from sqlalchemy.orm import Session

from app.config import settings
from app.dominio.decoradores.decorador_validacion import DecoradorValidacionFirma, ValidadorBase
from app.dominio.firma_entity import FirmaEntity
from app.dominio.iniciativa_entity import IniciativaEntity
from app.dominio.enums.estado_iniciativa import EstadoIniciativaEnum
from app.dominio.facades.fachada_verificacion import FachadaVerificacionIdentidad
from app.infraestructura.repositorios.repositorio_firmas import RepositorioFirmas
from app.infraestructura.repositorios.repositorio_ciudadanos import RepositorioCiudadanos
from app.infraestructura.repositorios.repositorio_iniciativas import RepositorioIniciativas
from app.infraestructura.proxys.proxy_repositorio_firmas import ProxyRepositorioFirmas


class ServicioFirmas:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._fachada = FachadaVerificacionIdentidad()
        self._validador = DecoradorValidacionFirma(ValidadorBase())

        self._repo_ciudadano = RepositorioCiudadanos(db)
        self._repo_iniciativa = RepositorioIniciativas(db)

        repo_firmas_real = RepositorioFirmas(db)
        self._repo_firma = ProxyRepositorioFirmas(repo_firmas_real)

    def registrar_firma(
        self,
        ciudadano_id: str,
        iniciativa_id: str,
    ) -> dict[str, Any]:
        ciudadano = self._repo_ciudadano.obtener_por_id(ciudadano_id)
        if ciudadano is None:
            raise ValueError(f"Ciudadano '{ciudadano_id}' no encontrado.")

        iniciativa = self._repo_iniciativa.obtener_por_id(iniciativa_id)
        if iniciativa is None:
            raise ValueError(f"Iniciativa '{iniciativa_id}' no encontrada.")

        self._fachada.validar_ciudadano(
            dni=ciudadano.dni
        )

        firma_entity = FirmaEntity(
            id=None,
            ciudadano_id=int(ciudadano_id),
            iniciativa_id=int(iniciativa_id),
            es_valida=True,
        )
        self._validador.validar(firma_entity, iniciativa)

        firma_guardada = self._repo_firma.guardar(firma_entity)

        iniciativa.total_firmas += 1

        if iniciativa.total_firmas >= settings.FIRMA_LIMITE:
            self._sellar_iniciativa(iniciativa)

        self._repo_iniciativa.actualizar(iniciativa)
        self._db.commit()

        return {
            "firma_id": firma_guardada.id,
            "iniciativa_id": iniciativa_id,
            "total_firmas": iniciativa.total_firmas,
            "estado": iniciativa.estado.value,
            "sellado_hash": iniciativa.sellado_hash,
        }

    def listar_iniciativas_activas(self) -> list[dict[str, Any]]:
        iniciativas = self._repo_iniciativa.listar_activas()
        return [
            {
                "id": str(i.id),
                "titulo": i.titulo,
                "descripcion": i.descripcion,
                "estado": i.estado.value,
                "total_firmas": i.total_firmas,
                "firma_limite": settings.FIRMA_LIMITE,
                "progreso_pct": round(
                    (i.total_firmas / settings.FIRMA_LIMITE) * 100, 2
                ),
                "fecha_inicio": i.fecha_inicio.isoformat(),
                "fecha_limite": i.fecha_limite.isoformat(),
            }
            for i in iniciativas
        ]

    @staticmethod
    def _sellar_iniciativa(iniciativa: IniciativaEntity) -> None:
        timestamp = datetime.now(UTC).isoformat()
        payload = f"{iniciativa.id}:{iniciativa.total_firmas}:{timestamp}"
        sellado_hash = hashlib.sha256(payload.encode()).hexdigest()
        iniciativa.sellado_hash = sellado_hash
        iniciativa.estado = EstadoIniciativaEnum.SELLADA
        print(
            f"[SEAL] Iniciativa '{iniciativa.id}' sellada. "
            f"Hash: {sellado_hash} | Timestamp: {timestamp}"
        )
