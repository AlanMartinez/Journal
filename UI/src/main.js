import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import AppWrapper from './AppWrapper.vue'
import router from './router'
import { useAuthStore } from './stores/authStore'

// Inicializar Pinia
const pinia = createPinia()

// Inicializar App
const app = createApp(AppWrapper)
app.use(pinia)
app.use(router)

app.mount('#app')

// Cargar datos de autenticación desde localStorage después de montar
const authStore = useAuthStore()
authStore.loadFromStorage()
