"""
Modelo de suscripción de usuario a fondos
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from database.connection import Base


class Subscription(Base):
    """Modelo de suscripción de usuario a un fondo"""
    
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fund_id = Column(Integer, ForeignKey("funds.id"), nullable=False)
    amount = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    subscribed_at = Column(DateTime, default=datetime.utcnow)
    unsubscribed_at = Column(DateTime, nullable=True)
    
    # Relaciones
    user = relationship("User", back_populates="subscriptions")
    fund = relationship("Fund", back_populates="subscriptions")
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, fund_id={self.fund_id})>"
    
    def unsubscribe(self):
        """Cancela la suscripción al fondo"""
        self.is_active = False
        self.unsubscribed_at = datetime.utcnow()