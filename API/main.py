import os
import traceback
from fastapi import FastAPI, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Importar configuración
from config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    ALLOWED_ORIGINS, HOST, PORT
)

# Configurar el entorno
ENV = os.getenv('ENV', 'development')
print(f"Iniciando aplicación en modo: {ENV}")

# Inicializar Firebase Admin para autenticación
# Esto asegura que Firebase esté disponible para verificar tokens
from app.auth import get_firebase_auth
try:
    get_firebase_auth()
    print("✅ Firebase Admin inicializado para autenticación")
except Exception as e:
    print(f"⚠️  Advertencia: No se pudo inicializar Firebase Admin: {e}")
    print("   La autenticación requerirá credenciales válidas")

# Inicializar servicios
from app.services.trade_service import create_trade_service

# Crear instancia del servicio de trades
trade_service = create_trade_service(use_in_memory=(ENV == 'development'))

# Importar rutas después de inicializar los servicios
from app.routes import trades, emotions, confirmations, day_journal, export, auth
from app.auth import get_current_user

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Middleware para manejo global de errores
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """Middleware para capturar y loggear errores 500"""
    try:
        return await call_next(request)
    except Exception as e:
        # Loggear el error completo con traceback
        error_traceback = traceback.format_exc()
        print(f"❌ ERROR 500 en {request.method} {request.url.path}")
        print(f"   Error: {str(e)}")
        print(f"   Traceback:\n{error_traceback}")

        # Retornar respuesta de error al cliente
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Internal server error",
                "error": str(e) if ENV == 'development' else "An error occurred processing your request"
            }
        )

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(auth.router)
app.include_router(trades.router)
app.include_router(emotions.router)
app.include_router(confirmations.router)
app.include_router(day_journal.router)
app.include_router(export.router)

@app.get("/")
async def root():
    return {"message": f"{API_TITLE} is running", "version": API_VERSION}

@app.get("/echo")
async def echo():
    return {"message": "hola mundo"}

@app.get("/api/user")
async def get_user(user: dict = Depends(get_current_user)):
    """Obtener información del usuario autenticado"""
    return {"uid": user["uid"], "email": user["email"], "name": user["name"]}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=True
    )
