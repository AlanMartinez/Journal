from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime
from ..database.base_data_service import BaseDataService
from .mocks.trade_mocks import TRADE_MOCK_DATA
from .mocks.confirmation_mocks import CONFIRMATION_MOCK_DATA
from .mocks.emotion_mocks import EMOTION_MOCK_DATA

class InMemoryService(BaseDataService):
    """Implementación en memoria de BaseDataService para desarrollo local"""
    
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.data: Dict[str, Dict[str, Any]] = {}
        self._initialize_mock_data()

    def _initialize_mock_data(self):
        """Inicializar con datos de ejemplo"""
        if self.collection_name == "trades":
            self.data = TRADE_MOCK_DATA.copy()
        elif self.collection_name == "confirmations":
            self.data = CONFIRMATION_MOCK_DATA.copy()
        elif self.collection_name == "emotions":
            self.data = EMOTION_MOCK_DATA.copy()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener todos los elementos"""
        return list(self.data.values())[skip:skip+limit]

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """Obtener un elemento por ID"""
        return self.data.get(id)

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo elemento"""
        new_id = str(uuid.uuid4())
        data['id'] = new_id
        data['created_at'] = datetime.utcnow().isoformat()
        self.data[new_id] = data
        return data

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar un elemento existente"""
        if id not in self.data:
            return None
        self.data[id].update(data)
        return self.data[id]

    async def delete(self, id: str) -> bool:
        """Eliminar un elemento"""
        if id in self.data:
            del self.data[id]
            return True
        return False

    async def get_count(self) -> int:
        """Obtener el conteo total de elementos"""
        return len(self.data)
