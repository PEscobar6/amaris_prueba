"""
Configuración de la aplicación usando Pydantic Settings
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Database
    database_url: str = Field(default="sqlite:///./database.db", env="DATABASE_URL")
    
    # Email configuration
    smtp_server: str = Field(default="smtp.gmail.com", env="SMTP_SERVER")
    smtp_port: int = Field(default=587, env="SMTP_PORT")
    smtp_username: Optional[str] = Field(default=None, env="SMTP_USERNAME")
    smtp_password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    
    # SMS configuration (Twilio)
    twilio_account_sid: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = Field(default=None, env="TWILIO_PHONE_NUMBER")
    
    # App configuration
    app_name: str = Field(default="FPV Management System", env="APP_NAME")
    debug: bool = Field(default=True, env="DEBUG")
    initial_balance: float = Field(default=500000.0, env="INITIAL_BALANCE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()