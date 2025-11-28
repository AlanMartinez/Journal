from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date

from app.models.trade import Trade, TradeCreate, TradeUpdate
from app.services.trade_service import trade_service
from app.services.trade_stats_service import trade_stats_service
from app.auth import get_current_user

router = APIRouter(
    prefix="/trades",
    tags=["trades"],
    responses={404: {"description": "Trade not found"}}
)

@router.get("", response_model=List[Trade])
@router.get("/", response_model=List[Trade])
async def get_trades(skip: int = 0, limit: int = 100, user: dict = Depends(get_current_user)):
    """Obtener lista de todos los trades"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    trades_data = trade_service.get_all(skip=skip, limit=limit, user_id=user_id)

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
async def get_trade(trade_id: str, user: dict = Depends(get_current_user)):
    """Obtener un trade específico por ID"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    trade_data = trade_service.get_by_id(trade_id, user_id=user_id)

    if trade_data is None:
        raise HTTPException(status_code=404, detail="Trade not found")

    # Convertir string de fecha a objeto date
    if isinstance(trade_data.get('date'), str):
        try:
            trade_data['date'] = date.fromisoformat(trade_data['date'])
        except ValueError:
            pass

    return Trade(**trade_data)

@router.post("", response_model=Trade)
@router.post("/", response_model=Trade)
async def create_trade(trade: TradeCreate, user: dict = Depends(get_current_user)):
    """Crear un nuevo trade"""
    # El modelo Pydantic ya valida los datos
    trade_data = trade.model_dump()

    # En modo demo, no asignar user_id (los datos mock no tienen user_id)
    # En modo usuario real, asignar el user_id del usuario
    user_id = None if user.get('demo_mode') else user['uid']
    created_trade_data = await trade_service.create_async(trade_data, user_id=user_id)

    # Convertir fecha de vuelta para respuesta
    if isinstance(created_trade_data.get('date'), str):
        try:
            created_trade_data['date'] = date.fromisoformat(created_trade_data['date'])
        except ValueError:
            pass

    return Trade(**created_trade_data)

@router.put("/{trade_id}", response_model=Trade)
async def update_trade(trade_id: str, trade_update: TradeUpdate, user: dict = Depends(get_current_user)):
    """Actualizar un trade existente"""
    # Convertir el modelo Pydantic a dict para el servicio
    update_data = trade_update.model_dump(exclude_unset=True)
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    trade_data = trade_service.update(trade_id, update_data, user_id=user_id)

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
async def delete_trade(trade_id: str, user: dict = Depends(get_current_user)):
    """Eliminar un trade"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    trade = trade_service.delete(trade_id, user_id=user_id)
    if trade is None:
        raise HTTPException(status_code=404, detail="Trade not found")
    return {"message": "Trade deleted successfully", "deleted_trade": trade}

@router.get("/stats/summary")
async def get_trades_summary(user: dict = Depends(get_current_user)):
    """Obtener estadísticas básicas de trades"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    return trade_stats_service.get_summary(user_id=user_id)
