import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
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

# Inicializar servicios
from app.services.trade_service import create_trade_service

# Crear instancia del servicio de trades
trade_service = create_trade_service(use_in_memory=(ENV == 'development'))

# Importar rutas después de inicializar los servicios
from app.routes import trades, emotions, confirmations

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
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
app.include_router(trades.router)
app.include_router(emotions.router)
app.include_router(confirmations.router)

@app.get("/")
async def root():
    return {"message": f"{API_TITLE} is running", "version": API_VERSION}

@app.get("/echo")
async def echo():
    return {"message": "hola mundo"}

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=True
    )
