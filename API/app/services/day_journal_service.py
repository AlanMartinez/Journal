import os
import asyncio
from typing import List, Optional, Dict
from datetime import datetime, date

from app.services.database.database_service import DatabaseService
from app.services.database.firebase_service import FirebaseService
from app.services.in_memory.in_memory_service import InMemoryService
from config import FIREBASE_COLLECTION

class DayJournalService:
    """Servicio para manejar day_journal siguiendo principios SOLID"""

    def __init__(self, database_service: Optional[DatabaseService] = None):
        """Inicializar con inyección de dependencias"""
        collection_name = f"{FIREBASE_COLLECTION}_day_journal"
        if database_service is not None:
            self.db = database_service
        else:
            # Usar InMemoryService en desarrollo, Firebase en producción
            if os.getenv('ENV') == 'development':
                self.db = InMemoryService(collection_name)
            else:
                self.db = FirebaseService(collection_name)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Obtener todos los day_journals"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async, self.db.get_all(skip, limit))
                    return future.result()
            else:
                return loop.run_until_complete(self.db.get_all(skip, limit))
        except Exception as e:
            print(f"Error en get_all day_journals: {e}")
            return []

    def get_by_id(self, day_journal_id: str) -> Optional[Dict]:
        """Obtener un day_journal por ID"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async, self.db.get_by_id(day_journal_id))
                    return future.result()
            else:
                return loop.run_until_complete(self.db.get_by_id(day_journal_id))
        except Exception as e:
            print(f"Error en get_by_id day_journal: {e}")
            return None

    def create(self, day_journal_data: Dict) -> Dict:
        """Crear un nuevo day_journal"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_create, day_journal_data)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.create(day_journal_data))
        except Exception as e:
            print(f"Error en create day_journal: {e}")
            raise

    def update(self, day_journal_id: str, day_journal_data: Dict) -> Optional[Dict]:
        """Actualizar un day_journal existente"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_update, day_journal_id, day_journal_data)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.update(day_journal_id, day_journal_data))
        except Exception as e:
            print(f"Error en update day_journal: {e}")
            return None

    def delete(self, day_journal_id: str) -> Optional[Dict]:
        """Eliminar un day_journal"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_delete, day_journal_id)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.delete(day_journal_id))
        except Exception as e:
            print(f"Error en delete day_journal: {e}")
            return None

    def get_count(self) -> int:
        """Obtener el número total de day_journals"""
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
            print(f"Error en get_count day_journals: {e}")
            return 0

    # Métodos auxiliares para ejecutar async functions
    def _run_async(self, coro):
        """Ejecutar coroutine en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    def _run_async_create(self, day_journal_data):
        """Ejecutar create en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.create(day_journal_data))
        finally:
            loop.close()

    def _run_async_update(self, day_journal_id, day_journal_data):
        """Ejecutar update en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.update(day_journal_id, day_journal_data))
        finally:
            loop.close()

    def _run_async_delete(self, day_journal_id):
        """Ejecutar delete en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.delete(day_journal_id))
        finally:
            loop.close()

    def _run_async_count(self):
        """Ejecutar get_count en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.get_count())
        finally:
            loop.close()

    def get_by_date_range(self, start_date: date, end_date: date) -> List[Dict]:
        """Obtener day_journals en un rango de fechas"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_date_range, start_date, end_date)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.get_by_date_range(start_date, end_date))
        except Exception as e:
            print(f"Error en get_by_date_range day_journals: {e}")
            return []

    def _run_async_date_range(self, start_date: date, end_date: date):
        """Ejecutar get_by_date_range en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.get_by_date_range(start_date, end_date))
        finally:
            loop.close()

# Instancia global del servicio de day_journals
day_journal_service = DayJournalService()


