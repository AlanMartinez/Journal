"""
Configuración global para tests unitarios
Incluye fixtures y configuración de pytest
"""
import os
import sys
import pytest
from unittest.mock import Mock, AsyncMock, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar variables de entorno para testing ANTES de importar cualquier módulo
os.environ['ENV'] = 'test'
os.environ['FIREBASE_COLLECTION'] = 'trades'
# Evitar intentar conectar a Firebase durante tests
os.environ['FIREBASE_CONFIG_PATH'] = ''

from app.services.in_memory.in_memory_service import InMemoryService
from app.services.day_journal_service import DayJournalService
from app.services.trade_service import TradeService
from app.services.emotion_service import EmotionService
from app.services.confirmation_service import ConfirmationService

# Importar todas las rutas
from app.routes import day_journal, trades, emotions, confirmations, export

@pytest.fixture
def mock_database_service():
    """Fixture para crear un servicio de base de datos mock"""
    return InMemoryService("test_collection")

@pytest.fixture
def day_journal_service_mock():
    """Fixture para crear un servicio de day_journal con mock"""
    mock_db = InMemoryService("trades_day_journal")
    return DayJournalService(database_service=mock_db)

@pytest.fixture
def trade_service_mock():
    """Fixture para crear un servicio de trades con mock"""
    mock_db = InMemoryService("trades")
    return TradeService(database_service=mock_db)

@pytest.fixture
def emotion_service_mock():
    """Fixture para crear un servicio de emotions con mock"""
    mock_db = InMemoryService("trades_emotions")
    return EmotionService(database_service=mock_db)

@pytest.fixture
def confirmation_service_mock():
    """Fixture para crear un servicio de confirmations con mock"""
    mock_db = InMemoryService("trades_confirmations")
    return ConfirmationService(database_service=mock_db)

@pytest.fixture
def app():
    """Fixture para crear una instancia de FastAPI para testing"""
    app = FastAPI(title="Test API")
    
    # Incluir todas las rutas
    app.include_router(day_journal.router)
    app.include_router(trades.router)
    app.include_router(emotions.router)
    app.include_router(confirmations.router)
    app.include_router(export.router)
    
    return app

@pytest.fixture
def client(app):
    """Fixture para crear un TestClient de FastAPI"""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_services():
    """Fixture que se ejecuta automáticamente antes de cada test"""
    # Asegurarse de que cada test empieza con un estado limpio
    yield
    # Cleanup si es necesario

