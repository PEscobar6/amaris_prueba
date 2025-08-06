"""
Servicio para gestión de transacciones
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from models.transaction import Transaction
from models.user import User
from models.fund import Fund
from models.subscription import Subscription
from schemas.transaction import TransactionCreate, TransactionResponse, TransactionWithDetails
from services.fund_service import FundService
from services.notification_service import NotificationService


class TransactionService:
    """Servicio para gestión de transacciones"""
    
    def __init__(self, db: Session):
        self.db = db
        self.fund_service = FundService(db)
        self.notification_service = NotificationService()
    
    async def create_subscription_transaction(
        self, 
        user: User, 
        fund_id: int, 
        amount: float,
        notification_type: str = "email"
    ) -> Transaction:
        """Crear transacción de suscripción a fondo"""
        
        # Obtener fondo
        fund = self.fund_service.get_fund_by_id(fund_id)
        
        # Validar elegibilidad
        self.fund_service.validate_subscription_eligibility(user, fund, amount)
        
        try:
            # Deducir saldo del usuario
            if not user.deduct_balance(amount):
                raise Exception("Error al deducir saldo")
            
            # Crear suscripción
            subscription = Subscription(
                user_id=user.id,
                fund_id=fund.id,
                amount=amount
            )
            self.db.add(subscription)
            
            # Crear transacción
            transaction = Transaction.create_subscription_transaction(
                user_id=user.id,
                fund_id=fund.id,
                amount=amount,
                description=f"Suscripción a {fund.name}"
            )
            self.db.add(transaction)
            
            # Guardar cambios
            self.db.commit()
            self.db.refresh(transaction)
            self.db.refresh(user)
            
            # Enviar notificación
            await self.notification_service.send_subscription_notification(
                user_name=user.name,
                user_email=user.email,
                user_phone=user.phone,
                fund_name=fund.name,
                amount=amount,
                notification_type=notification_type
            )
            
            return transaction
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    async def create_cancellation_transaction(
        self, 
        user: User, 
        subscription_id: int
    ) -> Transaction:
        """Crear transacción de cancelación de suscripción"""
        
        # Obtener suscripción
        subscription = self.fund_service.get_subscription_by_id(subscription_id, user.id)
        
        # Validar elegibilidad de cancelación
        self.fund_service.validate_cancellation_eligibility(subscription)
        
        try:
            # Obtener fondo
            fund = self.fund_service.get_fund_by_id(subscription.fund_id)
            
            # Devolver saldo al usuario
            user.add_balance(subscription.amount)
            
            # Cancelar suscripción
            subscription.unsubscribe()
            
            # Crear transacción
            transaction = Transaction.create_cancellation_transaction(
                user_id=user.id,
                fund_id=subscription.fund_id,
                amount=subscription.amount,
                description=f"Cancelación de suscripción a {fund.name}"
            )
            self.db.add(transaction)
            
            # Guardar cambios
            self.db.commit()
            self.db.refresh(transaction)
            self.db.refresh(user)
            
            # Enviar notificación
            await self.notification_service.send_cancellation_notification(
                user_name=user.name,
                user_email=user.email,
                user_phone=user.phone,
                fund_name=fund.name,
                amount=subscription.amount,
                notification_type=user.notification_preference
            )
            
            return transaction
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_user_transactions(
        self, 
        user_id: int, 
        limit: int = 50, 
        offset: int = 0,
        transaction_type: Optional[str] = None
    ) -> List[TransactionWithDetails]:
        """Obtener historial de transacciones del usuario"""
        
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if transaction_type:
            query = query.filter(Transaction.transaction_type == transaction_type)
        
        transactions = query.order_by(desc(Transaction.created_at)).offset(offset).limit(limit).all()
        
        # Convertir a schema con detalles
        transactions_with_details = []
        for transaction in transactions:
            fund = self.fund_service.get_fund_by_id(transaction.fund_id)
            user = self.db.query(User).filter(User.id == transaction.user_id).first()
            
            transaction_detail = TransactionWithDetails(
                id=transaction.id,
                transaction_id=transaction.transaction_id,
                user_id=transaction.user_id,
                fund_id=transaction.fund_id,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
                status=transaction.status,
                description=transaction.description,
                created_at=transaction.created_at,
                fund_name=fund.name if fund else "Fondo no encontrado",
                fund_category=fund.category if fund else "",
                user_name=user.name if user else "Usuario no encontrado",
                user_email=user.email if user else ""
            )
            transactions_with_details.append(transaction_detail)
        
        return transactions_with_details
    
    def get_transaction_by_id(self, transaction_id: str, user_id: int) -> Optional[Transaction]:
        """Obtener transacción por ID"""
        return self.db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id,
            Transaction.user_id == user_id
        ).first()