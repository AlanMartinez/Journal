# TradeJournal API - Complete Trading Journal System

API REST completa desarrollada con FastAPI para la gestión integral de un journal de trading. Incluye trades, emotions, confirmations y persistencia con Firebase Firestore siguiendo principios SOLID.

## 🏗️ Arquitectura SOLID

✅ **Single Responsibility**: Cada clase tiene una única responsabilidad
✅ **Open/Closed**: Interfaces abstractas permiten extensión sin modificación
✅ **Liskov Substitution**: Servicios intercambiables mediante interfaces
✅ **Interface Segregation**: Interfaces específicas para cada servicio
✅ **Dependency Inversion**: Inyección de dependencias en lugar de instanciación directa

```
API/
├── main.py              # Servidor FastAPI + configuración
├── config.py            # Configuración centralizada con env vars
├── setup.py             # Script de configuración general
├── firebase_setup.py    # Script específico para Firebase
├── check_firebase.py   # Script de verificación de Firebase
├── requirements.txt     # Dependencias
├── .env.example         # Variables de entorno ejemplo
├── firebase-credentials.json  # Credenciales Firebase (generar)
├── app/
│   ├── models/
│   │   ├── __init__.py        # Importación de modelos
│   │   ├── trade.py          # Modelos Pydantic para trades
│   │   ├── emotion.py        # Modelos Pydantic para emotions
│   │   └── confirmation.py   # Modelos Pydantic para confirmations
│   ├── services/
│   │   ├── __init__.py        # Importación de servicios
│   │   ├── database_service.py    # Interfaz abstracta SOLID
│   │   ├── firebase_service.py   # Implementación Firebase
│   │   ├── trade_service.py      # Lógica negocio trades
│   │   ├── emotion_service.py    # Lógica negocio emotions
│   │   └── confirmation_service.py  # Lógica negocio confirmations
│   └── routes/
│       ├── __init__.py        # Importación de routers
│       ├── trades.py         # Endpoints REST trades
│       ├── emotions.py       # Endpoints REST emotions
│       └── confirmations.py  # Endpoints REST confirmations
└── README.md            # Documentación completa

## 🚀 Instalación y Configuración

### 1. Dependencias
```bash
cd API
pip install -r requirements.txt
```

### 2. Configuración Automática
```bash

⚠️ **IMPORTANTE**: Necesitas **credenciales de servidor** (Service Account), no las configuraciones del cliente web.

#### Configuración Automática
```bash
python firebase_setup.py
```

Este script te guiará paso a paso y abrirá Firebase Console automáticamente.

#### Verificar Configuración
```bash
python check_firebase.py
```

Este script verifica que las credenciales estén correctas y prueba la conexión.

1. **Ve a Firebase Console**:
   - 🌐 https://console.firebase.google.com/project/tradejournal-9075d/settings/serviceaccounts/adminsdk

2. **Genera Service Account Key**:
   - En la sección "Service accounts"
   - Haz clic en "Generate new private key"
   - Descarga el archivo JSON

3. **Configura las credenciales**:
   - Renombra el archivo descargado a: `firebase-credentials.json`
   - Colócalo en la carpeta `API/`

4. **Verifica configuración**:
   ```bash
   python firebase_setup.py
   ```

#### Opciones de Configuración

**Opción A: Archivo de Credenciales** (Recomendado)
- Coloca `firebase-credentials.json` en la carpeta `API/`

**Opción B: Variables de Entorno**
```bash
export FIREBASE_PROJECT_ID="tradejournal-9075d"
export FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."
export FIREBASE_DATABASE_ID="journal-db"  # Opcional, nombre de la BD
# ... otras variables (ver .env.example)
```

**Opción C: Configuración en config.py**
```python
FIREBASE_CONFIG = {
    "projectId": "tradejournal-9075d",
    # ... configuración completa
}
FIREBASE_DATABASE_ID = "journal-db"  # Nombre de la base de datos Firestore
```

### Crear Base de Datos en Firebase Console

Si usas un `database_id` específico (como "journal-db"):

1. **Ve a Firebase Console**: https://console.firebase.google.com/project/tradejournal-9075d/firestore
2. **Haz clic en "Crear base de datos"** o selecciona una existente
3. **En la pestaña "Datos"**, puedes crear múltiples bases de datos
4. **El database_id** es el nombre que aparece en la URL o que configuras

**Nota**: Si no especificas `database_id`, Firebase usa la base de datos por defecto "(default)".

#### Verificar Configuración
```bash
python check_firebase.py
```

Este script verifica que las credenciales estén correctas y prueba la conexión.

### 4. Ejecutar
```bash
python run.py
```

### 5. Acceder
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

## 📋 Endpoints Disponibles

### Trades CRUD
- `GET /trades` - Listar trades (ordenados por fecha)
- `GET /trades/{id}` - Obtener trade específico
- `POST /trades` - Crear trade (con validación)
- `PUT /trades/{id}` - Actualizar trade
- `DELETE /trades/{id}` - Eliminar trade

