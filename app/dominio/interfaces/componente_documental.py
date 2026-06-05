from abc import ABC, abstractmethod

class ComponenteDocumental(ABC):
    """
    Interfaz base que cumple con ISP. 
    Solo contiene operaciones que todos los componentes (hojas y compuestos) comparten.
    """
    @abstractmethod
    def obtener_contenido(self) -> str:
        pass

    @abstractmethod
    def exportar_a_json(self) -> dict:
        pass
