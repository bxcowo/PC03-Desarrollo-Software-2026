from app.dominio.interfaces.componente_documental import ComponenteDocumental

class Articulo(ComponenteDocumental):
    def __init__(self, titulo: str, contenido: str) -> None:
        self.titulo = titulo
        self.contenido = contenido

    def obtener_contenido(self) -> str:
        return f"Artículo: {self.titulo}\n{self.contenido}"

    def exportar_a_json(self) -> dict:
        return {
            "tipo": "Articulo",
            "titulo": self.titulo,
            "contenido": self.contenido
        }
