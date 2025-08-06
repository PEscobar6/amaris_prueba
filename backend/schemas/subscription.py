"""
Schemas de suscripciones para validación de API
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SubscriptionBase(BaseModel):
    """Schema base para suscripción"""
    fund_id: int = Field(..., gt=0, description="ID del fondo")
    amount: float = Field(..., gt=0, description="Monto de la suscripción")


class SubscriptionCreate(SubscriptionBase):
    """Schema para creación de suscripción"""
    notification_type: Optional[str] = Field(default="email", pattern="^(email|sms)$")


class SubscriptionResponse(SubscriptionBase):
    """Schema de respuesta para suscripción"""
    id: int
    user_id: int
    is_active: bool
    subscribed_at: datetime
    unsubscribed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SubscriptionWithDetails(SubscriptionResponse):
    """Schema de suscripción con detalles del fondo"""
    fund_name: str
    fund_category: str
    fund_minimum_amount: float
    
    class Config:
        from_attributes = True


class SubscriptionCancellation(BaseModel):
    """Schema para cancelación de suscripción"""
    subscription_id: int = Field(..., gt=0, description="ID de la suscripción a cancelar")