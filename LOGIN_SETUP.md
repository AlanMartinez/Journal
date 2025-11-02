# Módulo de Login con Firebase - Configuración e Instrucciones

## 📋 Resumen

Se ha implementado un módulo completo de Login con Google usando Firebase Authentication, integrado con la API FastAPI. El sistema incluye:

- ✅ Autenticación con Google via Firebase
- ✅ Intercambio de tokens con el backend
- ✅ Protección de rutas con Vue Router
- ✅ Gestión de estado con Pinia
- ✅ Interceptores HTTP para incluir el JWT en todas las requests

## 🚀 Estructura Implementada

### Backend (API)

**Archivo:** `API/app/routes/auth.py`
- Endpoint `/auth/firebase` para intercambiar tokens de Firebase
- Validación de tokens usando Firebase Admin SDK

**Archivo:** `API/main.py`
- Importado y configurado el router de autenticación

### Frontend (UI)

**Archivos de configuración:**
- `UI/src/firebase/config.js` - Configuración de Firebase
- `UI/src/stores/authStore.js` - Store de Pinia para autenticación
- `UI/src/router/index.js` - Configuración de rutas
- `UI/src/api.js` - Agregado interceptor HTTP para incluir JWT
- `UI/src/main.js` - Configurado con Pinia y Router

**Componentes:**
- `UI/src/components/Login.vue` - Componente de login con Google
- `UI/src/AppWrapper.vue` - Wrapper para router-view
- `UI/src/App.vue` - Dashboard con botón de logout

## 🔧 Configuración Requerida

### 1. Obtener Credenciales de Firebase para el Cliente Web

Necesitas obtener la configuración de la aplicación web desde Firebase Console:

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto: `tradejournal-9075d`
3. Ve a Project Settings (⚙️) > General
4. Scroll hasta "Your apps" y selecciona la app web o crea una nueva
5. Copia la configuración que se ve así:

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "tradejournal-9075d.firebaseapp.com",
  projectId: "tradejournal-9075d",
  storageBucket: "tradejournal-9075d.appspot.com",
  messagingSenderId: "...",
  appId: "1:...:web:..."
};
```

### 2. Crear archivo `.env` en `UI/`

Crea un archivo `.env` en el directorio `UI/` con las siguientes variables:

```env
# Firebase Configuration (obtenidas de Firebase Console)
VITE_FIREBASE_API_KEY=tu-api-key-aqui
VITE_FIREBASE_AUTH_DOMAIN=tradejournal-9075d.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=tradejournal-9075d
VITE_FIREBASE_STORAGE_BUCKET=tradejournal-9075d.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=tu-messaging-sender-id
VITE_FIREBASE_APP_ID=tu-app-id

# API Configuration
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Habilitar Google Authentication en Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/project/tradejournal-9075d/authentication)
2. Ve a "Authentication" > "Sign-in method"
3. Habilita "Google" como proveedor de autenticación
4. Configura el Email de soporte y guarda los cambios

### 4. Configurar Dominios Autorizados

Asegúrate de que los dominios de desarrollo estén autorizados:

1. En Firebase Console > Authentication > Settings
2. Scroll hasta "Authorized domains"
3. Verifica que `localhost` esté en la lista
4. Si estás usando un puerto diferente, puedes agregarlo

## 🔐 Flujo de Autenticación

```
1. Usuario hace clic en "Iniciar sesión con Google" en Login.vue
   ↓
2. Firebase muestra popup de Google
   ↓
3. Usuario selecciona cuenta y autoriza
   ↓
4. Firebase devuelve idToken
   ↓
5. Frontend envía idToken al endpoint /auth/firebase
   ↓
6. Backend valida token con Firebase Admin
   ↓
7. Backend devuelve el mismo idToken (que es el JWT)
   ↓
8. Frontend guarda token en localStorage
   ↓
9. Todas las requests futuras incluyen: Authorization: Bearer <token>
   ↓
10. Router redirige a /dashboard
```

## 🧪 Pruebas

### Probar el endpoint de autenticación

```bash
# Iniciar el servidor API
cd API
python run.py

# En otra terminal, prueba el endpoint
curl -X POST http://localhost:8000/auth/firebase \
  -H "Content-Type: application/json" \
  -d '{"id_token": "tu-token-de-firebase-aqui"}'
```

### Probar la UI

```bash
# Iniciar el servidor de desarrollo
cd UI
npm run dev

# Abre http://localhost:5173
# Deberías ver la pantalla de login
```

## 📁 Archivos Modificados/Creados

### Backend
- ✅ `API/app/routes/auth.py` (nuevo)
- ✅ `API/main.py` (modificado)

### Frontend
- ✅ `UI/src/firebase/config.js` (nuevo)
- ✅ `UI/src/stores/authStore.js` (nuevo)
- ✅ `UI/src/router/index.js` (nuevo)
- ✅ `UI/src/components/Login.vue` (nuevo)
- ✅ `UI/src/AppWrapper.vue` (nuevo)
- ✅ `UI/src/main.js` (modificado)
- ✅ `UI/src/api.js` (modificado)
- ✅ `UI/src/App.vue` (modificado)
- ✅ `UI/package.json` (modificado - agregadas dependencias)

## ⚠️ Notas Importantes

1. **Credenciales**: Los valores actuales en `UI/src/firebase/config.js` son placeholders. Debes reemplazarlos con los valores reales de Firebase Console.

2. **Seguridad**: En producción, nunca expongas la `apiKey` de Firebase públicamente (aunque es safe hacerlo en el frontend según las prácticas de Firebase).

3. **Token Refresh**: Los tokens de Firebase expiran. Puede que necesites implementar refresh automático más adelante.

4. **Validación Backend**: Todas las rutas protegidas del backend ya tienen `Depends(get_current_user)` que valida el token.

## 🐛 Troubleshooting

### Error: "Firebase not initialized"
- Verifica que las credenciales en `UI/src/firebase/config.js` sean correctas
- Asegúrate de que el archivo `.env` tenga las variables correctas

### Error: "CORS policy"
- Verifica que `API/config.py` incluya tu origen en `ALLOWED_ORIGINS`
- El puerto por defecto es `http://localhost:5173`

### Error: "Google sign-in disabled"
- Ve a Firebase Console > Authentication > Sign-in method
- Habilita Google como proveedor

### Las requests no incluyen el token
- Verifica que el token se guarde en localStorage: `localStorage.getItem('auth_token')`
- Revisa la consola del navegador para ver errores de autenticación

## 📝 Próximos Pasos Sugeridos

1. ✅ Implementar refresh automático de tokens
2. ✅ Agregar manejo de errores más robusto
3. ✅ Agregar middleware para refresh de tokens en el interceptor HTTP
4. ✅ Implementar "Remember me" functionality
5. ✅ Agregar tests unitarios para authStore
6. ✅ Implementar protección de rutas más granular en el backend

## 📚 Referencias

- [Firebase Authentication Docs](https://firebase.google.com/docs/auth)
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup)
- [Pinia Documentation](https://pinia.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)

