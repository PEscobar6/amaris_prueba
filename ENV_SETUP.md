# 🔧 Configuración de Variables de Entorno - Sistema FPV

## ✅ Archivo .env Configurado

El archivo `.env` ya está configurado con todas las variables necesarias para el sistema FPV.

## 🚀 Configuración Básica (Ya Lista)

Las siguientes variables están **ya configuradas** y funcionan por defecto:

### Base de Datos:
- ✅ PostgreSQL configurado para Docker
- ✅ Credenciales: `fpv_user` / `fpv_password`
- ✅ Base de datos: `fpv_system`

### Aplicación:
- ✅ Saldo inicial: **COP $500.000**
- ✅ Puerto backend: **8000**
- ✅ Puerto frontend: **3000**
- ✅ Conexión API configurada

### Fondos Pre-configurados:
1. **FPV_EL CLIENTE_RECAUDADORA** - COP $75.000 (FPV)
2. **FPV_EL CLIENTE_ECOPETROL** - COP $125.000 (FPV)
3. **DEUDAPRIVADA** - COP $50.000 (FIC)
4. **FDO-ACCIONES** - COP $250.000 (FIC)
5. **FPV_EL CLIENTE_DINAMICA** - COP $100.000 (FPV)

## 📧 Configuración Opcional - Notificaciones por Email

Para habilitar notificaciones por email, **descomenta y configura** estas líneas en el `.env`:

```env
SMTP_USERNAME=tu_email@gmail.com
SMTP_PASSWORD=tu_contraseña_de_aplicacion
```

### Pasos para Gmail:
1. Ir a Google Account → Security → 2-Step Verification
2. Generar "App Password"
3. Usar esa contraseña en `SMTP_PASSWORD`

## 📱 Configuración Opcional - Notificaciones por SMS

Para habilitar notificaciones por SMS, **descomenta y configura** estas líneas en el `.env`:

```env
TWILIO_ACCOUNT_SID=tu_account_sid_de_twilio
TWILIO_AUTH_TOKEN=tu_auth_token_de_twilio
TWILIO_PHONE_NUMBER=+1234567890
```

### Pasos para Twilio:
1. Crear cuenta en https://www.twilio.com
2. Obtener Account SID y Auth Token del dashboard
3. Comprar un número de teléfono en Twilio

## 🚀 Ejecutar la Aplicación

```bash
# Simplemente ejecutar (todo está configurado)
docker-compose up --build
```

## 🌐 URLs de Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

## ⚙️ Variables Importantes

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `INITIAL_BALANCE` | 500000 | Saldo inicial en pesos colombianos |
| `DATABASE_URL` | postgresql://... | Conexión a PostgreSQL |
| `NEXT_PUBLIC_API_URL` | http://localhost:8000 | URL del backend |
| `DEBUG` | true | Modo desarrollo |

## 🛠️ Personalización

Si quieres cambiar alguna configuración, simplemente edita el archivo `.env`:

- **Cambiar saldo inicial**: Modifica `INITIAL_BALANCE`
- **Cambiar puertos**: Modifica `BACKEND_PORT` y `FRONTEND_PORT`
- **Modo producción**: Cambia `DEBUG=false`

## ✅ Estado del Sistema

- 🟢 **Base de datos**: Configurada (PostgreSQL)
- 🟢 **API Backend**: Configurada (FastAPI)
- 🟢 **Frontend**: Configurado (Next.js)
- 🟢 **Fondos**: 5 fondos precargados
- 🟢 **Usuario por defecto**: Configurado
- 🟡 **Notificaciones**: Opcionales (email/SMS)

## 🎯 Próximos Pasos

1. **Ejecutar**: `docker-compose up --build`
2. **Probar**: Ir a http://localhost:3000
3. **Opcional**: Configurar notificaciones si las necesitas

¡El sistema está **100% listo** para funcionar! 🚀