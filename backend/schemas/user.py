"""
Schemas de usuario para validación de API
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    """Schema base para usuario"""
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    phone: str = Field(..., min_length=10, max_length=20, description="Teléfono del usuario")
    notification_preference: str = Field(default="email", pattern="^(email|sms)$")


class UserCreate(UserBase):
    """Schema para creación de usuario"""
    pass


class UserResponse(UserBase):
    """Schema de respuesta para usuario"""
    id: int
    balance: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # subscriptions: Optional[List["SubscriptionResponse"]] = []
    # transactions: Optional[List["TransactionResponse"]] = []
    
    class Config:
        from_attributes = True


class UserBalanceUpdate(BaseModel):
    """Schema para actualización de saldo"""
    amount: float = Field(..., gt=0, description="Monto a añadir o deducir")
    operation: str = Field(..., pattern="^(add|deduct)$", description="Tipo de operación")


class NotificationPreferenceUpdate(BaseModel):
    """Schema para actualización de preferencia de notificación"""
    notification_preference: str = Field(..., pattern="^(email|sms)$")