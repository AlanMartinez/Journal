import { initializeApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider } from 'firebase/auth'

// Configuración de Firebase desde variables de entorno
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyCpJyweEx7srvyUKXh5c6_MRWkrl5JdH-A",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "tradejournal-9075d.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "tradejournal-9075d",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "tradejournal-9075d.appspot.com",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "123456789",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:123456789:web:abcdefghijklmnop"
}

// Inicializar Firebase
const app = initializeApp(firebaseConfig)

// Inicializar Auth
export const auth = getAuth(app)

// Configurar proveedor de Google
export const googleProvider = new GoogleAuthProvider()

// Asegurar que siempre se solicite la pantalla de selección de cuenta
googleProvider.setCustomParameters({
  prompt: 'select_account'
})

export default app

