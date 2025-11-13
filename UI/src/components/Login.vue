<template>
  <div class="min-h-screen login-bg flex items-center justify-center p-6">
    <div class="login-container">
      <!-- Left side - Image -->
      <div class="login-image">
        <div class="login-image-content">
          <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
            <!-- Background gradient -->
            <defs>
              <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:rgba(212, 173, 252, 0.1);stop-opacity:1" />
                <stop offset="100%" style="stop-color:rgba(255, 220, 190, 0.05);stop-opacity:1" />
              </linearGradient>
              <linearGradient id="chartGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:rgba(212, 173, 252, 0.8);stop-opacity:1" />
                <stop offset="100%" style="stop-color:rgba(212, 173, 252, 0.1);stop-opacity:1" />
              </linearGradient>
            </defs>
            
            <!-- Grid pattern -->
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(212, 173, 252, 0.08)" stroke-width="1"/>
            </pattern>
            <rect width="600" height="600" fill="url(#grid)" />
            
            <!-- Chart/candlestick abstract representation -->
            <g transform="translate(150, 100)">
              <!-- Candlesticks -->
              <rect x="40" y="100" width="20" height="120" fill="rgba(34, 197, 94, 0.6)" rx="4"/>
              <rect x="100" y="60" width="20" height="160" fill="rgba(34, 197, 94, 0.6)" rx="4"/>
              <rect x="160" y="140" width="20" height="80" fill="rgba(239, 68, 68, 0.6)" rx="4"/>
              <rect x="220" y="80" width="20" height="140" fill="rgba(34, 197, 94, 0.6)" rx="4"/>
              <rect x="280" y="180" width="20" height="40" fill="rgba(239, 68, 68, 0.6)" rx="4"/>
              
              <!-- Chart line -->
              <path d="M 50 160 Q 80 160 90 120 T 130 80 T 170 140 T 230 100 T 290 180" 
                    fill="none" 
                    stroke="rgba(212, 173, 252, 0.8)" 
                    stroke-width="4"
                    filter="url(#glow)"/>
              
              <!-- Gradient area under line -->
              <path d="M 50 160 Q 80 160 90 120 T 130 80 T 170 140 T 230 100 T 290 180 L 290 300 L 50 300 Z" 
                    fill="url(#chartGradient)"
                    opacity="0.3"/>
            </g>
            
            <!-- Glow filter -->
            <defs>
              <filter id="glow">
                <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
                <feMerge>
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>
            
            <!-- Floating particles -->
            <circle cx="120" cy="320" r="4" fill="rgba(212, 173, 252, 0.6)" opacity="0.8">
              <animate attributeName="cy" values="320;300;320" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="480" cy="280" r="5" fill="rgba(255, 220, 190, 0.6)" opacity="0.7">
              <animate attributeName="cy" values="280;260;280" dur="4s" repeatCount="indefinite"/>
            </circle>
            <circle cx="400" cy="380" r="3" fill="rgba(242, 190, 255, 0.6)" opacity="0.8">
              <animate attributeName="cy" values="380;360;380" dur="3.5s" repeatCount="indefinite"/>
            </circle>
          </svg>
        </div>
        <div class="login-image-overlay">
          <h2 class="text-2xl font-bold text-white mb-3">Registra tus operaciones</h2>
          <p class="text-white/70 text-lg">Analiza tu rendimiento y optimiza tu estrategia</p>
        </div>
      </div>

      <!-- Right side - Login Form -->
      <div class="login-form">
        <div class="text-center mb-8">
          <div class="inline-block mb-4">
            <div class="w-16 h-16 bg-gradient-to-br from-accent-cyan to-purple-500 rounded-2xl flex items-center justify-center mb-3 mx-auto shadow-lg shadow-cyan-500/20">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <h1 class="title-glow text-4xl font-bold mb-2">Trade Journal</h1>
        </div>

        <div class="space-y-6">
          <div class="text-center">
            <p class="text-white/90 text-lg">Bienvenido</p>
            <p class="text-white/60 text-sm mt-1">Accede a tu panel de control</p>
          </div>

          <button
            @click="handleLogin"
            :disabled="loading"
            class="btn-login w-full flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <svg v-if="!loading" class="w-5 h-5" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <svg v-else class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="font-semibold">{{ loading ? 'Conectando...' : 'Continuar con Google' }}</span>
          </button>

          <div v-if="error" class="bg-red-500/20 border border-red-500/50 rounded-lg p-4 animate-fade-in">
            <p class="text-red-300 text-sm">{{ error }}</p>
          </div>

          <div class="text-center text-sm text-white/40 pt-4">
            <p>Al continuar, aceptas nuestros términos de servicio</p>
          </div>

          <!-- Botón Demo - Discreto -->
          <div class="text-center pt-2">
            <button
              @click="handleDemoLogin"
              :disabled="loading"
              class="text-white/40 hover:text-white/60 text-xs underline transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              type="button"
            >
              Modo demo
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')

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
  
  return 'No se pudo iniciar sesión. Por favor intenta nuevamente.'
}

