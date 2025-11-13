"""
Rutas de autenticación para el intercambio de tokens de Firebase.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth import verify_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class FirebaseTokenRequest(BaseModel):
    """Request model para intercambio de token de Firebase"""
    id_token: str


@router.post("/firebase")
async def exchange_firebase_token(request: FirebaseTokenRequest):
    """
    Endpoint para intercambiar un token de Firebase por un token interno.
    
    El cliente envía el idToken de Firebase, y el servidor lo valida.
    Como estamos usando Firebase Admin para verificar tokens, el idToken
    es en sí mismo un JWT válido que puede usarse directamente.
    
    Args:
        request: Request body con el id_token de Firebase
        
    Returns:
        Dict con el token y información del usuario
    """
    try:
        # Verificar el token de Firebase
        # Usamos "Bearer" + token para simular un header Authorization
        authorization = f"Bearer {request.id_token}"
        
        # verify_token espera el header desde Header() dependency
        # Necesitamos crear una función auxiliar para esto
        decoded_token = await _verify_token_direct(request.id_token)
        
        # Extraer información del usuario
        user_info = {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "name": decoded_token.get("name") or decoded_token.get("display_name"),
        }
        
        # Devolver el idToken de Firebase que es el JWT válido
        # El cliente lo usará como Bearer token en requests subsecuentes
        return {
            "access_token": request.id_token,  # El idToken de Firebase es nuestro JWT
            "token_type": "bearer",
            "user": user_info
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}"
        )


async def _verify_token_direct(token: str):
    """
    Función auxiliar para verificar el token directamente sin el header.
    Reutiliza la lógica de verify_token pero con el token directo.
    """
    from app.auth import get_firebase_auth
    import firebase_admin
    from firebase_admin import auth as firebase_auth
    
    # Asegurar que Firebase Admin esté inicializado
    get_firebase_auth()
    
    # Verificar que Firebase esté inicializado
    if not firebase_admin._apps:
        raise HTTPException(
            status_code=500,
            detail="Firebase Admin not initialized"
        )
    
    try:
        # Verificar el token con Firebase Admin
        decoded_token = firebase_auth.verify_id_token(token)
        return decoded_token
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Token verification failed: {str(e)}"
        )

