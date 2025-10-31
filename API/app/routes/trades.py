from fastapi import APIRouter, HTTPException
from typing import List
from datetime import date

from app.models.trade import Trade, TradeCreate, TradeUpdate
from app.services.trade_service import trade_service
from app.services.trade_stats_service import trade_stats_service

router = APIRouter(
    prefix="/trades",
    tags=["trades"],
    responses={404: {"description": "Trade not found"}}
)

@router.get("/", response_model=List[Trade])
async def get_trades(skip: int = 0, limit: int = 100):
    """Obtener lista de todos los trades"""
    trades_data = trade_service.get_all(skip=skip, limit=limit)

    # Convertir datos de Firebase a formato Pydantic
    trades = []
    for trade_data in trades_data:
        # Convertir string de fecha a objeto date
        if isinstance(trade_data.get('date'), str):
            try:
                trade_data['date'] = date.fromisoformat(trade_data['date'])
            except ValueError:
                # Si no se puede parsear, dejar como string
                pass
        trades.append(Trade(**trade_data))

    # Ordenar por fecha descendente
    try:
        trades.sort(key=lambda t: t.date, reverse=True)
    except Exception:
        # Si algo falla en la comparación, devolver sin ordenar
        pass

    return trades

@router.get("/{trade_id}", response_model=Trade)
async def get_trade(trade_id: str):
    """Obtener un trade específico por ID"""
    trade_data = trade_service.get_by_id(trade_id)

    if trade_data is None:
        raise HTTPException(status_code=404, detail="Trade not found")

    # Convertir string de fecha a objeto date
    if isinstance(trade_data.get('date'), str):
        try:
            trade_data['date'] = date.fromisoformat(trade_data['date'])
        except ValueError:
            pass

    return Trade(**trade_data)

@router.post("/", response_model=Trade)
async def create_trade(trade: TradeCreate):
    """Crear un nuevo trade"""
    # El modelo Pydantic ya valida los datos
    trade_data = trade.model_dump()

    # El servicio maneja la conversión a Firebase
    created_trade_data = trade_service.create(trade_data)

    # Convertir fecha de vuelta para respuesta
    if isinstance(created_trade_data.get('date'), str):
        try:
            created_trade_data['date'] = date.fromisoformat(created_trade_data['date'])
        except ValueError:
            pass

    return Trade(**created_trade_data)

@router.put("/{trade_id}", response_model=Trade)
async def update_trade(trade_id: str, trade_update: TradeUpdate):
    """Actualizar un trade existente"""
    # Convertir el modelo Pydantic a dict para el servicio
    update_data = trade_update.model_dump(exclude_unset=True)
    trade_data = trade_service.update(trade_id, update_data)

    if trade_data is None:
        raise HTTPException(status_code=404, detail="Trade not found")

    # Convertir fecha de vuelta para respuesta
    if isinstance(trade_data.get('date'), str):
        try:
            trade_data['date'] = date.fromisoformat(trade_data['date'])
        except ValueError:
            pass

    return Trade(**trade_data)

@router.delete("/{trade_id}")
async def delete_trade(trade_id: str):
    """Eliminar un trade"""
    trade = trade_service.delete(trade_id)
    if trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return {"message": "Trade deleted successfully", "deleted_trade": trade}

@router.get("/stats/summary")
async def get_trades_summary():
    """Obtener estadísticas básicas de trades"""
    return trade_stats_service.get_summary()
