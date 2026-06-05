from pydantic import BaseModel
from typing import List, Optional, Any

class PropuestaCreate(BaseModel):
    iniciativa_id: int
    titulo: str

class SeccionCreate(BaseModel):
    iniciativa_id: int
    titulo_seccion: str

class ArticuloCreate(BaseModel):
    iniciativa_id: int
    titulo_seccion: str
    titulo_articulo: str
    contenido: str

class PropuestaResponse(BaseModel):
    tipo: str
    iniciativa_id: Optional[int] = None
    titulo: str
    hijos: List[Any] = []
    contenido: Optional[str] = None
