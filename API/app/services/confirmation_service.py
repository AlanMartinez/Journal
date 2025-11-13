import os
import asyncio
from typing import List, Optional, Dict
from datetime import datetime

from app.services.database.database_service import DatabaseService
from app.services.database.firebase_service import FirebaseService
from app.services.in_memory.in_memory_service import InMemoryService
from config import FIREBASE_COLLECTION

class ConfirmationService:
    """Servicio para manejar confirmations siguiendo principios SOLID"""

    def __init__(self, database_service: Optional[DatabaseService] = None):
        """Inicializar con inyección de dependencias"""
        collection_name = f"{FIREBASE_COLLECTION}_confirmations"
        if database_service is not None:
            self.db = database_service
        else:
            # Usar InMemoryService en desarrollo, Firebase en producción
            if os.getenv('ENV') == 'development':
                self.db = InMemoryService(collection_name)
            else:
                self.db = FirebaseService(collection_name)
        self._load_sample_data()

    def _load_sample_data(self):
        """Cargar datos de ejemplo para testing"""
        sample_confirmations = [
            {"id": "1", "name": "FVG", "description": "Fair Value Gap - Hueco de valor justo"},
            {"id": "2", "name": "CISD", "description": "Change in State of Delivery"},
            {"id": "3", "name": "IFVG", "description": "Internal Fair Value Gap"},
            {"id": "4", "name": "OB", "description": "Order Block - Bloque de órdenes"},
            {"id": "5", "name": "PDL", "description": "Previous Day Low - Mínimo del día anterior"},
            {"id": "6", "name": "PDH", "description": "Previous Day High - Máximo del día anterior"},
            {"id": "7", "name": "LTF", "description": "Lower Time Frame - Marco temporal inferior"},
            {"id": "8", "name": "HTF", "description": "Higher Time Frame - Marco temporal superior"}
        ]

        # Cargar datos de ejemplo solo si no hay datos en Firebase
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_count)
                    count = future.result()
            else:
                count = loop.run_until_complete(self.db.get_count())

            if count == 0:
                for confirmation in sample_confirmations:
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                executor.submit(self._run_async_create, confirmation)
                        else:
                            loop.run_until_complete(self.db.create(confirmation))
                    except Exception as e:
                        print(f"Error cargando confirmation de ejemplo: {e}")
        except Exception as e:
            print(f"Error verificando datos de confirmations: {e}")

    def get_all(self, user_id: Optional[str] = None) -> List[Dict]:
        """Obtener todas las confirmations"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async, self.db.get_all(user_id=user_id))
                    return future.result()
            else:
                return loop.run_until_complete(self.db.get_all(user_id=user_id))
        except Exception as e:
            print(f"Error en get_all confirmations: {e}")
            return []

    def create(self, confirmation_data: Dict, user_id: Optional[str] = None) -> Dict:
        """Crear una nueva confirmation"""
        try:
            # Agregar user_id al confirmation_data si se proporciona
            if user_id:
                confirmation_data['user_id'] = user_id
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_create, confirmation_data)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.create(confirmation_data))
        except Exception as e:
            print(f"Error en create confirmation: {e}")
            raise

    def delete(self, confirmation_id: str, user_id: Optional[str] = None) -> Optional[Dict]:
        """Eliminar una confirmation"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_delete, confirmation_id, user_id)
                    return future.result()
            else:
                result = loop.run_until_complete(self.db.delete(confirmation_id, user_id=user_id))
                # InMemoryService retorna bool, FirebaseService retorna Dict o None
                if isinstance(result, bool):
                    if result:
                        # Obtener el registro antes de eliminarlo para retornarlo
                        return loop.run_until_complete(self.db.get_by_id(confirmation_id, user_id=user_id))
                    return None
                return result
        except Exception as e:
            print(f"Error en delete confirmation: {e}")
            return None

    def get_count(self) -> int:
        """Obtener el número total de confirmations"""
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
            print(f"Error en get_count confirmations: {e}")
            return 0

    # Métodos auxiliares para ejecutar async functions
    def _run_async(self, coro):
        """Ejecutar coroutine en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    def _run_async_create(self, confirmation_data):
        """Ejecutar create en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.create(confirmation_data))
        finally:
            loop.close()

    def _run_async_delete(self, confirmation_id, user_id=None):
        """Ejecutar delete en event loop"""
        loop = asyncio.new_event_loop()
        try:
            result = loop.run_until_complete(self.db.delete(confirmation_id, user_id=user_id))
            if isinstance(result, bool):
                if result:
                    return loop.run_until_complete(self.db.get_by_id(confirmation_id, user_id=user_id))
                return None
            return result
        finally:
            loop.close()

    def _run_async_count(self):
        """Ejecutar get_count en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.get_count())
        finally:
            loop.close()

# Instancia global del servicio de confirmations
confirmation_service = ConfirmationService()
