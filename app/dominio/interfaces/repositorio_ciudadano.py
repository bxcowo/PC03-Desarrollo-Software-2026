from abc import ABC, abstractmethod
from typing import Optional
from app.dominio.ciudadano_entity import CiudadanoEntity

class IRepositorioCiudadanos(ABC):
    @abstractmethod
    def obtener_por_id(self, ciudadano_id: str) -> Optional[CiudadanoEntity]:
        pass

    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[CiudadanoEntity]:
        pass

    @abstractmethod
    def obtener_por_dni_o_email(self, dni: str, email: str) -> Optional[CiudadanoEntity]:
        pass

    @abstractmethod
    def guardar(self, ciudadano: CiudadanoEntity) -> CiudadanoEntity:
        pass
