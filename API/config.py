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
    "apiKey": "AIzaSyCpJyweEx7srvyUKXh5c6_MRWkrl5JdH-A",
    "authDomain": "tradejournal-9075d.firebaseapp.com",
    "projectId": "tradejournal-9075d",
    "storageBucket": "tradejournal-9075d.firebasestorage.app",
    "messagingSenderId": "242963148439",
    "appId": "1:242963148439:web:422291118ed2ce665083d2",
    "databaseURL": "https://tradejournal-9075d-default-rtdb.firebaseio.com"
}

# Colección de Firestore para trades
FIREBASE_COLLECTION = os.getenv("FIREBASE_COLLECTION", "trades")

# Base de datos Firestore (opcional, por defecto usa "(default)")
FIREBASE_DATABASE_ID = os.getenv("FIREBASE_DATABASE_ID", "journal-db")
