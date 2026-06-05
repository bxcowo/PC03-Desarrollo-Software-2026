from pydantic import BaseModel

class FirmaRequest(BaseModel):
    iniciativa_id: int


class FirmaResponse(BaseModel):
    firma_id: int
    iniciativa_id: int
    total_firmas: int
    estado: str
    sellado_hash: str | None = None


class IniciativaCreate(BaseModel):
    titulo: str
    descripcion: str
    dias_limite: int = 90


class IniciativaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    estado: str
    total_firmas: int
    firma_limite: int
    progreso_pct: float
    fecha_inicio: str
    fecha_limite: str
