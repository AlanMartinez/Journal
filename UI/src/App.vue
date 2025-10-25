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
        <TradeList v-else class="mt-6" :trades="trades" />
      </section>

      <section class="panel p-6 md:p-8">
        <div class="flex items-start justify-between gap-6">
          <div>
            <h2 class="heading-lg title-glow">Resumen</h2>
            <p class="subtitle mt-1">Rendimiento y métricas clave</p>
          </div>
        </div>

        <div class="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="panel p-5 glow-cyan">
            <div class="subtitle">PNL Hoy</div>
            <div class="metric metric-mono mt-1">+2.45%</div>
          </div>
          <div class="panel p-5">
            <div class="subtitle">Operaciones</div>
            <div class="metric metric-mono mt-1">{{ trades.length }}</div>
          </div>
          <div class="panel p-5 glow-amber">
            <div class="subtitle">Riesgo</div>
            <div class="metric metric-mono mt-1">0.62</div>
          </div>
        </div>
      </section>

      <Modal v-model="showLogModal" title="Log Trade">
        <TradeForm @cancel="showLogModal = false" @submit="handleSubmit" />
      </Modal>
    </main>
  </div>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Modal from './components/Modal.vue'
import TradeForm from './components/TradeForm.vue'
import TradeList from './components/TradeList.vue'
import { getTrades, createTrade } from './api'
import { useOptionsStore } from './stores/optionsStore'

const showLogModal = ref(false)
const trades = ref([])
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

async function handleSubmit(payload) {
  try {
    loading.value = true
    error.value = ''
    await createTrade(payload)
    await refreshTrades()
    showLogModal.value = false
  } catch (e) {
    error.value = e?.message || String(e)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    optionsStore.loadAll(),
    refreshTrades(),
  ])
})
</script>

