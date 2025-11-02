# Tests Unitarios - TradeJournal API

Este directorio contiene los tests unitarios para la API de TradeJournal.

## Estructura

```
tests/
├── __init__.py
├── conftest.py           # Configuración global de pytest y fixtures
├── test_day_journal.py  # Tests para endpoints de day_journal
├── test_trades.py       # Tests para endpoints de trades
├── test_emotions.py     # Tests para endpoints de emotions
├── test_confirmations.py # Tests para endpoints de confirmations
└── README.md            # Este archivo
```

## Instalación de Dependencias

Primero, asegúrate de tener instaladas las dependencias de testing:

```bash
cd API
pip install -r requirements.txt
```

Las dependencias de testing incluyen:
- `pytest`: Framework de testing
- `pytest-asyncio`: Soporte para tests asíncronos
- `httpx`: Cliente HTTP para testing de FastAPI
- `pytest-mock`: Utilidades para mocking

## Ejecutar los Tests

### Ejecutar todos los tests

```bash
cd API
pytest
```

### Ejecutar tests con más verbosidad

```bash
pytest -v
```

### Ejecutar un archivo de test específico

```bash
pytest tests/test_day_journal.py
```

### Ejecutar una clase de test específica

```bash
pytest tests/test_day_journal.py::TestDayJournalRoutes
```

### Ejecutar un test específico

```bash
pytest tests/test_day_journal.py::TestDayJournalRoutes::test_get_all_day_journals
```

### Ejecutar tests con cobertura

```bash
# Primero instala pytest-cov
pip install pytest-cov

# Luego ejecuta con cobertura
pytest --cov=app --cov-report=html
```

## Estructura de los Tests

Cada archivo de test sigue una estructura similar:

1. **Imports**: Importación de librerías necesarias
2. **Clase de Test**: Clase que agrupa tests relacionados
3. **Métodos de Test**: Cada método testea un caso específico

### Ejemplo de Test

```python
@patch('app.routes.day_journal.day_journal_service')
def test_get_all_day_journals(self, mock_service, client):
    """Test para obtener todos los day_journals"""
    # Arrange: Preparar datos mock
    mock_data = [{'id': '1', 'date': '2024-01-15'}]
    mock_service.get_all.return_value = mock_data
    
    # Act: Ejecutar la acción
    response = client.get("/day-journal/")
    
    # Assert: Verificar resultados
    assert response.status_code == 200
    assert len(response.json()) == 1
```

## Fixtures Disponibles

El archivo `conftest.py` proporciona las siguientes fixtures:

- `mock_database_service`: Servicio de base de datos mock
- `day_journal_service_mock`: Servicio de day_journal con mock
- `trade_service_mock`: Servicio de trades con mock
- `emotion_service_mock`: Servicio de emotions con mock
- `confirmation_service_mock`: Servicio de confirmations con mock
- `app`: Instancia de FastAPI para testing
- `client`: TestClient de FastAPI

## Cobertura de Tests

Los tests cubren los siguientes endpoints:

### Day Journal
- ✅ GET `/day-journal/` - Listar todos
- ✅ GET `/day-journal` - Listar (sin barra)
- ✅ GET `/day-journal/{id}` - Obtener por ID
- ✅ GET `/day-journal/range` - Obtener por rango de fechas
- ✅ POST `/day-journal/` - Crear
- ✅ PUT `/day-journal/{id}` - Actualizar
- ✅ DELETE `/day-journal/{id}` - Eliminar

### Trades
- ✅ GET `/trades/` - Listar todos
- ✅ GET `/trades/{id}` - Obtener por ID
- ✅ POST `/trades/` - Crear
- ✅ PUT `/trades/{id}` - Actualizar
- ✅ DELETE `/trades/{id}` - Eliminar
- ✅ GET `/trades/stats/summary` - Estadísticas

### Emotions
- ✅ GET `/emotions/` - Listar todos
- ✅ POST `/emotions/` - Crear
- ✅ DELETE `/emotions/{id}` - Eliminar

### Confirmations
- ✅ GET `/confirmations/` - Listar todos
- ✅ POST `/confirmations/` - Crear
- ✅ DELETE `/confirmations/{id}` - Eliminar

## Casos de Prueba Cubiertos

Para cada endpoint, los tests cubren:

1. **Casos exitosos**: Cuando la operación se completa correctamente
2. **Casos de error**: Cuando no se encuentra el recurso (404)
3. **Validación**: Cuando los datos no son válidos (422)
4. **Paginación**: Para endpoints que la soportan
5. **Conversión de datos**: Verificación de conversión de fechas y otros tipos

## Notas Importantes

1. **Mocks**: Los tests usan mocks para evitar dependencias reales de Firebase
2. **Aislamiento**: Cada test es independiente y no afecta a otros
3. **Limpieza**: Los fixtures aseguran un estado limpio antes de cada test
4. **Variables de Entorno**: Los tests usan `ENV=test` para configuración específica

## Troubleshooting

### Error: "Module not found"
Asegúrate de estar en el directorio `API` y que todas las dependencias estén instaladas.

### Error: "Import error"
Verifica que el path del proyecto esté correctamente configurado en `conftest.py`.

### Error: "TestClient not found"
Asegúrate de tener instalada la versión correcta de FastAPI y que `httpx` esté en las dependencias.

## Agregar Nuevos Tests

Para agregar nuevos tests:

1. Crea un nuevo archivo `test_<nombre>.py` en el directorio `tests/`
2. Importa las fixtures necesarias de `conftest.py`
3. Crea una clase `Test<Nombre>Routes`
4. Agrega métodos `test_<caso>` para cada caso de prueba
5. Usa `@patch` para mockear servicios externos

Ejemplo:

```python
from unittest.mock import patch
from tests.conftest import client

class TestNewRoutes:
    @patch('app.routes.new.new_service')
    def test_new_endpoint(self, mock_service, client):
        mock_service.method.return_value = {}
        response = client.get("/new/")
        assert response.status_code == 200
```

