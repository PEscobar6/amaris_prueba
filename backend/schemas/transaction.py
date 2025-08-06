"""
Schemas de transacciones para validación de API
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    """Schema base para transacción"""
    fund_id: int = Field(..., gt=0, description="ID del fondo")
    amount: float = Field(..., gt=0, description="Monto de la transacción")
    transaction_type: str = Field(..., pattern="^(subscription|cancellation)$")
    description: Optional[str] = Field(None, max_length=500)


class TransactionCreate(BaseModel):
    """Schema para creación de transacción"""
    fund_id: int = Field(..., gt=0, description="ID del fondo")
    transaction_type: str = Field(..., pattern="^(subscription|cancellation)$")
    amount: float = Field(..., gt=0, description="Monto de la transacción")
    description: Optional[str] = None


class TransactionResponse(TransactionBase):
    """Schema de respuesta para transacción"""
    id: int
    transaction_id: str
    user_id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TransactionWithDetails(TransactionResponse):
    """Schema de transacción con detalles del fondo y usuario"""
    fund_name: str
    fund_category: str
    user_name: str
    user_email: str
    
    class Config:
        from_attributes = True


class TransactionHistoryFilter(BaseModel):
    """Schema para filtros de historial de transacciones"""
    transaction_type: Optional[str] = Field(None, pattern="^(subscription|cancellation)$")
    fund_id: Optional[int] = Field(None, gt=0)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)