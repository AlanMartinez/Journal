from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models.confirmation import Confirmation, ConfirmationCreate
from app.services.confirmation_service import confirmation_service
from app.auth import get_current_user

router = APIRouter(
    prefix="/confirmations",
    tags=["confirmations"],
    responses={404: {"description": "Confirmation not found"}}
)

@router.get("", response_model=List[Confirmation])
@router.get("/", response_model=List[Confirmation])
async def get_confirmations(user: dict = Depends(get_current_user)):
    """Obtener lista de todas las confirmations"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    confirmations_data = confirmation_service.get_all(user_id=user_id)
    return [Confirmation(**confirmation_data) for confirmation_data in confirmations_data]

@router.post("", response_model=Confirmation)
@router.post("/", response_model=Confirmation)
async def create_confirmation(confirmation: ConfirmationCreate, user: dict = Depends(get_current_user)):
    """Crear una nueva confirmation"""
    # Convertir el modelo Pydantic a dict para el servicio
    confirmation_data = confirmation.model_dump()
    # En modo demo, no asignar user_id
    user_id = None if user.get('demo_mode') else user['uid']
    created_confirmation = confirmation_service.create(confirmation_data, user_id=user_id)
    return Confirmation(**created_confirmation)

@router.delete("/{confirmation_id}")
async def delete_confirmation(confirmation_id: str, user: dict = Depends(get_current_user)):
    """Eliminar una confirmation"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    confirmation = confirmation_service.delete(confirmation_id, user_id=user_id)
    if confirmation is None:
        raise HTTPException(status_code=404, detail="Confirmation not found")
    return {"message": "Confirmation deleted successfully", "deleted_confirmation": confirmation}
