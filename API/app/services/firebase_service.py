import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, List, Optional
import os

from app.services.database_service import DatabaseService
from config import FIREBASE_DATABASE_ID

class FirebaseService(DatabaseService):
    """Servicio Firebase Firestore siguiendo principios SOLID"""

    def __init__(self, collection_name: str):
        """Inicializar Firebase con inyección de dependencias"""
        self.collection_name = collection_name
        self._init_firebase()
        self.db = firestore.client(database_id=FIREBASE_DATABASE_ID)

    def _init_firebase(self):
        """Inicializar Firebase Admin SDK"""
        # Buscar archivo de credenciales
        cred_paths = [
            os.path.join(os.getcwd(), 'firebase-credentials.json'),
            os.path.join(os.path.dirname(os.getcwd()), 'firebase-credentials.json'),
            '/etc/firebase-credentials.json'
        ]

        cred_path = None
        for path in cred_paths:
            if os.path.exists(path):
                cred_path = path
                break

        if cred_path:
            # Usar archivo de credenciales
            cred = credentials.Certificate(cred_path)
        else:
            # Intentar usar variables de entorno
            import json
            from config import FIREBASE_CONFIG

            # Buscar credenciales completas en variables de entorno
            private_key_id = os.getenv("FIREBASE_PRIVATE_KEY_ID")
            private_key = os.getenv("FIREBASE_PRIVATE_KEY")
            client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
            client_id = os.getenv("FIREBASE_CLIENT_ID")

            if all([FIREBASE_CONFIG.get("projectId"), private_key_id, private_key, client_email]):
                # Crear credenciales desde variables de entorno
                cred_dict = {
                    "type": "service_account",
                    "project_id": FIREBASE_CONFIG.get("projectId"),
                    "private_key_id": private_key_id,
                    "private_key": private_key.replace('\\n', '\n'),
                    "client_email": client_email,
                    "client_id": client_id,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{client_email}"
                }
                cred = credentials.Certificate(cred_dict)
            else:
                # No hay credenciales válidas
                print("⚠️  No se encontraron credenciales de Firebase válidas.")
                print("📝 Configura:")
                print("   - Archivo: firebase-credentials.json en el directorio API/")
                print("   - O variables de entorno: FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, etc.")
                print("   - O edita config.py con tus credenciales")
                print("🔄 La API funcionará en modo de desarrollo (datos temporales)")
                return

        # Inicializar Firebase solo si no está inicializado
        if not firebase_admin._apps:
            try:
                firebase_admin.initialize_app(cred)
                print("✅ Firebase inicializado correctamente")
            except Exception as e:
                print(f"❌ Error inicializando Firebase: {e}")
                print("🔄 Continuando en modo de desarrollo...")

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Obtener todos los trades ordenados por fecha descendente"""
        try:
            trades_ref = self.db.collection(self.collection_name)
            query = trades_ref.order_by('date', direction=firestore.Query.DESCENDING)
            docs = query.limit(limit).offset(skip).stream()

            trades = []
            for doc in docs:
                trade_data = doc.to_dict()
                trade_data['id'] = doc.id
                trades.append(trade_data)

            return trades
        except Exception as e:
            print(f"❌ Error obteniendo trades: {e}")
            return []

    async def get_by_id(self, record_id: str) -> Optional[Dict]:
        """Obtener un trade por ID"""
        try:
            doc = self.db.collection(self.collection_name).document(record_id).get()
            if doc.exists:
                trade_data = doc.to_dict()
                trade_data['id'] = doc.id
                return trade_data
            return None
        except Exception as e:
            print(f"❌ Error obteniendo trade {record_id}: {e}")
            return None

    async def create(self, data: Dict) -> Dict:
        """Crear un nuevo trade"""
        try:
            # Preparar datos para Firestore
            trade_data = self._prepare_data_for_firestore(data)

            # Crear documento
            doc_ref = self.db.collection(self.collection_name).document()
            doc_ref.set(trade_data)

            # Retornar con ID
            trade_data['id'] = doc_ref.id
            return trade_data
        except Exception as e:
            print(f"❌ Error creando trade: {e}")
            raise

    async def update(self, record_id: str, data: Dict) -> Optional[Dict]:
        """Actualizar un trade existente"""
        try:
            # Preparar datos para Firestore
            update_data = self._prepare_data_for_firestore(data)

            # Actualizar documento
            doc_ref = self.db.collection(self.collection_name).document(record_id)
            doc_ref.update(update_data)

            # Obtener datos actualizados
            updated_doc = doc_ref.get()
            if updated_doc.exists:
                trade_data = updated_doc.to_dict()
                trade_data['id'] = updated_doc.id
                return trade_data
            return None
        except Exception as e:
            print(f"❌ Error actualizando trade {record_id}: {e}")
            return None

    async def delete(self, record_id: str) -> Optional[Dict]:
        """Eliminar un trade"""
        try:
            # Obtener datos antes de eliminar
            trade = await self.get_by_id(record_id)
            if trade is None:
                return None

            # Eliminar documento
            self.db.collection(self.collection_name).document(record_id).delete()
            return trade
        except Exception as e:
            print(f"❌ Error eliminando trade {record_id}: {e}")
            return None

    async def get_count(self) -> int:
        """Obtener el número total de trades"""
        try:
            docs = self.db.collection(self.collection_name).stream()
            return sum(1 for _ in docs)
        except Exception as e:
            print(f"❌ Error contando trades: {e}")
            return 0

    def _prepare_data_for_firestore(self, data: Dict) -> Dict:
        """Preparar datos para almacenamiento en Firestore"""
        prepared_data = {}

        for key, value in data.items():
            if hasattr(value, 'isoformat'):  # date objects
                # Convertir date a string para Firestore
                prepared_data[key] = value.isoformat()
            elif isinstance(value, list):
                # Firestore maneja listas bien
                prepared_data[key] = value
            elif value is not None:
                prepared_data[key] = value
            # Ignorar valores None

        return prepared_data