### Emotions
- `GET /emotions` - Obtener todas las emotions
- `POST /emotions` - Crear nueva emotion
- `DELETE /emotions/{id}` - Eliminar emotion

### Confirmations
- `GET /confirmations` - Obtener todas las confirmations
- `POST /confirmations` - Crear nueva confirmation
- `DELETE /confirmations/{id}` - Eliminar confirmation

### Utilidades
- `GET /` - Información de la API
- `GET /echo` - Endpoint de prueba

## 💾 Modelo de Trade

```json
{
  "symbol": "str",           // Símbolo (NQ, ES, YM, etc.)
  "side": "str",             // 'buy' | 'sell'
  "date": "date",            // Fecha del trade (YYYY-MM-DD)
  "rate": "float",           // Porcentaje de rate
  "risk": "float | null",    // Riesgo en R
  "result": "float | null",  // Resultado en dinero
  "status": "str | null",    // 'TP' | 'SL' | 'BE'
  "notes": "str | null",     // Notas del trade
  "emotions": ["str"],       // Lista de emociones
  "confirmations": ["str"],  // Lista de confirmaciones
  "trading_link": "str | null"  // Link del trade
}
```

## 💾 Modelos de Datos

### Emotion
```json
{
  "id": "str",              // ID único de la emotion
  "name": "str",            // Nombre de la emoción
  "description": "str | null"  // Descripción opcional
}
```

### Confirmation
```json
{
  "id": "str",              // ID único de la confirmation
  "name": "str",            // Nombre de la confirmación
  "description": "str | null"  // Descripción opcional
}
```

## 🔧 Características SOLID

### Single Responsibility Principle (SRP)
- `DatabaseService`: Solo maneja operaciones de base de datos
- `TradeService`: Solo maneja lógica de negocio de trades
- `FirebaseService`: Solo maneja conexión con Firebase

### Open/Closed Principle (OCP)
- Interfaces abstractas permiten agregar nuevas implementaciones de BD
- Sin modificar código existente, se puede cambiar a PostgreSQL, MongoDB, etc.

### Liskov Substitution Principle (LSP)
- Cualquier implementación de `DatabaseService` es intercambiable
- El `TradeService` funciona igual sin importar la BD subyacente

### Interface Segregation Principle (ISP)
- `DatabaseService` tiene solo métodos necesarios
- Interfaces pequeñas y específicas

### Dependency Inversion Principle (DIP)
- `TradeService` depende de abstracción (`DatabaseService`)
- No depende de implementación concreta (`FirebaseService`)

## 📊 Ejemplos de Uso

### Crear trade con emotions y confirmations:

```bash
curl -X POST "http://localhost:8000/trades" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "NQ",
       "side": "buy",
       "date": "2025-10-25",
       "rate": 0.5,
       "risk": 1.0,
       "result": 250.0,
       "status": "TP",
       "notes": "Trade exitoso con múltiples confirmaciones",
       "emotions": ["Confianza", "Calma"],
       "confirmations": ["FVG", "OB", "CISD"],
       "trading_link": "https://example.com/trade/123"
     }'
```

## 🎯 Flujo Frontend: Asociar Emotions y Confirmations

### 📝 **Cómo funciona la asociación:**

Cuando creas un trade, los campos `emotions` y `confirmations` son **arrays de strings** (nombres), no IDs:

```json
{
  "emotions": ["Confianza", "Calma"],
  "confirmations": ["FVG", "OB", "CISD"]
}
```

### 🔄 **Flujo completo desde el frontend:**

#### 1. **Cargar opciones para dropdowns/checkboxes:**
```javascript
// En tu componente Vue.js
const emotions = await fetch('/emotions').then(r => r.json())
const confirmations = await fetch('/confirmations').then(r => r.json())

// emotions = [{id: "...", name: "Confianza", description: "..."}, ...]
// confirmations = [{id: "...", name: "FVG", description: "..."}, ...]
```

#### 2. **Crear el trade con los nombres seleccionados:**
```javascript
const tradeData = {
  symbol: "NQ",
  side: "buy",
  date: "2025-10-25",
  rate: 0.5,
  risk: 1.0,
  result: 250.0,
  status: "TP",
  notes: "Trade exitoso",
  emotions: ["Confianza", "Calma"],        // ← Nombres de emotions
  confirmations: ["FVG", "OB"],             // ← Nombres de confirmations
  trading_link: "https://example.com/trade"
}

await fetch('/trades', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(tradeData)
})
```

### 📋 **Ejemplo completo con curl:**

