<template>
  <div class="app-bg min-h-screen">
    <nav class="navbar fixed top-0 left-0 right-0 z-10">
      <div class="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <h1 class="title-glow text-xl font-bold tracking-wide">SinXa</h1>
          <button 
            @click="handleExport"
            :disabled="isExporting"
            class="btn-export w-8 h-8 rounded-full flex items-center justify-center transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Exportar datos"
            aria-label="Exportar datos"
          >
            <svg v-if="!isExporting" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </button>
        </div>
        <div class="flex items-center gap-3">
          <span class="badge badge-live metric-mono">LIVE</span>
        </div>
      </div>
    </nav>

    <main class="mx-auto max-w-7xl px-6 pt-28 pb-12">
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
          <h2 class="heading-lg title-glow">Trades</h2>
          <button class="btn-primary" @click="handleNewTrade">Log Trade</button>
        </div>

        <div v-if="loading" class="text-white/70 mt-6">Cargando trades...</div>
        <div v-else-if="error" class="text-red-400 mt-6">{{ error }}</div>
        <TradeList 
          v-else 
          class="mt-6" 
          :trades="trades" 
          @edit="handleEditTrade"
        />
      </section>
      
      <Modal v-model="showLogModal" :title="editingTrade ? 'Editar Trade' : 'Nuevo Trade'">
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
import { getTrades, createTrade, updateTrade, getTradeStatsSummary, exportAllData } from './api'
import { useOptionsStore } from './stores/optionsStore'

const showLogModal = ref(false)
const editingTrade = ref(null)
const trades = ref([])
const stats = ref({ total_pnl: 0, avg_pnl: 0, total_trades: 0, win_rate: 0 })
const loading = ref(false)
const error = ref('')
const optionsStore = useOptionsStore()
const username = ref('Usuario')
const isExporting = ref(false)

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
    
    // Actualizar la lista de trades en segundo plano
    refreshTrades().catch(e => {
      console.error('Error refreshing trades:', e)
      error.value = 'Error actualizando la lista de trades: ' + (e?.message || String(e))
    })
    
    // Actualizar estadísticas en segundo plano
    refreshStats().catch(e => console.error('Error refreshing stats:', e))
    
  } catch (e) {
    console.error('Error in handleSubmit:', e)
    // Mostrar error al usuario si algo falla
    error.value = 'Error ' + (wasEditing ? 'actualizando' : 'creando') + ' el trade: ' + (e?.message || String(e))
  } finally {
    loading.value = false
  }
}

async function handleExport() {
  if (isExporting.value) return
  
  try {
    isExporting.value = true
    error.value = ''
    
    const data = await exportAllData()
    
    // Crear un blob con los datos JSON
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    
    // Crear un enlace temporal para descargar
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    
    // Nombre del archivo con la fecha actual
    const date = new Date().toISOString().split('T')[0]
    link.download = `trade-journal-export-${date}.json`
    
    // Trigger download
    document.body.appendChild(link)
    link.click()
    
    // Cleanup
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
  } catch (e) {
    console.error('Error exporting data:', e)
    error.value = 'Error al exportar los datos: ' + (e?.message || String(e))
  } finally {
    isExporting.value = false
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

