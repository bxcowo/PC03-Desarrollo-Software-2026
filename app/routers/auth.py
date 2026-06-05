from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dtos.auth_dtos import LoginRequest, RegistroRequest, TokenResponse
from app.infraestructura.database import get_db
from app.servicios.servicio_auth import ServicioAuth

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/registro",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo ciudadano",
)
def registro(body: RegistroRequest, db: Session = Depends(get_db)):
    servicio = ServicioAuth(db)
    try:
        return servicio.registrar_ciudadano(body)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    servicio = ServicioAuth(db)
    try:
        return servicio.login(body)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
