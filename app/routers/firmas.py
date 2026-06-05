from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.servicios.servicio_firmas import ServicioFirmas
from app.infraestructura.database import get_db
from app.utils.token_management import get_current_ciudadano_id
from app.dtos.firm_dtos import FirmaRequest, FirmaResponse, IniciativaResponse

from app.dtos.firm_dtos import FirmaRequest, FirmaResponse, IniciativaResponse, IniciativaCreate
from app.infraestructura.database.models.iniciativa import Iniciativa
from app.dominio.enums.estado_iniciativa import EstadoIniciativaEnum
from datetime import datetime, timedelta, UTC

router = APIRouter(tags=["firmas"])

@router.post(
    "/iniciativas/",
    response_model=IniciativaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva iniciativa legislativa",
)
def crear_iniciativa(
    body: IniciativaCreate,
    db: Session = Depends(get_db),
    ciudadano_id: str = Depends(get_current_ciudadano_id),
):
    nueva_iniciativa = Iniciativa(
        titulo=body.titulo,
        descripcion=body.descripcion,
        creador_id=int(ciudadano_id),
        fecha_limite=datetime.now(UTC) + timedelta(days=body.dias_limite),
        estado=EstadoIniciativaEnum.ACTIVA,
        total_firmas=0
    )
    db.add(nueva_iniciativa)
    db.commit()
    db.refresh(nueva_iniciativa)
    
    # Adaptación manual al DTO de respuesta para simplificar
    return {
        "id": nueva_iniciativa.id,
        "titulo": nueva_iniciativa.titulo,
        "descripcion": nueva_iniciativa.descripcion,
        "estado": nueva_iniciativa.estado.value,
        "total_firmas": nueva_iniciativa.total_firmas,
        "firma_limite": 25000, # Constante según README
        "progreso_pct": 0,
        "fecha_inicio": nueva_iniciativa.fecha_inicio.isoformat(),
        "fecha_limite": nueva_iniciativa.fecha_limite.isoformat()
    }


@router.get(
    "/iniciativas/",
    response_model=list[IniciativaResponse],
    summary="Listar iniciativas activas",
)
def listar_iniciativas(db: Session = Depends(get_db)):
    servicio = ServicioFirmas(db)
    return servicio.listar_iniciativas_activas()


@router.post(
    "/firmas/",
    response_model=FirmaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar firma digital",
)
def registrar_firma(
    body: FirmaRequest,
    db: Session = Depends(get_db),
    ciudadano_id: str = Depends(get_current_ciudadano_id),
):
    servicio = ServicioFirmas(db)
    try:
        result = servicio.registrar_firma(
            ciudadano_id=ciudadano_id,
            iniciativa_id=body.iniciativa_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    return FirmaResponse(**result)
