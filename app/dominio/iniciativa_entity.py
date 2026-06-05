from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.dominio.enums.estado_iniciativa import EstadoIniciativaEnum

@dataclass
class IniciativaEntity:
    id: Optional[int]
    titulo: str
    descripcion: str
    estado: EstadoIniciativaEnum
    total_firmas: int
    fecha_inicio: datetime
    fecha_limite: datetime
    sellado_hash: Optional[str] = None
