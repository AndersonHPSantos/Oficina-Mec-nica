from fastapi import FastAPI, HTTPException

from app.core.config import settings
from app.infrastructure.database import verificar_conexao

from app.api.routes.clientes import router as clientes_router


app = FastAPI(
    title=settings.APP_NAME,
    description="API para a gestão de uma oficina mecanica.",
    version="0.1.0"
)

@app.get("/health", tags=["Monitoramento"])
def health_check():
    return {
        "status": "ok",
        "application": settings.APP_NAME
    }

@app.get("/health/database", tags=["Monitoramento"])
def database_health_check():
    try:
        verificar_conexao()
        return {"status": "ok", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=504,
            detail="Banco de dados indisponível"
        )
app.include_router(clientes_router)