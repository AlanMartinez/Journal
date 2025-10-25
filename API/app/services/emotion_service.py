import asyncio
from typing import List, Optional, Dict
from datetime import datetime

from app.services.database_service import DatabaseService
from app.services.firebase_service import FirebaseService
from config import FIREBASE_COLLECTION

class EmotionService:
    """Servicio para manejar emotions siguiendo principios SOLID"""

    def __init__(self, database_service: Optional[DatabaseService] = None):
        """Inicializar con inyección de dependencias"""
        collection_name = f"{FIREBASE_COLLECTION}_emotions"
        self.db: DatabaseService = database_service or FirebaseService(collection_name)
        self._load_sample_data()
        print('pase')

    def _load_sample_data(self):
        """Cargar datos de ejemplo para testing"""
        sample_emotions = [
            {"id": "1", "name": "Confianza", "description": "Sentimiento de seguridad en la operación"},
            {"id": "2", "name": "Calma", "description": "Estado de tranquilidad durante el trade"},
            {"id": "3", "name": "Ansiedad", "description": "Nerviosismo antes o durante la operación"},
            {"id": "4", "name": "Euforia", "description": "Excitación por buenos resultados"},
            {"id": "5", "name": "Frustración", "description": "Sentimiento tras pérdidas"}
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
                for emotion in sample_emotions:
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            import concurrent.futures
                            with concurrent.futures.ThreadPoolExecutor() as executor:
                                executor.submit(self._run_async_create, emotion)
                        else:
                            loop.run_until_complete(self.db.create(emotion))
                    except Exception as e:
                        print(f"Error cargando emotion de ejemplo: {e}")
        except Exception as e:
            print(f"Error verificando datos de emotions: {e}")

    def get_all(self) -> List[Dict]:
        """Obtener todas las emotions"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async, self.db.get_all())
                    return future.result()
            else:
                return loop.run_until_complete(self.db.get_all())
        except Exception as e:
            print(f"Error en get_all emotions: {e}")
            return []

    def create(self, emotion_data: Dict) -> Dict:
        """Crear una nueva emotion"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_create, emotion_data)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.create(emotion_data))
        except Exception as e:
            print(f"Error en create emotion: {e}")
            raise

    def delete(self, emotion_id: str) -> Optional[Dict]:
        """Eliminar una emotion"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self._run_async_delete, emotion_id)
                    return future.result()
            else:
                return loop.run_until_complete(self.db.delete(emotion_id))
        except Exception as e:
            print(f"Error en delete emotion: {e}")
            return None

    def get_count(self) -> int:
        """Obtener el número total de emotions"""
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
            print(f"Error en get_count emotions: {e}")
            return 0

    # Métodos auxiliares para ejecutar async functions
    def _run_async(self, coro):
        """Ejecutar coroutine en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    def _run_async_create(self, emotion_data):
        """Ejecutar create en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.create(emotion_data))
        finally:
            loop.close()

    def _run_async_delete(self, emotion_id):
        """Ejecutar delete en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.delete(emotion_id))
        finally:
            loop.close()

    def _run_async_count(self):
        """Ejecutar get_count en event loop"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.db.get_count())
        finally:
            loop.close()

# Instancia global del servicio de emotions
emotion_service = EmotionService()
