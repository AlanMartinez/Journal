from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from datetime import date

class DatabaseService(ABC):
    """Interfaz abstracta para servicios de base de datos"""

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Obtener todos los registros"""
        pass

    @abstractmethod
    async def get_by_id(self, record_id: str) -> Optional[Dict]:
        """Obtener un registro por ID"""
        pass

    @abstractmethod
    async def create(self, data: Dict) -> Dict:
        """Crear un nuevo registro"""
        pass

    @abstractmethod
    async def update(self, record_id: str, data: Dict) -> Optional[Dict]:
        """Actualizar un registro existente"""
        pass

    @abstractmethod
    async def delete(self, record_id: str) -> Optional[Dict]:
        """Eliminar un registro"""
        pass

    @abstractmethod
    async def get_count(self) -> int:
        """Obtener el número total de registros"""
        pass
