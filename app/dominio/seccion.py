from typing import List
from app.dominio.interfaces.componente_documental import ComponenteDocumental

class Seccion(ComponenteDocumental):
    def __init__(self, titulo: str) -> None:
        self.titulo = titulo
        self.hijos: List[ComponenteDocumental] = []

    def obtener_contenido(self) -> str:
        contenido = f"Sección: {self.titulo}\n"
        for hijo in self.hijos:
            contenido += hijo.obtener_contenido() + "\n"
        return contenido

    def exportar_a_json(self) -> dict:
        return {
            "tipo": "Seccion",
            "titulo": self.titulo,
            "hijos": [hijo.exportar_a_json() for hijo in self.hijos]
        }

    def agregar(self, componente: ComponenteDocumental) -> None:
        self.hijos.append(componente)

    def eliminar(self, componente: ComponenteDocumental) -> None:
        self.hijos.remove(componente)
