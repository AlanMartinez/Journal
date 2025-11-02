from typing import List, Dict, Optional, Any
import uuid
from datetime import datetime, date
from ..database.base_data_service import BaseDataService
from .mocks.trade_mocks import TRADE_MOCK_DATA
from .mocks.confirmation_mocks import CONFIRMATION_MOCK_DATA
from .mocks.emotion_mocks import EMOTION_MOCK_DATA
from .mocks.day_journal_mocks import DAY_JOURNAL_MOCK_DATA

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
        elif self.collection_name == "trades_day_journal" or self.collection_name.endswith("_day_journal"):
            self.data = DAY_JOURNAL_MOCK_DATA.copy()

    async def get_all(self, skip: int = 0, limit: int = 100, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener todos los elementos"""
        items = list(self.data.values())
        # Filtrar por user_id si se proporciona
        if user_id:
            items = [item for item in items if item.get('user_id') == user_id]
        return items[skip:skip+limit]

    async def get_by_id(self, id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Obtener un elemento por ID"""
        item = self.data.get(id)
        # Verificar que el elemento pertenece al usuario si se proporciona user_id
        if item and user_id and item.get('user_id') != user_id:
            return None
        return item

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo elemento"""
        new_id = str(uuid.uuid4())
        data['id'] = new_id
        data['created_at'] = datetime.utcnow().isoformat()
        self.data[new_id] = data
        return data

    async def update(self, id: str, data: Dict[str, Any], user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Actualizar un elemento existente"""
        if id not in self.data:
            return None
        # Verificar que el elemento pertenece al usuario si se proporciona user_id
        if user_id and self.data[id].get('user_id') != user_id:
            return None
        self.data[id].update(data)
        return self.data[id]

    async def delete(self, id: str, user_id: Optional[str] = None) -> bool:
        """Eliminar un elemento"""
        if id not in self.data:
            return False
        # Verificar que el elemento pertenece al usuario si se proporciona user_id
        if user_id and self.data[id].get('user_id') != user_id:
            return False
        del self.data[id]
        return True

    async def get_count(self, user_id: Optional[str] = None) -> int:
        """Obtener el conteo total de elementos"""
        if user_id:
            return sum(1 for item in self.data.values() if item.get('user_id') == user_id)
        return len(self.data)

    async def get_by_date_range(self, start_date: date, end_date: date, date_field: str = 'date', user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Obtener elementos en un rango de fechas"""
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()
        
        results = []
        for item in self.data.values():
            # Filtrar por user_id si se proporciona
            if user_id and item.get('user_id') != user_id:
                continue
            
            item_date = item.get(date_field)
            if item_date:
                # Si la fecha está como string, convertirla para comparar
                if isinstance(item_date, str):
                    try:
                        item_date_obj = date.fromisoformat(item_date)
                    except (ValueError, AttributeError):
                        # Si no se puede parsear, saltar este item
                        continue
                    if start_date <= item_date_obj <= end_date:
                        results.append(item)
                elif isinstance(item_date, date):
                    if start_date <= item_date <= end_date:
                        results.append(item)
        
        return results
