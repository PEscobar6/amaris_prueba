"""
Modelo de transacciones del sistema
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database.connection import Base


class Transaction(Base):
    """Modelo de transacciones (aperturas y cancelaciones)"""
    
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=False)
    transaction_type = Column(String(20), nullable=False)  # "subscription" or "cancellation"
    amount = Column(Float, nullable=False)
    status = Column(String(20), default="completed")  # "completed", "pending", "failed"
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="transactions")
    fund = relationship("Fund", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type='{self.transaction_type}', amount={self.amount})>"
    
    @classmethod
    def create_subscription_transaction(cls, user_id: int, fund_id: int, amount: float, description: str = None):
        """Crea una transacción de suscripción"""
        return cls(
            user_id=user_id,
            fund_id=fund_id,
            transaction_type="subscription",
            amount=amount,
            description=description or "Suscripción a fondo"
        )
    
    @classmethod
    def create_cancellation_transaction(cls, user_id: int, fund_id: int, amount: float, description: str = None):
        """Crea una transacción de cancelación"""
        return cls(
            user_id=user_id,
            fund_id=fund_id,
            transaction_type="cancellation",
            amount=amount,
            description=description or "Cancelación de suscripción a fondo"
        )