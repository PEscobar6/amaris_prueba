"""
Router para gestión de fondos
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from services.fund_service import FundService
from services.user_service import UserService
from schemas.fund import FundSummary, FundResponse
from schemas.subscription import SubscriptionResponse, SubscriptionWithDetails

router = APIRouter()


@router.get("/funds", response_model=List[FundSummary])
async def get_all_funds(db: Session = Depends(get_db)):
    """Obtener todos los fondos disponibles"""
    fund_service = FundService(db)
    return fund_service.get_all_funds()


@router.get("/funds/{fund_id}", response_model=FundResponse)
async def get_fund_by_id(fund_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un fondo específico"""
    fund_service = FundService(db)
    fund = fund_service.get_fund_by_id(fund_id)
    
    if not fund:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fondo no encontrado"
        )
    
    return FundResponse.from_orm(fund)


@router.get("/user/subscriptions", response_model=List[SubscriptionWithDetails])
async def get_user_subscriptions(db: Session = Depends(get_db)):
    """Obtener suscripciones activas del usuario por defecto"""
    user_service = UserService(db)
    fund_service = FundService(db)
    
    # Obtener usuario por defecto
    user = user_service.get_default_user()
    
    # Obtener suscripciones
    subscriptions = fund_service.get_user_subscriptions(user.id)
    
    # Convertir a schema con detalles
    subscriptions_with_details = []
    for subscription in subscriptions:
        fund = fund_service.get_fund_by_id(subscription.fund_id)
        subscription_detail = SubscriptionWithDetails(
            id=subscription.id,
            user_id=subscription.user_id,
            fund_id=subscription.fund_id,
            amount=subscription.amount,
            is_active=subscription.is_active,
            subscribed_at=subscription.subscribed_at,
            unsubscribed_at=subscription.unsubscribed_at,
            fund_name=fund.name if fund else "Fondo no encontrado",
            fund_category=fund.category if fund else "",
            fund_minimum_amount=fund.minimum_amount if fund else 0
        )
        subscriptions_with_details.append(subscription_detail)
    
    return subscriptions_with_details


@router.get("/funds/{fund_id}/eligibility")
async def check_subscription_eligibility(
    fund_id: int, 
    amount: float,
    db: Session = Depends(get_db)
):
    """Verificar elegibilidad para suscribirse a un fondo"""
    user_service = UserService(db)
    fund_service = FundService(db)
    
    # Obtener usuario y fondo
    user = user_service.get_default_user()
    fund = fund_service.get_fund_by_id(fund_id)
    
    try:
        fund_service.validate_subscription_eligibility(user, fund, amount)
        return {
            "eligible": True,
            "message": f"Puede suscribirse al fondo {fund.name}",
            "user_balance": user.balance,
            "required_amount": amount,
            "fund_minimum": fund.minimum_amount
        }
    except HTTPException as e:
        return {
            "eligible": False,
            "message": e.detail,
            "user_balance": user.balance,
            "required_amount": amount,
            "fund_minimum": fund.minimum_amount if fund else 0
        }