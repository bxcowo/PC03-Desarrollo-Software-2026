from pydantic import BaseModel

class FirmaRequest(BaseModel):
    iniciativa_id: str


class FirmaResponse(BaseModel):
    firma_id: str
    iniciativa_id: str
    total_firmas: int
    estado: str
    sellado_hash: str | None = None


class IniciativaResponse(BaseModel):
    id: str
    titulo: str
    descripcion: str
    estado: str
    total_firmas: int
    firma_limite: int
    progreso_pct: float
    fecha_inicio: str
    fecha_limite: str
