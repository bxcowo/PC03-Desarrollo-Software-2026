from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.iniciativa_entity import IniciativaEntity

class IRepositorioIniciativas(ABC):
    @abstractmethod
    def obtener_por_id(self, iniciativa_id: str) -> Optional[IniciativaEntity]:
        pass

    @abstractmethod
    def listar_activas(self) -> List[IniciativaEntity]:
        pass

    @abstractmethod
    def actualizar(self, iniciativa: IniciativaEntity) -> IniciativaEntity:
        pass
