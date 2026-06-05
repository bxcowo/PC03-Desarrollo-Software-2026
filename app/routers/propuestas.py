from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, status
from sqlalchemy.orm import Session
from app.servicios.servicio_documental import ServicioDocumental
from app.dtos.propuesta_dtos import PropuestaCreate, SeccionCreate, ArticuloCreate, PropuestaResponse
from app.utils.token_management import get_current_ciudadano_id
from app.infraestructura.database import get_db

router = APIRouter(prefix="/propuestas", tags=["propuestas"])

@router.post("/", response_model=PropuestaResponse, status_code=status.HTTP_201_CREATED, summary="Crear estructura de propuesta")
def crear_propuesta(
    body: PropuestaCreate, 
    db: Session = Depends(get_db),
    ciudadano_id: str = Depends(get_current_ciudadano_id)
):
    servicio = ServicioDocumental(db)
    try:
        return servicio.crear_propuesta_inicial(body.iniciativa_id, int(ciudadano_id), body.titulo)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.post("/secciones", response_model=PropuestaResponse, summary="Agregar sección a la propuesta")
def agregar_seccion(
    body: SeccionCreate, 
    db: Session = Depends(get_db),
    ciudadano_id: str = Depends(get_current_ciudadano_id)
):
    servicio = ServicioDocumental(db)
    try:
        return servicio.agregar_seccion(body.iniciativa_id, int(ciudadano_id), body.titulo_seccion)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/articulos", response_model=PropuestaResponse, summary="Agregar artículo a una sección")
def agregar_articulo(
    body: ArticuloCreate, 
    db: Session = Depends(get_db),
    ciudadano_id: str = Depends(get_current_ciudadano_id)
):
    servicio = ServicioDocumental(db)
    try:
        return servicio.agregar_articulo_a_seccion(
            body.iniciativa_id, 
            int(ciudadano_id),
            body.titulo_seccion, 
            body.titulo_articulo, 
            body.contenido
        )
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{iniciativa_id}/adjuntar", response_model=PropuestaResponse, summary="Adjuntar documento externo (PDF/DOCX)")
async def adjuntar_documento(
    iniciativa_id: int, 
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    ciudadano_id: str = Depends(get_current_ciudadano_id)
):
    servicio = ServicioDocumental(db)
    contenido = await file.read()
    try:
        return servicio.adjuntar_recurso_externo(iniciativa_id, int(ciudadano_id), file.filename, contenido)
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
