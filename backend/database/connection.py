"""
Configuración de la base de datos y sesiones
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
import asyncio

from core.config import settings

# Configuración de la base de datos
if settings.database_url.startswith("sqlite"):
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Generador de sesiones de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Inicializar la base de datos y crear las tablas"""
    from models import fund, user, transaction, subscription
    
    Base.metadata.create_all(bind=engine)
    
    # Crear fondos por defecto si no existen
    db = SessionLocal()
    try:
        await create_default_funds(db)
        await create_default_user(db)
    finally:
        db.close()


async def create_default_funds(db):
    """Crear fondos por defecto"""
    from models.fund import Fund
    
    default_funds = [
        {
            "id": 1,
            "name": "FPV_EL CLIENTE_RECAUDADORA",
            "minimum_amount": 75000.0,
            "category": "FPV"
        },
        {
            "id": 2,
            "name": "FPV_EL CLIENTE_ECOPETROL",
            "minimum_amount": 125000.0,
            "category": "FPV"
        },
        {
            "id": 3,
            "name": "DEUDAPRIVADA",
            "minimum_amount": 50000.0,
            "category": "FIC"
        },
        {
            "id": 4,
            "name": "FDO-ACCIONES",
            "minimum_amount": 250000.0,
            "category": "FIC"
        },
        {
            "id": 5,
            "name": "FPV_EL CLIENTE_DINAMICA",
            "minimum_amount": 100000.0,
            "category": "FPV"
        }
    ]
    
    for fund_data in default_funds:
        existing_fund = db.query(Fund).filter(Fund.id == fund_data["id"]).first()
        if not existing_fund:
            fund = Fund(**fund_data)
            db.add(fund)
    
    db.commit()


async def create_default_user(db):
    """Crear usuario por defecto"""
    from models.user import User
    
    existing_user = db.query(User).filter(User.email == "user@fpv.com").first()
    if not existing_user:
        user = User(
            name="Usuario FPV",
            email="user@fpv.com",
            phone="+573001234567",
            balance=settings.initial_balance
        )
        db.add(user)
        db.commit()