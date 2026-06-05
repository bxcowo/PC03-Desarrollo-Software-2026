from fastapi import FastAPI

from app.routers import auth, firmas, propuestas

app = FastAPI(
    title="Voz del Ciudadano",
    description=(
        "Plataforma de registro de firmas digitales para iniciativas ciudadanas. "
        "HU-01: Registro de Firma Digital. "
        "HU-02: Construcción de la Propuesta Normativa."
    ),
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(firmas.router)
app.include_router(propuestas.router)

@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "Voz del Ciudadano"}
