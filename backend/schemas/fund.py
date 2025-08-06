"""
Schemas de fondos para validación de API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class FundBase(BaseModel):
    """Schema base para fondo"""
    name: str = Field(..., min_length=3, max_length=100, description="Nombre del fondo")
    minimum_amount: float = Field(..., gt=0, description="Monto mínimo de vinculación")
    category: str = Field(..., pattern="^(FPV|FIC)$", description="Categoría del fondo")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del fondo")


class FundResponse(FundBase):
    """Schema de respuesta para fondo"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # subscriptions: Optional[List["SubscriptionResponse"]] = []
    # transactions: Optional[List["TransactionResponse"]] = []
    
    class Config:
        from_attributes = True


class FundSummary(BaseModel):
    """Schema resumido de fondo para listados"""
    id: int
    name: str
    minimum_amount: float
    category: str
    description: Optional[str] = None
    is_active: bool
    
    class Config:
        from_attributes = True