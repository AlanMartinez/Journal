<template>
  <div class="space-y-4">
    <div class="panel p-4">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-white/70">Win Rate</p>
          <p class="text-2xl font-bold" :class="(stats?.win_rate || 0) >= 0 ? 'text-green-400' : 'text-red-400'">
            {{ formatPercent(stats?.win_rate) }}
          </p>
          <p class="text-xs text-white/50 mt-1">{{ stats?.winning_trades || 0 }} / {{ stats?.total_trades || 0 }}</p>
        </div>
        <div class="p-2 rounded-full bg-cyan-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
      </div>
    </div>

    <div class="panel p-4">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-white/70">Operaciones</p>
          <p class="text-2xl font-bold">{{ stats?.total_trades || 0 }}</p>
          <p class="text-xs text-white/50 mt-1">Total de trades</p>
        </div>
        <div class="p-2 rounded-full bg-blue-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
      </div>
    </div>

    <div class="panel p-4">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-white/70">Riesgo Promedio</p>
          <p class="text-2xl font-bold">{{ formatNumber(stats?.avg_risk, 2) }}</p>
        </div>
        <div class="p-2 rounded-full bg-amber-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
      </div>
    </div>

    <div class="panel p-4">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm text-white/70">Resultado Total</p>
          <p class="text-2xl font-bold" :class="(stats?.total_pnl || 0) >= 0 ? 'text-green-400' : 'text-red-400'">
            {{ formatCurrency(stats?.total_pnl) }}
          </p>
          <p class="text-xs text-white/50 mt-1">Beneficio/Pérdida</p>
        </div>
        <div class="p-2 rounded-full bg-green-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  stats: { type: Object, default: () => ({}) }
})

function formatNumber(v, d = 2) {
  if (v == null || v === '' || Number.isNaN(Number(v))) return '0.00'
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: d,
    maximumFractionDigits: d
  }).format(Number(v))
}

function formatCurrency(amount) {
  const num = Number(amount) || 0
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(num)
}

function formatPercent(v) {
  const n = Number(v) || 0
  return `${n.toFixed(1)}%`
}
</script>
