# Sistema de Gestión FPV (Fondos Voluntarios de Pensión)

Este proyecto implementa un sistema completo para la gestión de Fondos Voluntarios de Pensión (FPV) y Fondos de Inversión Colectiva (FIC), desarrollado con **FastAPI** para el backend y **Next.js** con **shadcn/ui** para el frontend.

## 🚀 Características Principales

- **Suscripción a fondos**: Los usuarios pueden suscribirse a diferentes fondos FPV y FIC
- **Cancelación de suscripciones**: Posibilidad de cancelar suscripciones activas con devolución automática
- **Historial de transacciones**: Seguimiento completo de todas las operaciones realizadas
- **Notificaciones**: Sistema de notificaciones por email o SMS según preferencia del usuario
- **Interface intuitiva**: Dashboard moderno y fácil de usar
- **Validaciones de negocio**: Control de saldos y montos mínimos
- **Identificadores únicos**: Cada transacción genera un UUID único

## 📋 Reglas de Negocio

- Saldo inicial: **COP $500.000**
- Monto mínimo variable por fondo
- Devolución automática al cancelar suscripciones
- Validación de saldo suficiente antes de suscripciones
- Sistema de notificaciones configurable por usuario

## 🏗️ Arquitectura del Sistema

### Backend (FastAPI)
```
backend/
├── core/           # Configuración de la aplicación
├── database/       # Conexión y configuración de BD
├── models/         # Modelos SQLAlchemy
├── schemas/        # Schemas Pydantic
├── services/       # Lógica de negocio
├── routers/        # Endpoints REST API
├── main.py         # Punto de entrada de la aplicación
└── requirements.txt
```

### Frontend (Next.js + shadcn/ui)
```
frontend/
├── src/
│   ├── app/          # App Router de Next.js
│   ├── components/   # Componentes React
│   │   └── ui/       # Componentes shadcn/ui
│   ├── lib/          # Utilidades
│   ├── services/     # Servicios API
│   └── types/        # Definiciones TypeScript
├── package.json
└── tailwind.config.ts
```

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para base de datos
- **Pydantic**: Validación de datos
- **PostgreSQL**: Base de datos principal
- **Alembic**: Migraciones de base de datos
- **Uvicorn**: Servidor ASGI

### Frontend
- **Next.js 14**: Framework React con App Router
- **TypeScript**: Tipado estático
- **Tailwind CSS**: Framework de CSS utilitario
- **shadcn/ui**: Componentes UI modernos
- **Axios**: Cliente HTTP
- **React Hook Form**: Manejo de formularios

### DevOps
- **Docker**: Containerización
- **Docker Compose**: Orquestación de servicios

## 📊 Fondos Disponibles

| ID | Nombre | Monto Mínimo | Categoría |
|----|--------|--------------|-----------|
| 1 | FPV_EL CLIENTE_RECAUDADORA | COP $75.000 | FPV |
| 2 | FPV_EL CLIENTE_ECOPETROL | COP $125.000 | FPV |
| 3 | DEUDAPRIVADA | COP $50.000 | FIC |
| 4 | FDO-ACCIONES | COP $250.000 | FIC |
| 5 | FPV_EL CLIENTE_DINAMICA | COP $100.000 | FPV |

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Docker y Docker Compose instalados
- Node.js 18+ (para desarrollo local)
- Python 3.11+ (para desarrollo local)

### Ejecución con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd amaris_prueba
   ```

2. **Variables de entorno configuradas**
   ```bash
   # ✅ El archivo .env YA ESTÁ LISTO con todas las configuraciones
   # Ver ENV_SETUP.md para personalización opcional
   ```

3. **Ejecutar con Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentación API: http://localhost:8000/docs

### Ejecución en Desarrollo Local

#### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configurar variables de entorno en .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Endpoints

### Usuarios
- `GET /api/v1/user/profile` - Obtener perfil de usuario
- `GET /api/v1/user/balance` - Obtener saldo actual
- `PUT /api/v1/user/notification-preference` - Actualizar preferencias

### Fondos
- `GET /api/v1/funds` - Listar todos los fondos
- `GET /api/v1/funds/{id}` - Obtener detalles de un fondo
- `GET /api/v1/funds/{id}/eligibility` - Verificar elegibilidad
- `GET /api/v1/user/subscriptions` - Obtener suscripciones del usuario

### Transacciones
- `POST /api/v1/subscriptions` - Suscribirse a un fondo
- `POST /api/v1/cancellations` - Cancelar suscripción
- `GET /api/v1/transactions` - Obtener historial de transacciones
- `GET /api/v1/transactions/{id}` - Obtener detalles de transacción

## 🎯 Funcionalidades del Usuario

### Dashboard Principal
- Vista resumen con saldo disponible
- Fondos disponibles y suscritos
- Estadísticas de transacciones

### Gestión de Fondos
- Explorar fondos disponibles (FPV y FIC)
- Verificar elegibilidad para suscripción
- Suscribirse con validación de monto mínimo
- Ver fondos suscritos activos

### Historial de Transacciones
- Ver todas las transacciones realizadas
- Filtrar por tipo (suscripciones/cancelaciones)
- Detalles completos de cada operación
- Cancelar suscripciones activas

### Configuración
- Actualizar preferencias de notificación
- Ver información del perfil
- Gestionar configuración del sistema

## 🔐 Configuración de Notificaciones

### Email (SMTP)
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### SMS (Twilio)
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_phone_number
```

## 🧪 Testing

```bash
# Backend testing
cd backend
pytest

# Frontend testing
cd frontend
npm test
```

## 📝 Estructura de Base de Datos

### Tablas Principales
- **users**: Información de usuarios
- **funds**: Catálogo de fondos disponibles
- **subscriptions**: Suscripciones de usuarios a fondos
- **transactions**: Registro de todas las transacciones

## 🔧 Variables de Entorno

Todas las variables de entorno están centralizadas en el archivo `.env` en la raíz del proyecto.

### ✅ Configuración Lista
El archivo `.env` **ya está completamente configurado** y listo para usar:
- Ver archivo `ENV_SETUP.md` para opciones adicionales
- Las notificaciones (email/SMS) son opcionales y se habilitan descomentando variables

### Variables Principales
```env
# Base de datos
DATABASE_URL=postgresql://fpv_user:fpv_password@database:5432/fpv_system

# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000

# Configuración de la aplicación
INITIAL_BALANCE=500000
```

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema:
- Email: soporte@fpv-system.com
- Documentación API: http://localhost:8000/docs

## 📄 Licencia

Este proyecto es propiedad de **El Cliente** y está desarrollado para uso interno de la organización.

---

### Arquitectura Clean Code

El proyecto sigue principios de **Clean Architecture** y **Clean Code**:

- ✅ Separación clara de responsabilidades
- ✅ Inversión de dependencias
- ✅ Código autodocumentado
- ✅ Patrones de diseño apropiados
- ✅ Testing y validaciones
- ✅ Documentación completa

**Desarrollado con ❤️ usando las mejores prácticas de desarrollo moderno**