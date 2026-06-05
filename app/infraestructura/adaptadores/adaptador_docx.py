from app.dominio.interfaces.documento_normativo import IDocumentoNormativo
from app.dominio.recurso_extraido import RecursoExtraido

class AdaptadorDOCX(IDocumentoNormativo):
    def __init__(self, binario: bytes, nombre_archivo: str) -> None:
        self._binario = binario
        self._nombre = nombre_archivo

    def extraer_informacion(self) -> RecursoExtraido:
        # Simulación de extracción
        return RecursoExtraido(
            texto=f"[Contenido extraído del DOCX {self._nombre}]",
            formato="DOCX",
            nombre_original=self._nombre,
            tamano_bytes=len(self._binario)
        )
