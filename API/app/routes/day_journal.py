from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import date

from app.models.day_journal import DayJournal, DayJournalCreate, DayJournalUpdate
from app.services.day_journal_service import day_journal_service
from app.auth import get_current_user

router = APIRouter(
    prefix="/day-journal",
    tags=["day-journal"],
    responses={404: {"description": "Day journal not found"}}
)

@router.get("", response_model=List[DayJournal])
@router.get("/", response_model=List[DayJournal])
async def get_day_journals(skip: int = 0, limit: int = 100, user: dict = Depends(get_current_user)):
    """Obtener lista de todos los day_journals"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    day_journals_data = day_journal_service.get_all(skip=skip, limit=limit, user_id=user_id)

    # Convertir datos de Firebase a formato Pydantic
    day_journals = []
    for day_journal_data in day_journals_data:
        # Convertir string de fecha a objeto date
        if isinstance(day_journal_data.get('date'), str):
            try:
                day_journal_data['date'] = date.fromisoformat(day_journal_data['date'])
            except ValueError:
                # Si no se puede parsear, dejar como string
                pass
        day_journals.append(DayJournal(**day_journal_data))

    return day_journals

@router.get("/range", response_model=List[DayJournal])
async def get_day_journals_by_date_range(start_date: date, end_date: date, user: dict = Depends(get_current_user)):
    """
    Obtener day_journals en un rango de fechas.
    Útil para consultar todos los días de un mes visible en el calendario.
    Ejemplo: ?start_date=2024-10-01&end_date=2024-10-31
    """
    if start_date > end_date:
        raise HTTPException(
            status_code=400, 
            detail="start_date debe ser anterior o igual a end_date"
        )
    
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    day_journals_data = day_journal_service.get_by_date_range(start_date, end_date, user_id=user_id)

    # Convertir datos de Firebase a formato Pydantic
    day_journals = []
    for day_journal_data in day_journals_data:
        # Convertir string de fecha a objeto date
        if isinstance(day_journal_data.get('date'), str):
            try:
                day_journal_data['date'] = date.fromisoformat(day_journal_data['date'])
            except ValueError:
                # Si no se puede parsear, saltar este registro
                continue
        day_journals.append(DayJournal(**day_journal_data))

    return day_journals

@router.get("/{day_journal_id}", response_model=DayJournal)
async def get_day_journal(day_journal_id: str, user: dict = Depends(get_current_user)):
    """Obtener un day_journal específico por ID"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    day_journal_data = day_journal_service.get_by_id(day_journal_id, user_id=user_id)

    if day_journal_data is None:
        raise HTTPException(status_code=404, detail="Day journal not found")

    # Convertir string de fecha a objeto date
    if isinstance(day_journal_data.get('date'), str):
        try:
            day_journal_data['date'] = date.fromisoformat(day_journal_data['date'])
        except ValueError:
            pass

    return DayJournal(**day_journal_data)

@router.post("", response_model=DayJournal)
@router.post("/", response_model=DayJournal)
async def create_day_journal(day_journal: DayJournalCreate, user: dict = Depends(get_current_user)):
    """Crear un nuevo day_journal"""
    # El modelo Pydantic ya valida los datos
    day_journal_data = day_journal.model_dump()

    # En modo demo, no asignar user_id
    user_id = None if user.get('demo_mode') else user['uid']
    created_day_journal_data = day_journal_service.create(day_journal_data, user_id=user_id)

    # Convertir fecha de vuelta para respuesta
    if isinstance(created_day_journal_data.get('date'), str):
        try:
            created_day_journal_data['date'] = date.fromisoformat(created_day_journal_data['date'])
        except ValueError:
            pass

    return DayJournal(**created_day_journal_data)

# Alias sin barra final para soportar POST /day-journal además de /day-journal/
@router.post("", response_model=DayJournal)
async def create_day_journal_no_slash(day_journal: DayJournalCreate, user: dict = Depends(get_current_user)):
    return await create_day_journal(day_journal, user=user)

@router.put("/{day_journal_id}", response_model=DayJournal)
async def update_day_journal(day_journal_id: str, day_journal_update: DayJournalUpdate, user: dict = Depends(get_current_user)):
    """Actualizar un day_journal existente"""
    # Convertir el modelo Pydantic a dict para el servicio
    update_data = day_journal_update.model_dump(exclude_unset=True)
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    day_journal_data = day_journal_service.update(day_journal_id, update_data, user_id=user_id)

    if day_journal_data is None:
        raise HTTPException(status_code=404, detail="Day journal not found")

    # Convertir fecha de vuelta para respuesta
    if isinstance(day_journal_data.get('date'), str):
        try:
            day_journal_data['date'] = date.fromisoformat(day_journal_data['date'])
        except ValueError:
            pass

    return DayJournal(**day_journal_data)

@router.delete("/{day_journal_id}")
async def delete_day_journal(day_journal_id: str, user: dict = Depends(get_current_user)):
    """Eliminar un day_journal"""
    # En modo demo/dev, no filtrar por usuario
    user_id = None if user.get('demo_mode') else user['uid']
    day_journal = day_journal_service.delete(day_journal_id, user_id=user_id)
    if day_journal is None:
        raise HTTPException(status_code=404, detail="Day journal not found")
    return {"message": "Day journal deleted successfully", "deleted_day_journal": day_journal}