```bash
# 1. Crear emotions disponibles
curl -X POST "http://localhost:8000/emotions" \
     -H "Content-Type: application/json" \
     -d '{"name": "Confianza", "description": "Sentimiento de seguridad"}'

# 2. Crear confirmations disponibles  
curl -X POST "http://localhost:8000/confirmations" \
     -H "Content-Type: application/json" \
     -d '{"name": "FVG", "description": "Fair Value Gap"}'

# 3. Crear trade usando los nombres
curl -X POST "http://localhost:8000/trades" \
     -H "Content-Type: application/json" \
     -d '{
       "symbol": "NQ",
       "side": "buy", 
       "date": "2025-10-25",
       "rate": 0.5,
       "emotions": ["Confianza"],
       "confirmations": ["FVG"],
       "result": 250.0,
       "status": "TP"
     }'
```

### 🎯 **Respuesta del trade creado:**
```json
{
  "id": "bXHeXVdjVDtM7XdodLwu",
  "symbol": "NQ",
  "side": "buy",
  "date": "2025-10-25", 
  "rate": 0.5,
  "emotions": ["Confianza"],
  "confirmations": ["FVG"],
  "result": 250.0,
  "status": "TP",
  "notes": null,
  "risk": null,
  "trading_link": null
}
```

### ✨ **Beneficios de esta aproximación:**
- ✅ **Simple**: Solo enviar nombres, no IDs complejos
- ✅ **Flexible**: Puedes usar emotions/confirmations sin crearlas primero
- ✅ **Escalable**: Fácil agregar nuevas emotions/confirmations
- ✅ **Compatible**: Funciona con tu formulario actual

### Crear confirmations disponibles:

```bash
# Crear confirmation "FVG"
curl -X POST "http://localhost:8000/confirmations" \
     -H "Content-Type: application/json" \
     -d '{"name": "FVG", "description": "Fair Value Gap"}'

# Crear confirmation "OB"
curl -X POST "http://localhost:8000/confirmations" \
     -H "Content-Type: application/json" \
     -d '{"name": "OB", "description": "Order Block"}'
```

### Ver emotions disponibles:

```bash
curl http://localhost:8000/emotions
```

### Ver confirmations disponibles:

```bash
curl http://localhost:8000/confirmations
```

### Obtener trades:
```bash
curl http://localhost:8000/trades
```

### Actualizar trade:
```bash
curl -X PUT "http://localhost:8000/trades/1" \
     -H "Content-Type: application/json" \
     -d '{"result": 300.0, "notes": "Actualizado"}'
```

### Obtener emotions:
```bash
curl http://localhost:8000/emotions
```

### Crear emotion:
```bash
curl -X POST "http://localhost:8000/emotions" \
     -H "Content-Type: application/json" \
     -d '{"name": "Esperanza", "description": "Sentimiento positivo"}'
```

### Obtener confirmations:
```bash
curl http://localhost:8000/confirmations
```

### Crear confirmation:
```bash
curl -X POST "http://localhost:8000/confirmations" \
     -H "Content-Type: application/json" \
     -d '{"name": "POI", "description": "Point of Interest"}'
```

## 🔧 Características SOLID

### Single Responsibility Principle (SRP)
- `DatabaseService`: Solo maneja operaciones de base de datos
- `TradeService`: Solo maneja lógica de negocio de trades
- `EmotionService`: Solo maneja lógica de negocio de emotions
- `ConfirmationService`: Solo maneja lógica de negocio de confirmations
- `FirebaseService`: Solo maneja conexión con Firebase

### Open/Closed Principle (OCP)
- Interfaces abstractas permiten agregar nuevas implementaciones de BD
- Sin modificar código existente, se puede cambiar a PostgreSQL, MongoDB, etc.

### Liskov Substitution Principle (LSP)
- Cualquier implementación de `DatabaseService` es intercambiable
- El sistema funciona igual sin importar la BD subyacente

### Interface Segregation Principle (ISP)
- `DatabaseService` tiene solo métodos necesarios
- Interfaces pequeñas y específicas para cada responsabilidad

### Dependency Inversion Principle (DIP)
- Servicios dependen de abstracciones (`DatabaseService`) no de implementaciones
- Inyección de dependencias permite cambiar Firebase por otra BD sin refactor

## 🔄 Integración con Frontend

La API está lista para conectar con Vue.js:
- ✅ **Datos de ejemplo** incluidos para testing inmediato
- ✅ **CORS configurado** para frontend Vue
- ✅ **Documentación automática** con Swagger UI
- ✅ **Validación de datos** con Pydantic v2
- ✅ **Estadísticas básicas** de rendimiento
- ✅ **Gestión de emotions** y confirmations
- ✅ **Arquitectura modular** y escalable

## 🧪 Testing Rápido

```bash
# Ver información de la API
curl http://localhost:8000/

# Probar endpoint echo
curl http://localhost:8000/echo

# Ver trades guardados en Firebase
curl http://localhost:8000/trades

# Ver emotions
curl http://localhost:8000/emotions

# Ver confirmations
curl http://localhost:8000/confirmations

# Ver estadísticas
curl http://localhost:8000/trades/stats/summary
```

## 🛠️ Versión

- FastAPI 0.115.12 (compatible con Pydantic v2)
- Firebase Admin SDK 6.6.0
- Python 3.11+
