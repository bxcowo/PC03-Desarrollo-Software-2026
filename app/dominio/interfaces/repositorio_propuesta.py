from abc import ABC, abstractmethod
from typing import Optional
from app.dominio.propuesta import Propuesta as PropuestaEntity

class IRepositorioPropuestas(ABC):
    @abstractmethod
    def obtener_por_iniciativa(self, iniciativa_id: int) -> Optional[PropuestaEntity]:
        """Recupera una propuesta y su estructura completa por el ID de iniciativa."""
        pass

    @abstractmethod
    def guardar(self, propuesta: PropuestaEntity) -> PropuestaEntity:
        """Persiste o actualiza una propuesta y su árbol jerárquico."""
        pass

    @abstractmethod
    def verificar_autoria(self, iniciativa_id: int, ciudadano_id: int) -> bool:
        """Verifica si un ciudadano es el creador de la iniciativa asociada a la propuesta."""
        pass
