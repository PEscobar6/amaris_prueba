"""
Router para gestión de usuarios
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from services.user_service import UserService
from schemas.user import UserResponse, NotificationPreferenceUpdate

router = APIRouter()


@router.get("/user/profile", response_model=UserResponse)
async def get_user_profile(db: Session = Depends(get_db)):
    """Obtener perfil del usuario por defecto"""
    user_service = UserService(db)
    user = user_service.get_default_user()
    
    return UserResponse.from_orm(user)


@router.put("/user/notification-preference", response_model=UserResponse)
async def update_notification_preference(
    preference_data: NotificationPreferenceUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar preferencia de notificación del usuario"""
    user_service = UserService(db)
    user = user_service.get_default_user()
    
    updated_user = user_service.update_notification_preference(
        user_id=user.id,
        preference=preference_data.notification_preference
    )
    
    return UserResponse.from_orm(updated_user)


@router.get("/user/balance")
async def get_user_balance(db: Session = Depends(get_db)):
    """Obtener saldo actual del usuario"""
    user_service = UserService(db)
    user = user_service.get_default_user()
    
    return {
        "balance": user.balance,
        "formatted_balance": f"COP ${user.balance:,.0f}",
        "currency": "COP"
    }