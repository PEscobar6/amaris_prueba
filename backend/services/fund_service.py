"""
Servicio para gestión de fondos de inversión
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.fund import Fund
from models.subscription import Subscription
from models.user import User
from schemas.fund import FundResponse, FundSummary
from schemas.subscription import SubscriptionCreate, SubscriptionResponse


class FundService:
    """Servicio para gestión de fondos"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_funds(self) -> List[FundSummary]:
        """Obtener todos los fondos disponibles"""
        funds = self.db.query(Fund).filter(Fund.is_active == True).all()
        return [FundSummary.from_orm(fund) for fund in funds]
    
    def get_fund_by_id(self, fund_id: int) -> Optional[Fund]:
        """Obtener fondo por ID"""
        return self.db.query(Fund).filter(
            Fund.id == fund_id, 
            Fund.is_active == True
        ).first()
    
    def validate_subscription_eligibility(self, user: User, fund: Fund, amount: float) -> None:
        """Validar si el usuario puede suscribirse al fondo"""
        
        # Verificar si el fondo existe y está activo
        if not fund:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fondo no encontrado"
            )
        
        # Verificar monto mínimo
        if amount < fund.minimum_amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El monto mínimo para {fund.name} es COP ${fund.minimum_amount:,.0f}"
            )
        
        # Verificar saldo suficiente
        if not user.has_sufficient_balance(amount):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No tiene saldo disponible para vincularse al fondo {fund.name}"
            )
        
        # Verificar si ya está suscrito al fondo
        existing_subscription = self.db.query(Subscription).filter(
            Subscription.user_id == user.id,
            Subscription.fund_id == fund.id,
            Subscription.is_active == True
        ).first()
        
        if existing_subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya está suscrito al fondo {fund.name}"
            )
    
    def get_user_subscriptions(self, user_id: int) -> List[Subscription]:
        """Obtener suscripciones activas del usuario"""
        return self.db.query(Subscription).filter(
            Subscription.user_id == user_id,
            Subscription.is_active == True
        ).all()
    
    def get_subscription_by_id(self, subscription_id: int, user_id: int) -> Optional[Subscription]:
        """Obtener suscripción por ID y usuario"""
        return self.db.query(Subscription).filter(
            Subscription.id == subscription_id,
            Subscription.user_id == user_id,
            Subscription.is_active == True
        ).first()
    
    def validate_cancellation_eligibility(self, subscription: Subscription) -> None:
        """Validar si se puede cancelar la suscripción"""
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Suscripción no encontrada"
            )
        
        if not subscription.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La suscripción ya está cancelada"
            )