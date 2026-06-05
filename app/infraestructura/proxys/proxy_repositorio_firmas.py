from datetime import datetime, UTC
from typing import Optional
from app.dominio.firma_entity import FirmaEntity
from app.dominio.interfaces.repositorio_firma import IRepositorioFirmas


class ProxyRepositorioFirmas(IRepositorioFirmas):
    """
        Verifica duplicados y registra auditoría antes de delegar al repositorio real.
    """

    def __init__(self, repositorio_real: IRepositorioFirmas) -> None:
        self._real = repositorio_real

    def obtener_por_ciudadano_e_iniciativa(
        self, ciudadano_id: int, iniciativa_id: int
    ) -> Optional[FirmaEntity]:
        return self._real.obtener_por_ciudadano_e_iniciativa(ciudadano_id, iniciativa_id)

    def guardar(self, firma: FirmaEntity) -> FirmaEntity:
        existente = self._real.obtener_por_ciudadano_e_iniciativa(
            firma.ciudadano_id, firma.iniciativa_id
        )
        if existente is not None:
            self._audit("DUPLICADO_BLOQUEADO", firma.ciudadano_id, firma.iniciativa_id)
            raise ValueError(
                f"El ciudadano '{firma.ciudadano_id}' ya firmó la iniciativa '{firma.iniciativa_id}'."
            )
        resultado = self._real.guardar(firma)
        self._audit("FIRMA_GUARDADA", firma.ciudadano_id, firma.iniciativa_id)
        return resultado

    def contar_por_iniciativa(self, iniciativa_id: int) -> int:
        return self._real.contar_por_iniciativa(iniciativa_id)

    @staticmethod
    def _audit(evento: str, ciudadano_id: int, iniciativa_id: int) -> None:
        timestamp = datetime.now(UTC).isoformat()
        print(f"[AUDIT] {timestamp} | evento={evento} | ciudadano={ciudadano_id} | iniciativa={iniciativa_id}")
