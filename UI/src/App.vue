<template>
  <div class="app-bg min-h-screen">
    <nav class="navbar fixed top-0 left-0 right-0 z-10">
      <div class="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
        <h1 class="title-glow text-xl font-bold tracking-wide">SinXa</h1>
        <div class="flex items-center gap-3">
          <span class="badge badge-live metric-mono">LIVE</span>
        </div>
      </div>
    </nav>

    <main class="mx-auto max-w-6xl px-6 pt-28 pb-12">
      <section class="panel p-6 md:p-8 mt-6">
        <div class="flex items-center justify-between">
          <h2 class="heading-lg title-glow">Trades</h2>
          <button class="btn-primary" @click="showLogModal = true">Log Trade</button>
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

      <section class="panel p-6 md:p-8 mt-10">
        <div class="flex items-start justify-between gap-6">
          <div>
            <h2 class="heading-lg title-glow">Resumen</h2>
            <p class="subtitle mt-1">Rendimiento y métricas clave</p>
          </div>
        </div>

        <DashboardStats class="mt-6" :trades="trades" />
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
import Modal from './components/Modal.vue'
import TradeForm from './components/TradeForm.vue'
import TradeList from './components/TradeList.vue'
import DashboardStats from './components/DashboardStats.vue'
import { getTrades, createTrade, updateTrade, getTradeStatsSummary } from './api'
import { useOptionsStore } from './stores/optionsStore'

const showLogModal = ref(false)
const editingTrade = ref(null)
const trades = ref([])
const stats = ref({ total_pnl: 0, avg_pnl: 0, total_trades: 0, win_rate: 0 })
const loading = ref(false)
const error = ref('')
const optionsStore = useOptionsStore()

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

function cancelEdit() {
  editingTrade.value = null
  showLogModal.value = false
}

async function handleSubmit(payload) {
  try {
    loading.value = true
    error.value = ''
    
    if (editingTrade.value?.id) {
      // Create a clean payload for update, excluding the date if it hasn't changed
      const updatePayload = { ...payload }
      
      // If the date hasn't changed, remove it from the payload
      if (updatePayload.date === editingTrade.value.date) {
        delete updatePayload.date
      }
      
      console.log('Updating trade with payload:', { id: editingTrade.value.id, ...updatePayload })
      try {
        const result = await updateTrade(editingTrade.value.id, updatePayload)
        console.log('Update successful:', result)
      } catch (updateError) {
        console.error('Error updating trade:', updateError)
        throw updateError // Re-lanzar para que sea manejado por el catch externo
      }
    } else {
      console.log('Creating new trade:', payload)
      await createTrade(payload)
    }
    
    // Refrescar datos
    await Promise.all([refreshTrades(), refreshStats()])
    cancelEdit()
  } catch (e) {
    console.error('Error in handleSubmit:', e)
    error.value = e?.message || String(e)
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

