"""
Modelo de fondo de inversión
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base


class Fund(Base):
    """Modelo de Fondo Voluntario de Pensión (FPV) o Fondo de Inversión Colectiva (FIC)"""
    
    __tablename__ = "funds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    minimum_amount = Column(Float, nullable=False)
    category = Column(String(10), nullable=False)  # "FPV" or "FIC"
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    subscriptions = relationship("Subscription", back_populates="fund")
    transactions = relationship("Transaction", back_populates="fund")
    
    def __repr__(self):
        return f"<Fund(id={self.id}, name='{self.name}', category='{self.category}')>"
    
    def is_subscription_allowed(self, amount: float) -> bool:
        """Verifica si el monto permite la suscripción al fondo"""
        return amount >= self.minimum_amount