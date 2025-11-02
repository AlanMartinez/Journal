<template>
  <div class="app-bg min-h-screen">
    <!-- Nuevo Navbar Component -->
    <Navbar />

    <main class="mx-auto max-w-7xl px-6 pt-24 pb-12">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
        <!-- Left column - Summary -->
        <div class="lg:col-span-1 h-full">
          <section class="panel p-6 md:p-6 h-full flex flex-col">
            <div class="flex items-start justify-between gap-6">
              <div>
                <h2 class="heading-lg title-glow">Resumen</h2>
                <p class="subtitle mt-1">Rendimiento y métricas clave</p>
              </div>
            </div>
            <div class="flex-grow mt-6">
              <DashboardStats :stats="stats" />
            </div>
          </section>
        </div>

        <!-- Right column - Journal -->
        <div class="lg:col-span-2 h-full">
          <Journal :trades="trades" class="h-full" />
        </div>
      </div>

      <section class="panel p-6 md:p-8 mt-6">
        <div class="flex items-center justify-between">
          <h2 class="heading-lg title-glow">Operaciones</h2>
          <button class="btn-primary" @click="handleNewTrade">Registrar Operación</button>
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
import Navbar from './components/Navbar.vue'

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

