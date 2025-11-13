from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
from datetime import date

from app.services.trade_service import trade_service
from app.services.day_journal_service import day_journal_service
from app.models.trade import Trade
from app.models.day_journal import DayJournal
from app.auth import get_current_user

router = APIRouter(
    prefix="/export",
    tags=["export"],
)

def _get_all_records(service, batch_size: int = 1000, user_id: Optional[str] = None) -> List[Dict]:
    """
    Obtener todos los registros de un servicio usando paginación
    """
    all_records = []
    skip = 0
    
    while True:
        # Intentar pasar user_id si está disponible y el servicio lo soporta
        try:
            if user_id:
                # Intentar llamar con user_id primero (para servicios que lo soportan)
                import inspect
                sig = inspect.signature(service.get_all)
                if 'user_id' in sig.parameters:
                    batch = service.get_all(skip=skip, limit=batch_size, user_id=user_id)
                else:
                    batch = service.get_all(skip=skip, limit=batch_size)
            else:
                batch = service.get_all(skip=skip, limit=batch_size)
        except TypeError:
            # Si falla, intentar sin user_id
            batch = service.get_all(skip=skip, limit=batch_size)
        
        if not batch:
            break
        all_records.extend(batch)
        
        # Si obtenemos menos registros que el batch_size, significa que no hay más
        if len(batch) < batch_size:
            break
        
        skip += batch_size
    
    return all_records

@router.get("/all")
async def export_all_data(user: dict = Depends(get_current_user)):
    """
    Exportar toda la información de las colecciones trades y dayjournal en formato JSON
    """
    try:
        user_id = user['uid']
        # Obtener todos los trades usando paginación filtrados por usuario
        trades_data = _get_all_records(trade_service, user_id=user_id)
        
        # Convertir datos de trades a formato Pydantic
        trades = []
        for trade_data in trades_data:
            # Convertir string de fecha a objeto date
            if isinstance(trade_data.get('date'), str):
                try:
                    trade_data['date'] = date.fromisoformat(trade_data['date'])
                except ValueError:
                    pass
            # Usar mode='json' para serializar fechas como strings ISO
            trades.append(Trade(**trade_data).model_dump(mode='json'))
        
        # Obtener todos los day journals usando paginación filtrados por usuario
        day_journals_data = _get_all_records(day_journal_service, user_id=user_id)
        
        # Convertir datos de day journals a formato Pydantic
        day_journals = []
        for day_journal_data in day_journals_data:
            # Convertir string de fecha a objeto date
            if isinstance(day_journal_data.get('date'), str):
                try:
                    day_journal_data['date'] = date.fromisoformat(day_journal_data['date'])
                except ValueError:
                    pass
            # Usar mode='json' para serializar fechas como strings ISO
            day_journals.append(DayJournal(**day_journal_data).model_dump(mode='json'))
        
        # Crear el objeto de respuesta con toda la información
        export_data: Dict[str, Any] = {
            "trades": trades,
            "day_journals": day_journals,
            "metadata": {
                "total_trades": len(trades),
                "total_day_journals": len(day_journals),
                "export_date": date.today().isoformat()
            }
        }
        
        return JSONResponse(content=export_data)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Error al exportar los datos", "detail": str(e)}
        )

