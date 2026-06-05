from sqlalchemy.orm import Session
from app.dominio.ciudadano_entity import CiudadanoEntity
from app.infraestructura.repositorios.repositorio_ciudadanos import RepositorioCiudadanos
from app.utils.token_management import create_token, hash_password
from app.dtos.auth_dtos import LoginRequest, RegistroRequest, TokenResponse

class ServicioAuth:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._repo = RepositorioCiudadanos(db)

    def registrar_ciudadano(self, body: RegistroRequest) -> TokenResponse:
        existing = self._repo.obtener_por_dni_o_email(body.dni, body.email)
        if existing:
            raise ValueError("Ya existe un ciudadano con ese DNI o email.")

        nuevo_ciudadano = CiudadanoEntity(
            id=None,
            dni=body.dni,
            nombre=body.nombre,
            email=body.email,
            hashed_password=hash_password(body.password)
        )

        ciudadano_guardado = self._repo.guardar(nuevo_ciudadano)
        self._db.commit()

        token = create_token(str(ciudadano_guardado.id), ciudadano_guardado.email)
        return TokenResponse(access_token=token, ciudadano_id=str(ciudadano_guardado.id))

    def login(self, body: LoginRequest) -> TokenResponse:
        ciudadano = self._repo.obtener_por_email(body.email)

        if ciudadano is None or ciudadano.hashed_password != hash_password(body.password):
            raise ValueError("Credenciales incorrectas.")

        token = create_token(str(ciudadano.id), ciudadano.email)
        return TokenResponse(access_token=token, ciudadano_id=str(ciudadano.id))
