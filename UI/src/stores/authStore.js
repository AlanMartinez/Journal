import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { signInWithPopup, signOut } from 'firebase/auth'
import { auth, googleProvider } from '../firebase/config'
import { exchangeFirebaseToken } from '../api'

export const useAuthStore = defineStore('auth', () => {
  // Estado
  const token = ref(localStorage.getItem('auth_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('auth_user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const currentUser = computed(() => user.value)

  // Helper function to detect connection errors and return generic message
  function getErrorMessage(err) {
    const errorCode = err?.code || ''
    const errorMessage = err?.message || ''
    
    // Detectar errores de conexión de Firebase
    const isConnectionError = 
      errorCode.includes('network') ||
      errorCode.includes('timeout') ||
      errorCode.includes('unavailable') ||
      errorMessage.toLowerCase().includes('network') ||
      errorMessage.toLowerCase().includes('connection') ||
      errorMessage.toLowerCase().includes('fetch') ||
      errorMessage.toLowerCase().includes('timeout') ||
      errorMessage.toLowerCase().includes('failed to fetch')
    
    if (isConnectionError) {
      return 'Error de conexión. Verifica tu internet e intenta nuevamente.'
    }
    
    return err.message || 'No se pudo iniciar sesión'
  }

  // Actions
  async function login() {
    try {
      loading.value = true
      error.value = null

      // Paso 1: Iniciar sesión con Firebase
      const result = await signInWithPopup(auth, googleProvider)
      const firebaseIdToken = await result.user.getIdToken()

      // Paso 2: Enviar token a la API para intercambio
      const response = await exchangeFirebaseToken(firebaseIdToken)
      
      // Paso 3: Guardar token y usuario
      token.value = response.access_token
      user.value = response.user

      // Paso 4: Persistir en localStorage
      localStorage.setItem('auth_token', response.access_token)
      localStorage.setItem('auth_user', JSON.stringify(response.user))

      return { success: true, user: response.user }
    } catch (err) {
      console.error('Error en login:', err)
      error.value = getErrorMessage(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      loading.value = true
      
      // Verificar si es modo demo
      const isDemoMode = localStorage.getItem('demo_mode') === 'true'
      
      // Cerrar sesión en Firebase solo si no es modo demo
      if (!isDemoMode) {
        await signOut(auth)
      }
      
      // Limpiar estado local
      token.value = null
      user.value = null
      
      // Limpiar localStorage
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
      localStorage.removeItem('demo_mode')
    } catch (err) {
      console.error('Error en logout:', err)
      error.value = err.message || 'Error al cerrar sesión'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Modo demo: login sin Firebase usando datos mock
  function demoLogin() {
    try {
      loading.value = true
      error.value = null

      // Crear token y usuario demo
      const demoToken = 'demo_token_' + Date.now()
      const demoUser = {
        id: 'demo_user',
        name: 'Usuario Demo',
        email: 'demo@tradejournal.com',
        picture: null
      }

      // Guardar en estado
      token.value = demoToken
      user.value = demoUser

      // Persistir en localStorage
      localStorage.setItem('auth_token', demoToken)
      localStorage.setItem('auth_user', JSON.stringify(demoUser))
      localStorage.setItem('demo_mode', 'true')

      return { success: true, user: demoUser }
    } catch (err) {
      console.error('Error en demo login:', err)
      error.value = 'Error al iniciar modo demo'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  // Cargar datos desde localStorage al iniciar
  function loadFromStorage() {
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('auth_user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      user.value = JSON.parse(storedUser)
    }
  }

  return {
    // Estado
    token,
    user,
    loading,
    error,
    // Getters
    isAuthenticated,
    currentUser,
    // Actions
    login,
    logout,
    demoLogin,
    clearError,
    loadFromStorage
  }
})

