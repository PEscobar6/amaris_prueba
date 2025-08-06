"""
Router para gestión de transacciones
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from database.connection import get_db
from services.transaction_service import TransactionService
from services.user_service import UserService
from services.fund_service import FundService
from schemas.transaction import TransactionResponse, TransactionWithDetails
from schemas.subscription import SubscriptionCreate, SubscriptionCancellation

router = APIRouter()


@router.post("/subscriptions", response_model=TransactionResponse)
async def subscribe_to_fund(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    """Suscribirse a un fondo"""
    user_service = UserService(db)
    transaction_service = TransactionService(db)
    
    # Obtener usuario por defecto
    user = user_service.get_default_user()
    
    try:
        # Crear transacción de suscripción
        transaction = await transaction_service.create_subscription_transaction(
            user=user,
            fund_id=subscription_data.fund_id,
            amount=subscription_data.amount,
            notification_type=subscription_data.notification_type or user.notification_preference
        )
        
        return TransactionResponse.from_orm(transaction)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/cancellations", response_model=TransactionResponse)
async def cancel_subscription(
    cancellation_data: SubscriptionCancellation,
    db: Session = Depends(get_db)
):
    """Cancelar suscripción a un fondo"""
    user_service = UserService(db)
    transaction_service = TransactionService(db)
    
    # Obtener usuario por defecto
    user = user_service.get_default_user()
    
    try:
        # Crear transacción de cancelación
        transaction = await transaction_service.create_cancellation_transaction(
            user=user,
            subscription_id=cancellation_data.subscription_id
        )
        
        return TransactionResponse.from_orm(transaction)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/transactions", response_model=List[TransactionWithDetails])
async def get_transaction_history(
    limit: int = 50,
    offset: int = 0,
    transaction_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtener historial de transacciones del usuario"""
    user_service = UserService(db)
    transaction_service = TransactionService(db)
    
    # Obtener usuario por defecto
    user = user_service.get_default_user()
    
    # Validar transaction_type si se proporciona
    if transaction_type and transaction_type not in ["subscription", "cancellation"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de transacción inválido. Use 'subscription' o 'cancellation'"
        )
    
    # Obtener transacciones
    transactions = transaction_service.get_user_transactions(
        user_id=user.id,
        limit=min(limit, 100),  # Máximo 100 transacciones
        offset=offset,
        transaction_type=transaction_type
    )
    
    return transactions


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction_by_id(
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """Obtener detalles de una transacción específica"""
    user_service = UserService(db)
    transaction_service = TransactionService(db)
    
    # Obtener usuario por defecto
    user = user_service.get_default_user()
    
    # Obtener transacción
    transaction = transaction_service.get_transaction_by_id(transaction_id, user.id)
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transacción no encontrada"
        )
    
    return TransactionResponse.from_orm(transaction)