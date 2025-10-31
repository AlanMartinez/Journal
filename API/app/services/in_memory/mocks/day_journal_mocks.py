from datetime import date
import random
import uuid

def generate_october_day_journals_for_year(year):
    """
    Genera datos mock de day_journal para todos los días laborables de octubre de un año específico.
    Excluye sábados (5) y domingos (6).
    """
    data = {}
    
    # Generar todos los días de octubre
    for day in range(1, 32):  # Octubre tiene 31 días
        try:
            current_date = date(year, 10, day)
            # weekday() retorna 0=Lunes, 1=Martes, ..., 6=Domingo
            # Excluir sábados (5) y domingos (6)
            if current_date.weekday() < 5:  # Lunes=0 a Viernes=4
                day_id = str(uuid.uuid4())
                
                # Aleatoriamente decidir si rompió el trading plan (30% de probabilidad)
                break_trading_plan = random.choice([True, False, False, False, False, False, False])
                
                # Notas opcionales según si rompió el plan
                notes = None
                if break_trading_plan:
                    notes_options = [
                        "No seguí el plan de trading hoy.",
                        "Me emocioné y tomé trades fuera del plan.",
                        "Overtrading - tomé más trades de los permitidos.",
                        "Ignoré las reglas de riesgo hoy."
                    ]
                    notes = random.choice(notes_options)
                else:
                    notes_options = [
                        "Seguí el plan correctamente hoy.",
                        "Buen día, mantuve la disciplina.",
                        None,  # Sin notas algunas veces
                        None
                    ]
                    notes = random.choice(notes_options)
                
                data[day_id] = {
                    "id": day_id,
                    "date": current_date.isoformat(),
                    "break_trading_plan": break_trading_plan,
                    "notes": notes
                }
        except ValueError:
            # Si el día no existe (ej: 31 en febrero), continuar
            continue
    
    return data

def generate_october_day_journals():
    """
    Genera datos mock de day_journal para todos los días laborables de octubre.
    Incluye múltiples años para desarrollo (2024, 2025).
    """
    # Fijar semilla para resultados consistentes
    random.seed(42)
    
    data = {}
    
    # Generar para múltiples años (2024 y 2025)
    for year in [2024, 2025]:
        year_data = generate_october_day_journals_for_year(year)
        data.update(year_data)
    
    return data

# Generar los datos mock una vez al importar el módulo
DAY_JOURNAL_MOCK_DATA = generate_october_day_journals()

