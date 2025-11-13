from pydantic import BaseModel
from typing import Optional

class EmotionBase(BaseModel):
    """Modelo base para emotions"""
    name: str
    description: Optional[str] = None
    user_id: Optional[str] = None  # ID del usuario propietario

class EmotionCreate(EmotionBase):
    """Modelo para crear emotions"""
    pass

class Emotion(EmotionBase):
    """Modelo completo de emotion con ID"""
    id: str

    model_config = {"from_attributes": True}

class ConfirmationBase(BaseModel):
    """Modelo base para confirmations"""
    name: str
    description: Optional[str] = None

class ConfirmationCreate(ConfirmationBase):
    """Modelo para crear confirmations"""
    pass

class Confirmation(ConfirmationBase):
    """Modelo completo de confirmation con ID"""
    id: str

    model_config = {"from_attributes": True}
