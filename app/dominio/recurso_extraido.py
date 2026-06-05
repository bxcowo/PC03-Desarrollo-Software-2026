from dataclasses import dataclass

@dataclass(frozen=True)
class RecursoExtraido:
    """Value Object para representar el contenido y metadatos extraídos de un archivo."""
    texto: str
    formato: str
    nombre_original: str
    tamano_bytes: int
