from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.emotion import Emotion, EmotionCreate
from app.services.emotion_service import emotion_service
from app.auth import get_current_user

router = APIRouter(
    prefix="/emotions",
    tags=["emotions"],
    responses={404: {"description": "Emotion not found"}}
)

@router.get("/", response_model=List[Emotion])
async def get_emotions(user: dict = Depends(get_current_user)):
    """Obtener lista de todas las emotions"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    emotions_data = emotion_service.get_all(user_id=user_id)
    return [Emotion(**emotion_data) for emotion_data in emotions_data]

@router.post("/", response_model=Emotion)
async def create_emotion(emotion: EmotionCreate, user: dict = Depends(get_current_user)):
    """Crear una nueva emotion"""
    # Convertir el modelo Pydantic a dict para el servicio
    emotion_data = emotion.model_dump()
    # En modo demo, no asignar user_id
    user_id = None if user.get('demo_mode') else user['uid']
    created_emotion = emotion_service.create(emotion_data, user_id=user_id)
    return Emotion(**created_emotion)

@router.delete("/{emotion_id}")
async def delete_emotion(emotion_id: str, user: dict = Depends(get_current_user)):
    """Eliminar una emotion"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    emotion = emotion_service.delete(emotion_id, user_id=user_id)
    if emotion is None:
        raise HTTPException(status_code=404, detail="Emotion not found")
    return {"message": "Emotion deleted successfully", "deleted_emotion": emotion}
