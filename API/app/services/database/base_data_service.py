from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any, TypeVar, Generic

T = TypeVar('T')

class BaseDataService(ABC):
    """Interfaz base para todos los servicios de datos"""
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener todos los elementos"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """Obtener un elemento por ID"""
        pass
    
    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo elemento"""
        pass
    
    @abstractmethod
    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizar un elemento existente"""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Eliminar un elemento"""
        pass
    
    @abstractmethod
    async def get_count(self) -> int:
        """Obtener el conteo total de elementos"""
        pass
