"""
Servicio para gestión de usuarios
"""

from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models.user import User
from schemas.user import UserCreate, UserResponse
from core.config import settings


class UserService:
    """Servicio para gestión de usuarios"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_default_user(self) -> User:
        """Obtener el usuario por defecto del sistema"""
        user = self.db.query(User).filter(User.email == "user@fpv.com").first()
        
        if not user:
            # Crear usuario por defecto si no existe
            user = User(
                name="Usuario FPV",
                email="user@fpv.com",
                phone="+573001234567",
                balance=settings.initial_balance,
                notification_preference="email"
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return self.db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(
            User.email == email,
            User.is_active == True
        ).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Crear nuevo usuario"""
        
        # Verificar que el email no esté en uso
        existing_user = self.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear usuario
        user = User(
            name=user_data.name,
            email=user_data.email,
            phone=user_data.phone,
            balance=settings.initial_balance,
            notification_preference=user_data.notification_preference
        )
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_notification_preference(self, user_id: int, preference: str) -> User:
        """Actualizar preferencia de notificación del usuario"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        if preference not in ["email", "sms"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Preferencia de notificación inválida"
            )
        
        user.notification_preference = preference
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_user_info(self, user_id: int, name: str = None, phone: str = None) -> User:
        """Actualizar información del usuario"""
        user = self.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        if name:
            user.name = name
        if phone:
            user.phone = phone
        
        self.db.commit()
        self.db.refresh(user)
        
        return user