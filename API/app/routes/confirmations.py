from fastapi import APIRouter, HTTPException
from typing import List

from app.models.confirmation import Confirmation, ConfirmationCreate
from app.services.confirmation_service import confirmation_service

router = APIRouter(
    prefix="/confirmations",
    tags=["confirmations"],
    responses={404: {"description": "Confirmation not found"}}
)

@router.get("/", response_model=List[Confirmation])
async def get_confirmations():
    """Obtener lista de todas las confirmations"""
    confirmations_data = confirmation_service.get_all()
    return [Confirmation(**confirmation_data) for confirmation_data in confirmations_data]

@router.post("/", response_model=Confirmation)
async def create_confirmation(confirmation: ConfirmationCreate):
    """Crear una nueva confirmation"""
    # Convertir el modelo Pydantic a dict para el servicio
    confirmation_data = confirmation.model_dump()
    created_confirmation = confirmation_service.create(confirmation_data)
    return Confirmation(**created_confirmation)

@router.delete("/{confirmation_id}")
async def delete_confirmation(confirmation_id: str):
    """Eliminar una confirmation"""
    confirmation = confirmation_service.delete(confirmation_id)
    if confirmation is None:
        raise HTTPException(status_code=404, detail="Confirmation not found")
    return {"message": "Confirmation deleted successfully", "deleted_confirmation": confirmation}
