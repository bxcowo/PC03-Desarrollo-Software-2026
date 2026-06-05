from pydantic import BaseModel, EmailStr

class RegistroRequest(BaseModel):
    dni: str
    nombre: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    ciudadano_id: str
