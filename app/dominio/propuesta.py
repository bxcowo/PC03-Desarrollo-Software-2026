from typing import List
from app.dominio.interfaces.componente_documental import ComponenteDocumental

class Propuesta(ComponenteDocumental):
    def __init__(self, iniciativa_id: int, titulo: str) -> None:
        self.iniciativa_id = iniciativa_id
        self.titulo = titulo
        self.hijos: List[ComponenteDocumental] = []

    def obtener_contenido(self) -> str:
        contenido = f"Propuesta Normativa: {self.titulo}\n"
        contenido += "=" * len(contenido) + "\n"
        for hijo in self.hijos:
            contenido += hijo.obtener_contenido() + "\n"
        return contenido

    def exportar_a_json(self) -> dict:
        return {
            "tipo": "Propuesta",
            "iniciativa_id": self.iniciativa_id,
            "titulo": self.titulo,
            "hijos": [hijo.exportar_a_json() for hijo in self.hijos]
        }

    def agregar(self, componente: ComponenteDocumental) -> None:
        self.hijos.append(componente)

    def eliminar(self, componente: ComponenteDocumental) -> None:
        self.hijos.remove(componente)