async function handleLogin() {
  try {
    loading.value = true
    error.value = ''
    await authStore.login()
    
    // Redirigir al dashboard
    router.push('/dashboard')
  } catch (err) {
    console.error('Error en login:', err)
    error.value = getErrorMessage(err)
  } finally {
    loading.value = false
  }
}

async function handleDemoLogin() {
  try {
    loading.value = true
    error.value = ''
    authStore.demoLogin()
    
    // Redirigir al dashboard
    router.push('/dashboard')
  } catch (err) {
    console.error('Error en demo login:', err)
    error.value = 'Error al iniciar modo demo'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Login Background */
.login-bg {
  background:
    radial-gradient(1200px 800px at 20% 30%, rgba(212, 173, 252, 0.15), transparent 60%),
    radial-gradient(1000px 600px at 80% 70%, rgba(255, 220, 190, 0.1), transparent 50%),
    radial-gradient(800px 500px at 50% 50%, rgba(242, 190, 255, 0.08), transparent 40%),
    linear-gradient(135deg, rgb(12, 16, 26) 0%, rgb(18, 24, 36) 50%, rgb(12, 16, 26) 100%);
}

/* Login Container - Split Layout */
.login-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  max-width: 1200px;
  width: 100%;
  min-height: 650px;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08);
  background: linear-gradient(180deg, rgb(22, 30, 46) 0%, rgb(28, 40, 60) 100%);
}

/* Left Side - Image */
.login-image {
  position: relative;
  background: linear-gradient(135deg, rgba(212, 173, 252, 0.08), rgba(170, 135, 245, 0.05));
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.login-image::before {
  content: '';
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(circle at 30% 40%, rgba(212, 173, 252, 0.1), transparent 50%),
    radial-gradient(circle at 70% 60%, rgba(255, 220, 190, 0.08), transparent 50%);
  opacity: 0.6;
}

.login-image-content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-image-content svg {
  width: 90%;
  height: auto;
  max-width: 500px;
  filter: drop-shadow(0 0 40px rgba(212, 173, 252, 0.15));
}

.login-image-overlay {
  position: absolute;
  bottom: 40px;
  left: 40px;
  right: 40px;
  z-index: 2;
  text-align: center;
  background: rgba(12, 16, 26, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

/* Right Side - Form */
.login-form {
  padding: 60px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;
}

.login-form::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 100% 0%, rgba(212, 173, 252, 0.05), transparent 60%),
    radial-gradient(circle at 0% 100%, rgba(255, 220, 190, 0.03), transparent 60%);
  opacity: 0.5;
  pointer-events: none;
}

.login-form > * {
  position: relative;
  z-index: 1;
}

/* Login Button */
.btn-login {
  background: linear-gradient(135deg, rgba(212, 173, 252, 1), rgba(170, 135, 245, 0.92));
  color: #0f0f17;
  padding: 16px 32px;
  border-radius: 14px;
  border: 1px solid rgba(212, 173, 252, 0.5);
  box-shadow: 0 8px 24px rgba(212, 173, 252, 0.25);
  transition: all 0.3s ease;
  font-weight: 600;
}

.btn-login:hover:not(:disabled) {
  filter: brightness(1.08);
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(212, 173, 252, 0.35);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
}

/* Animated icon wrapper */
.btn-login svg {
  transition: transform 0.3s ease;
}

.btn-login:hover svg:not(.animate-spin) {
  transform: scale(1.1);
}

/* Fade in animation */
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .login-container {
    grid-template-columns: 1fr;
    max-width: 500px;
    min-height: auto;
  }
  
  .login-image {
    display: none;
  }
  
  .login-form {
    padding: 50px 40px;
  }
}

@media (max-width: 640px) {
  .login-bg {
    padding: 0;
  }
  
  .login-container {
    border-radius: 0;
    min-height: 100vh;
  }
  
  .login-form {
    padding: 40px 24px;
  }
  
  .login-image-overlay {
    display: none;
  }
}

/* Accent color utilities */
.from-accent-cyan {
  --tw-gradient-from: rgb(212, 173, 252);
}

.text-white\/90 {
  color: rgba(255, 255, 255, 0.9);
}

.text-white\/70 {
  color: rgba(255, 255, 255, 0.7);
}

.text-white\/60 {
  color: rgba(255, 255, 255, 0.6);
}

.text-white\/40 {
  color: rgba(255, 255, 255, 0.4);
}
</style>

