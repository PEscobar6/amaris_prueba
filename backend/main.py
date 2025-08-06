"""
Sistema de Gestión de Fondos Voluntarios de Pensión (FPV) y Fondos de Inversión Colectiva (FIC)
Desarrollado con FastAPI siguiendo principios de Clean Code
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database.connection import init_db
from routers import funds, transactions, users
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="FPV Management System",
    description="Sistema para gestión de Fondos Voluntarios de Pensión e Inversión Colectiva",
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(funds.router, prefix="/api/v1", tags=["funds"])
app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])


@app.get("/")
async def root():
    """Endpoint raíz del API"""
    return {
        "message": "FPV Management System API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificar la salud del servicio"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)