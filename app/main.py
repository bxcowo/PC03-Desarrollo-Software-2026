from fastapi import FastAPI

from app.routers import auth, firmas

app = FastAPI(
    title="Voz del Ciudadano",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(firmas.router)

@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "service": "Voz del Ciudadano"}
