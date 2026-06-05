from abc import ABC, abstractmethod
from typing import Optional
from app.dominio.firma_entity import FirmaEntity

class IRepositorioFirmas(ABC):

    @abstractmethod
    def obtener_por_ciudadano_e_iniciativa(
        self, ciudadano_id: int, iniciativa_id: int
    ) -> Optional[FirmaEntity]: ...

    @abstractmethod
    def guardar(self, firma: FirmaEntity) -> FirmaEntity: ...

    @abstractmethod
    def contar_por_iniciativa(self, iniciativa_id: int) -> int: ...
