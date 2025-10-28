import asyncio
import os
from typing import List, Optional, Dict, Any
from datetime import datetime, date

from .database.base_data_service import BaseDataService
from .in_memory.in_memory_service import InMemoryService

# Importación condicional de Firebase
if os.getenv('ENV') != 'development':
    from .firebase_service import FirebaseService
    from config import FIREBASE_COLLECTION

class TradeService:
    """Servicio para manejar trades siguiendo principios SOLID"""

    def __init__(self, data_service: Optional[BaseDataService] = None):
        """Inicializar con inyección de dependencias"""
        if data_service is not None:
            self.db = data_service
        else:
            # Si no se proporciona un servicio, elegir según el entorno
            if os.getenv('ENV') == 'development':
                self.db = InMemoryService("trades")
            else:
                self.db = FirebaseService(FIREBASE_COLLECTION)

    async def get_all_async(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Versión asíncrona para obtener todos los trades"""
        try:
            return await self.db.get_all(skip, limit)
        except Exception as e:
            print(f"Error en get_all_async: {e}")
            return []

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Obtener todos los trades ordenados por fecha descendente"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        asyncio.run, 
                        self.get_all_async(skip, limit)
                    )
                    return future.result()
            else:
                return loop.run_until_complete(self.get_all_async(skip, limit))
        except Exception as e:
            print(f"Error en get_all: {e}")
            return []

    def get_by_id(self, trade_id: str) -> Optional[Dict]:
        """Obtener un trade por ID"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async, self.db.get_by_id(trade_id))
                    return future.result()
            else:
                return loop.run_until_complete(self.db.get_by_id(trade_id))
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None

    def create(self, trade_data: Dict) -> Dict:
        """Crear un nuevo trade"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_create, trade_data)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.create(trade_data))
        except Exception as e:
            print(f"Error en create: {e}")
            raise

    def update(self, trade_id: str, trade_data: Dict) -> Optional[Dict]:
        """Actualizar un trade existente"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_update, trade_id, trade_data)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.update(trade_id, trade_data))
        except Exception as e:
            print(f"Error en update: {e}")
            return None

    def delete(self, trade_id: str) -> Optional[Dict]:
        """Eliminar un trade"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_delete, trade_id)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.delete(trade_id))
        except Exception as e:
            print(f"Error en delete: {e}")
            return None

    def get_count(self) -> int:
        """Obtener el número total de trades"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_count)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.get_count())
        except Exception as e:
            print(f"Error en get_count: {e}")
            return 0

    # Métodos auxiliares para ejecutar async functions
    def _run_async(self, coro):
        """Ejecutar coroutine en event loop existente"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    def _run_async_create(self, trade_data):
        """Ejecutar create en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.create(trade_data))
        finally:
            loop.close()

    def _run_async_update(self, trade_id, trade_data):
        """Ejecutar update en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.update(trade_id, trade_data))
        finally:
            loop.close()

    def _run_async_delete(self, trade_id):
        """Ejecutar delete en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.delete(trade_id))
        finally:
            loop.close()

    def _run_async_count(self):
        """Ejecutar get_count en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.get_count())
        finally:
            loop.close()

# Factory function para crear el servicio apropiado según el entorno
def create_trade_service(use_in_memory: bool = None) -> 'TradeService':
    """Crea una instancia de TradeService con el backend configurado"""
    if use_in_memory is None:
        use_in_memory = os.getenv('ENV') == 'development'
    
    if use_in_memory:
        return TradeService(InMemoryService("trades"))
    else:
        return TradeService()

# Instancia global del servicio de trades
trade_service = create_trade_service()
