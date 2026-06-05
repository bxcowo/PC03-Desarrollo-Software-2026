from abc import ABC, abstractmethod
from app.dominio.firma_entity import FirmaEntity
from app.dominio.iniciativa_entity import IniciativaEntity

class IValidadorFirma(ABC):
    @abstractmethod
    def validar(self, firma: FirmaEntity, iniciativa: IniciativaEntity) -> bool: ...
