# Configuración de Variables de Entorno

## 📋 Archivo .env

El proyecto utiliza un archivo `.env` en la raíz para configurar todas las variables de entorno. Copia el siguiente contenido y ajusta los valores según necesites:

```env
# ==============================================
# CONFIGURACIÓN DEL SISTEMA FPV
# ==============================================

# Base de datos
DATABASE_URL=postgresql://fpv_user:fpv_password@database:5432/fpv_system
POSTGRES_DB=fpv_system
POSTGRES_USER=fpv_user
POSTGRES_PASSWORD=fpv_password

# Configuración del Backend API
BACKEND_PORT=8000

# Configuración del Frontend
FRONTEND_PORT=3000
NEXT_PUBLIC_API_URL=http://localhost:8000

# Configuración de Email (SMTP) - OPCIONAL
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
# SMTP_USERNAME=tu_email@gmail.com
# SMTP_PASSWORD=tu_contraseña_de_aplicacion

# Configuración de SMS (Twilio) - OPCIONAL
# TWILIO_ACCOUNT_SID=tu_account_sid_de_twilio
# TWILIO_AUTH_TOKEN=tu_auth_token_de_twilio
# TWILIO_PHONE_NUMBER=tu_numero_de_twilio
SMS_API_URL=https://api.twilio.com/2010-04-01

# Configuración de la Aplicación
APP_NAME=FPV Management System
DEBUG=true
INITIAL_BALANCE=500000

# Para desarrollo local sin Docker (OPCIONAL)
LOCAL_DATABASE_URL=sqlite:///./database.db
```

## 🔧 Configuración Opcional

### Email (SMTP)
Para habilitar notificaciones por email, descomenta y configura:
- `SMTP_USERNAME`: Tu email de Gmail
- `SMTP_PASSWORD`: Contraseña de aplicación de Gmail

### SMS (Twilio)
Para habilitar notificaciones por SMS, descomenta y configura:
- `TWILIO_ACCOUNT_SID`: Account SID de Twilio
- `TWILIO_AUTH_TOKEN`: Auth Token de Twilio  
- `TWILIO_PHONE_NUMBER`: Número de teléfono de Twilio

## 🚀 Uso

1. **Crear el archivo .env**:
   ```bash
   # En la raíz del proyecto
   touch .env
   # Copia el contenido de arriba
   ```

2. **Ejecutar con Docker**:
   ```bash
   docker-compose up --build
   ```

El sistema funcionará con las configuraciones por defecto. Las notificaciones por email y SMS son opcionales.