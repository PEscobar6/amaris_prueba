"""
Modelo de usuario del sistema
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base


class User(Base):
    """Modelo de usuario del sistema FPV"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    balance = Column(Float, default=500000.0, nullable=False)
    notification_preference = Column(String(10), default="email")  # "email" or "sms"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    subscriptions = relationship("Subscription", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    
    def has_sufficient_balance(self, amount: float) -> bool:
        """Verifica si el usuario tiene saldo suficiente"""
        return self.balance >= amount
    
    def deduct_balance(self, amount: float) -> bool:
        """Deduce el monto del saldo del usuario"""
        if self.has_sufficient_balance(amount):
            self.balance -= amount
            return True
        return False
    
    def add_balance(self, amount: float):
        """Añade monto al saldo del usuario"""
        self.balance += amount