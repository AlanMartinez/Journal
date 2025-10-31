from pydantic import BaseModel
from typing import Optional
from datetime import date

class DayJournalBase(BaseModel):
    """Modelo base para day_journal"""
    date: date
    break_trading_plan: bool = False
    notes: Optional[str] = None

class DayJournalCreate(DayJournalBase):
    """Modelo para crear day_journal"""
    pass

class DayJournalUpdate(BaseModel):
    """Modelo para actualizar day_journal (todos los campos opcionales)"""
    # date no se incluye porque no debe cambiar (identifica el día específico)
    break_trading_plan: Optional[bool] = None
    notes: Optional[str] = None

class DayJournal(DayJournalBase):
    """Modelo completo de day_journal con ID"""
    id: str  # Firestore usa string IDs

    model_config = {"from_attributes": True}


