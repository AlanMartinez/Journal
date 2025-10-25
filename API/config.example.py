# Configuración de ejemplo para la API
# Copia este archivo a config.py y ajusta según necesites

from datetime import date
import os

# Configuración de la API
API_TITLE = "TradeJournal API"
API_DESCRIPTION = "API para gestión de trades de trading"
API_VERSION = "1.0.0"

# Configuración CORS
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://localhost:3000",  # React dev server
    "http://localhost:8080",  # Vue CLI dev server
]

# Configuración del servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Configuración de paginación por defecto
DEFAULT_SKIP = 0
DEFAULT_LIMIT = 100
MAX_LIMIT = 1000

# Configuración de Firebase
FIREBASE_CONFIG = {
    "apiKey": os.getenv("FIREBASE_API_KEY", "your-api-key"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "your-project.firebaseapp.com"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID", "your-project-id"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "your-project.appspot.com"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "123456789"),
    "appId": os.getenv("FIREBASE_APP_ID", "your-app-id"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "https://your-project-default-rtdb.firebaseio.com")
}

# Colección de Firestore para trades
FIREBASE_COLLECTION = os.getenv("FIREBASE_COLLECTION", "trades")

# Base de datos Firestore (opcional, por defecto usa "(default)")
FIREBASE_DATABASE_ID = os.getenv("FIREBASE_DATABASE_ID", "journal-db")
