<template>
  <div class="app-bg min-h-screen">
    <main class="dashboard-container px-6 pt-12 pb-12">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 items-stretch">
        <!-- Left column - Summary -->
        <div class="lg:col-span-1 flex">
          <section class="panel p-4 flex flex-col w-full">
            <div class="flex items-center justify-between gap-6 mb-4">
              <div>
                <h2 class="heading-lg title-glow">Resumen</h2>
                <p class="subtitle mt-1 text-sm">Rendimiento y métricas clave</p>
              </div>
              <button 
                class="trade-button" 
                @click="handleNewTrade"
                title="Registrar Operación"
                aria-label="Registrar Operación"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </button>
            </div>
            <DashboardStats :stats="stats" />
          </section>
        </div>

        <!-- Right column - Journal -->
        <div class="lg:col-span-2 flex">
          <Journal :trades="trades" class="w-full" />
        </div>
      </div>

      <section class="panel p-6 md:p-8 mt-4">
        <div class="flex items-center justify-between">
          <h2 class="heading-lg title-glow">Operaciones</h2>
        </div>

        <div v-if="loading" class="text-white/70 mt-6">Cargando operaciones...</div>
        <div v-else-if="error" class="text-red-400 mt-6">{{ error }}</div>
        <TradeList 
          v-else 
          class="mt-6" 
          :trades="trades" 
          @edit="handleEditTrade"
        />
      </section>
      
      <Modal v-model="showLogModal" :title="editingTrade ? 'Editar Operación' : 'Nueva Operación'">
        <TradeForm 
          :initial-data="editingTrade"
          @cancel="cancelEdit"
          @submit="handleSubmit" 
        />
      </Modal>
    </main>
  </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import TradeList from './components/TradeList.vue'
import TradeForm from './components/TradeForm.vue'
import DashboardStats from './components/DashboardStats.vue'
import Journal from './components/Journal.vue'
import Modal from './components/Modal.vue'

// Register components
const components = {
  TradeList,
  TradeForm,
  DashboardStats,
  Journal,
  Modal
}
import { getTrades, createTrade, updateTrade, getTradeStatsSummary } from './api'
import { useOptionsStore } from './stores/optionsStore'
import { useAuthStore } from './stores/authStore'

const showLogModal = ref(false)
const editingTrade = ref(null)
const trades = ref([])
const stats = ref({ total_pnl: 0, avg_pnl: 0, total_trades: 0, win_rate: 0 })
const loading = ref(false)
const error = ref('')
const optionsStore = useOptionsStore()
const authStore = useAuthStore()

const user = authStore.currentUser

async function refreshTrades() {
  try {
    loading.value = true
    error.value = ''
    const data = await getTrades()
    trades.value = Array.isArray(data) ? data : []
  } catch (e) {
    error.value = e?.message || String(e)
  } finally {
    loading.value = false
  }
}

async function refreshStats() {
  try {
    const data = await getTradeStatsSummary()
    stats.value = data || { total_pnl: 0, avg_pnl: 0, total_trades: 0, win_rate: 0 }
  } catch (_) {
    // ignore error
  }
}

function formatMoney(n) {
  const v = Number(n) || 0
  const sign = v >= 0 ? '' : '-'
  const abs = Math.abs(v).toFixed(2)
  return `${sign}$${abs}`
}

async function handleEditTrade(trade) {
  editingTrade.value = { ...trade }
  showLogModal.value = true
}

function handleNewTrade() {
  editingTrade.value = null
  showLogModal.value = true
}

function cancelEdit() {
  editingTrade.value = null
  showLogModal.value = false
}

async function handleSubmit(payload) {
  loading.value = true
  error.value = ''
  
  // Guardar el ID del trade antes de limpiar
  const tradeId = editingTrade.value?.id
  const wasEditing = !!tradeId
  
  // Cerrar el modal inmediatamente
  cancelEdit()
  
  try {
    if (wasEditing && tradeId) {
      // Create a clean payload for update, excluding the date if it hasn't changed
      const updatePayload = { ...payload }
      
      // If the date hasn't changed, remove it from the payload
      if (updatePayload.date === payload.date) {
        delete updatePayload.date
      }
      
      console.log('Updating trade with payload:', { id: tradeId, ...updatePayload })
      await updateTrade(tradeId, updatePayload)
      console.log('Update successful')
    } else {
      console.log('Creating new trade:', payload)
      await createTrade(payload)
    }
    
    // Actualizar la lista de operaciones en segundo plano
    refreshTrades().catch(e => {
      console.error('Error refreshing trades:', e)
      error.value = 'Error actualizando la lista de operaciones: ' + (e?.message || String(e))
    })
    
    // Actualizar estadísticas en segundo plano
    refreshStats().catch(e => console.error('Error refreshing stats:', e))
    
  } catch (e) {
    console.error('Error in handleSubmit:', e)
    // Mostrar error al usuario si algo falla
    error.value = 'Error ' + (wasEditing ? 'actualizando' : 'creando') + ' la operación: ' + (e?.message || String(e))
  } finally {
    loading.value = false
  }
}


onMounted(async () => {
  await Promise.all([
    optionsStore.loadAll(),
    refreshTrades(),
    refreshStats(),
  ])
})
</script>

<style scoped>
.dashboard-container {
  max-width: 100%;
  width: 100%;
}

.trade-button {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(var(--accent-cyan) / 1), rgba(170, 135, 245, 0.92));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0f0f17;
  box-shadow: 0 6px 20px rgba(var(--accent-cyan) / 0.3);
  border: 2px solid rgba(var(--accent-cyan) / 0.4);
  flex-shrink: 0;
  transition: all 0.2s ease;
  user-select: none;
  cursor: pointer;
}

.trade-button:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(var(--accent-cyan) / 0.4);
}

.trade-button:active {
  transform: scale(0.98);
}
</style>

