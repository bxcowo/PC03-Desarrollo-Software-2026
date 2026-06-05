from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.servicios.servicio_firmas import ServicioFirmas
from app.infraestructura.database import get_db
from app.utils.token_management import get_current_ciudadano_id
from app.dtos.firm_dtos import FirmaRequest, FirmaResponse, IniciativaResponse

router = APIRouter(tags=["firmas"])

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
