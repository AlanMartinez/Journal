<template>
  <div class="stats-grid">
    <MetricCard
      title="Win Rate"
      :value="formatPercent(stats?.win_rate)"
      :subtitle="`${stats?.winning_trades || 0} / ${stats?.total_trades || 0}`"
      icon="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
      color="cyan"
      :is-positive="(stats?.win_rate || 0) >= 50"
    />
    
    <MetricCard
      title="Total Trades"
      :value="stats?.total_trades || 0"
      subtitle="Operaciones totales"
      icon="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
      color="cyan"
    />
    
    <MetricCard
      title="Average Risk"
      :value="`${formatNumber(stats?.avg_risk, 2)}`"
      icon="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
      color="pink"
    />
    
    <MetricCard
      title="Total P&L"
      :value="formatCurrency(stats?.total_pnl)"
      subtitle="Beneficio/Pérdida"
      icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      color="cyan"
      :is-positive="(stats?.total_pnl || 0) >= 0"
    />
  </div>
</template>

<script setup>
import MetricCard from './ui/MetricCard.vue'

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

<style scoped>
.stats-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
