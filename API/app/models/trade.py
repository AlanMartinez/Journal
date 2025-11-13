from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class TradeBase(BaseModel):
    """Modelo base para trades"""
    symbol: str
    side: str  # 'buy' or 'sell'
    date: date
    rate: float
    risk: Optional[float] = None
    result: Optional[float] = None
    status: Optional[str] = None  # 'TP', 'SL', 'BE'
    notes: Optional[str] = None
    emotions: List[str] = []
    confirmations: List[str] = []
    trading_link: Optional[str] = None
    user_id: Optional[str] = None  # ID del usuario propietario

class TradeCreate(TradeBase):
    """Modelo para crear trades"""
    pass

class TradeUpdate(BaseModel):
    """Modelo para actualizar trades (todos los campos opcionales)"""
    symbol: Optional[str] = None
    side: Optional[str] = None
    date: Optional[date] = None
    rate: Optional[float] = None
    risk: Optional[float] = None
    result: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    emotions: Optional[List[str]] = None
    confirmations: Optional[List[str]] = None
    trading_link: Optional[str] = None

class Trade(TradeBase):
    """Modelo completo de trade con ID"""
    id: str  # Firestore usa string IDs

    model_config = {"from_attributes": True}
