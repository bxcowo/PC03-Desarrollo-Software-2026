from dataclasses import dataclass
from typing import Optional

@dataclass
class FirmaEntity:
    id: Optional[int]
    ciudadano_id: int
    iniciativa_id: int
    es_valida: bool = True
