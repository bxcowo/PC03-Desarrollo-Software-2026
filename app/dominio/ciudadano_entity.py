from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional

@dataclass
class CiudadanoEntity:
    id: Optional[int]
    dni: str
    nombre: str
    email: str
    hashed_password: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
