"""
Servicio para envío de notificaciones (email y SMS)
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import asyncio
import aiosmtplib

from core.config import settings


class NotificationService:
    """Servicio para envío de notificaciones"""
    
    async def send_email_notification(
        self, 
        to_email: str, 
        subject: str, 
        message: str,
        user_name: str = "Usuario"
    ) -> bool:
        """Enviar notificación por email"""
        try:
            if not settings.smtp_username or not settings.smtp_password:
                print(f"Email notification (simulated): {subject} to {to_email}")
                return True
            
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = settings.smtp_username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Cuerpo del mensaje
            body = f"""
            Hola {user_name},
            
            {message}
            
            Saludos,
            Equipo FPV Management System
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Enviar email
            await aiosmtplib.send(
                msg,
                hostname=settings.smtp_server,
                port=settings.smtp_port,
                start_tls=True,
                username=settings.smtp_username,
                password=settings.smtp_password,
            )
            
            return True
            
        except Exception as e:
            print(f"Error enviando email: {e}")
            return False
    
    async def send_sms_notification(
        self, 
        to_phone: str, 
        message: str
    ) -> bool:
        """Enviar notificación por SMS usando Twilio"""
        try:
            if not settings.twilio_account_sid or not settings.twilio_auth_token:
                print(f"SMS notification (simulated): {message} to {to_phone}")
                return True
            
            # Aquí se implementaría la integración con Twilio
            # from twilio.rest import Client
            # client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            # message = client.messages.create(
            #     body=message,
            #     from_=settings.twilio_phone_number,
            #     to=to_phone
            # )
            
            print(f"SMS notification (simulated): {message} to {to_phone}")
            return True
            
        except Exception as e:
            print(f"Error enviando SMS: {e}")
            return False
    
    async def send_subscription_notification(
        self,
        user_name: str,
        user_email: str,
        user_phone: str,
        fund_name: str,
        amount: float,
        notification_type: str = "email"
    ) -> bool:
        """Enviar notificación de suscripción exitosa"""
        
        subject = "Suscripción Exitosa - FPV Management System"
        message = f"""
        Su suscripción al fondo {fund_name} ha sido procesada exitosamente.
        
        Detalles:
        - Fondo: {fund_name}
        - Monto: COP ${amount:,.0f}
        - Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        
        Gracias por confiar en nosotros.
        """
        
        if notification_type == "email":
            return await self.send_email_notification(user_email, subject, message, user_name)
        elif notification_type == "sms":
            sms_message = f"Suscripción exitosa a {fund_name} por COP ${amount:,.0f}. Gracias por confiar en FPV System."
            return await self.send_sms_notification(user_phone, sms_message)
        
        return False
    
    async def send_cancellation_notification(
        self,
        user_name: str,
        user_email: str,
        user_phone: str,
        fund_name: str,
        amount: float,
        notification_type: str = "email"
    ) -> bool:
        """Enviar notificación de cancelación exitosa"""
        
        subject = "Cancelación Exitosa - FPV Management System"
        message = f"""
        Su cancelación del fondo {fund_name} ha sido procesada exitosamente.
        
        Detalles:
        - Fondo: {fund_name}
        - Monto devuelto: COP ${amount:,.0f}
        - Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
        
        El monto ha sido devuelto a su saldo disponible.
        """
        
        if notification_type == "email":
            return await self.send_email_notification(user_email, subject, message, user_name)
        elif notification_type == "sms":
            sms_message = f"Cancelación exitosa de {fund_name}. COP ${amount:,.0f} devuelto a su saldo. FPV System."
            return await self.send_sms_notification(user_phone, sms_message)
        
        return False


# Importar datetime al final para evitar conflictos
from datetime import datetime