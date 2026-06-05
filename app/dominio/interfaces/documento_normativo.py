from abc import ABC, abstractmethod
from app.dominio.recurso_extraido import RecursoExtraido

class IDocumentoNormativo(ABC):
    @abstractmethod
    def extraer_informacion(self) -> RecursoExtraido:
        pass
