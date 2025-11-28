from datetime import date
import os
import json

# Configuración de la API
API_TITLE = "TradeJournal API"
API_DESCRIPTION = "API para gestión de trades de trading"
API_VERSION = "1.0.0"

# Configuración CORS
# Base origins para desarrollo
_DEFAULT_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://localhost:8080",
]

# Permitir agregar origins adicionales desde variable de entorno (ej: producción)
# ALLOWED_ORIGINS="https://domain1.com,https://domain2.com"
_env_origins = os.getenv("ALLOWED_ORIGINS", "")
if _env_origins:
    additional_origins = [origin.strip() for origin in _env_origins.split(",") if origin.strip()]
    ALLOWED_ORIGINS = _DEFAULT_ORIGINS + additional_origins
else:
    # Si no hay env var, usar los defaults + el dominio de producción conocido
    ALLOWED_ORIGINS = _DEFAULT_ORIGINS + [
        "https://journal-23783252-2d978.web.app",
        "https://journal-23783252-2d978.firebaseapp.com",
    ]

# Configuración del servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Configuración de paginación por defecto
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000

def _load_firebase_config():
    """Carga configuración de Firebase desde archivo externo o variables de entorno.

    Orden de carga:
    1) Archivo JSON apuntado por FIREBASE_CONFIG_PATH
    2) Archivo JSON por defecto en API/firebase_config.json
    3) Variables de entorno FIREBASE_*
    """
    # 1) Ruta por variable de entorno
    path = os.getenv("FIREBASE_CONFIG_PATH")
    if path and os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # 2) Ruta por defecto junto a la API (no debe subirse a git)
    default_path = os.path.join(os.path.dirname(__file__), "firebase_config.json")
    if os.path.exists(default_path):
        try:
            with open(default_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # 3) Variables de entorno
    api_key = os.getenv("FIREBASE_API_KEY")
    if api_key:
        return {
            "apiKey": api_key,
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", ""),
            "projectId": os.getenv("FIREBASE_PROJECT_ID", ""),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", ""),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", ""),
            "appId": os.getenv("FIREBASE_APP_ID", ""),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "")
        }

    # Si no hay configuración disponible, devolver None para que el servicio entre en modo dev
    return None

# Configuración de Firebase
FIREBASE_CONFIG = _load_firebase_config()

# Colección de Firestore para trades
FIREBASE_COLLECTION = os.getenv("FIREBASE_COLLECTION", "trades")

# Base de datos Firestore (opcional, por defecto usa "(default)")
FIREBASE_DATABASE_ID = os.getenv("FIREBASE_DATABASE_ID", "journal-db")
