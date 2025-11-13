"""
Módulo de autenticación Firebase para FastAPI.

Proporciona dependencias para verificar tokens de Firebase Authentication
y proteger endpoints de la API.
"""

from fastapi import HTTPException, Header, Depends
from typing import Optional, Dict
import firebase_admin
from firebase_admin import auth, credentials
import os


def get_firebase_auth():
    """
    Obtiene o inicializa Firebase Admin para autenticación.
    Esta función asegura que Firebase Admin esté inicializado antes de verificar tokens.
    """
    # Si ya está inicializado, no hacer nada
    if firebase_admin._apps:
        return
    
    # Buscar archivo de credenciales
    cred_paths = [
        os.path.join(os.getcwd(), 'firebase-credentials.json'),
        os.path.join(os.path.dirname(os.getcwd()), 'firebase-credentials.json'),
        '/etc/firebase-credentials.json'
    ]

    cred = None
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
        from config import FIREBASE_CONFIG

        # Buscar credenciales completas en variables de entorno
        private_key_id = os.getenv("FIREBASE_PRIVATE_KEY_ID")
        private_key = os.getenv("FIREBASE_PRIVATE_KEY")
        client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
        client_id = os.getenv("FIREBASE_CLIENT_ID")

        project_id = None
        try:
            project_id = (FIREBASE_CONFIG or {}).get("projectId")
        except Exception:
            project_id = None
        if not project_id:
            project_id = os.getenv("FIREBASE_PROJECT_ID")

        if all([project_id, private_key_id, private_key, client_email]):
            # Crear credenciales desde variables de entorno
            cred_dict = {
                "type": "service_account",
                "project_id": project_id,
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
            # No lanzar excepción aquí porque esto podría ejecutarse durante la inicialización
            # La verificación de credenciales se hará cuando se intente verificar un token
            return

    # Inicializar Firebase solo si no está inicializado y tenemos credenciales
    if cred and not firebase_admin._apps:
        try:
            firebase_admin.initialize_app(cred)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error initializing Firebase: {str(e)}"
            )


async def verify_token(authorization: Optional[str] = Header(None)) -> Dict:
    """
    Dependencia de FastAPI para verificar tokens de Firebase Authentication.
    
    Extrae el token del header Authorization y lo valida contra Firebase.
    En modo development, también acepta tokens demo que empiezan con "demo_token_".
    
    Args:
        authorization: Header Authorization con formato "Bearer <token>"
    
    Returns:
        Dict con la información del usuario autenticado (uid, email, etc.)
    
    Raises:
        HTTPException: 401 si el token es inválido o falta
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Expected 'Bearer <token>'"
        )
    
    token = authorization.split(" ")[1]
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token missing in authorization header"
        )
    
    # Modo demo: en development, aceptar tokens que empiezan con "demo_token_"
    ENV = os.getenv('ENV', 'development')
    if ENV == 'development' and token.startswith('demo_token_'):
        # Retornar un token demo válido
        return {
            "uid": "demo_user",
            "email": "demo@tradejournal.com",
            "name": "Usuario Demo",
            "display_name": "Usuario Demo",
            "demo_mode": True
        }
    
    # Asegurar que Firebase Admin esté inicializado
    get_firebase_auth()
    
    # Verificar que Firebase esté inicializado
    if not firebase_admin._apps:
        raise HTTPException(
            status_code=500,
            detail="Firebase Admin not initialized. Please configure Firebase credentials."
        )
    
    try:
        # Verificar el token con Firebase Admin
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token verification failed: {str(e)}"
        )


async def get_current_user(decoded_token: Dict = Depends(verify_token)) -> Dict:
    """
    Dependencia que extrae información útil del token decodificado.
    
    Args:
        decoded_token: Token decodificado de Firebase
    
    Returns:
        Dict con uid, email, name del usuario y demo_mode si aplica
    """
    return {
        "uid": decoded_token.get("uid"),
        "email": decoded_token.get("email"),
        "name": decoded_token.get("name") or decoded_token.get("display_name"),
        "demo_mode": decoded_token.get("demo_mode", False),
        "firebase_claims": decoded_token
    }

