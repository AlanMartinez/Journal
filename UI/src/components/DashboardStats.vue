<template>
  <div class="mt-6 flex flex-wrap justify-center gap-6">
   
    <div class="panel p-5 glow-cyan w-[260px] md:w-[300px]">
      <div class="subtitle">Win Rate</div>
      <div class="metric metric-mono mt-1">{{ formatPercent(winRate) }}</div>
      <div class="text-xs text-white/50 mt-1">{{ wins }} / {{ total }}</div>
    </div>

    <div class="panel p-5 w-[260px] md:w-[300px]">
      <div class="subtitle">Operaciones</div>
      <div class="metric metric-mono mt-1">{{ total }}</div>
      <div class="text-xs text-white/50 mt-1">Últimos {{ total }}</div>
    </div>

    <div class="panel p-5 glow-amber w-[260px] md:w-[300px]">
      <div class="subtitle">Riesgo Promedio</div>
      <div class="metric metric-mono mt-1">{{ formatNumber(avgRisk, 2) }}</div>
    </div>
    
   
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  trades: { type: Array, default: () => [] }
})

const todayStr = new Date().toISOString().slice(0, 10)

const total = computed(() => props.trades.length)
const wins = computed(() => props.trades.filter(t => (t.status || '').toUpperCase() === 'TP').length)
const winRate = computed(() => total.value ? (wins.value / total.value) * 100 : 0)

const pnlToday = computed(() => props.trades
  .filter(t => t.date === todayStr)
  .reduce((acc, t) => acc + (Number(t.result) || 0), 0)
)
const pnlTodayPct = computed(() => {
  // Si tenés una base de capital, podrías normalizar; por ahora derivamos del rate si está presente
  // Si hay múltiples, promedio del rate del día
  const day = props.trades.filter(t => t.date === todayStr && t.rate != null)
  if (!day.length) return 0
  const avg = day.reduce((a, t) => a + Number(t.rate || 0), 0) / day.length
  return avg
})

const avgRisk = computed(() => {
  const withRisk = props.trades.map(t => Number(t.risk)).filter(v => !Number.isNaN(v))
  if (!withRisk.length) return 0
  return withRisk.reduce((a, b) => a + b, 0) / withRisk.length
})

const sumPnl = computed(() => props.trades.reduce((acc, t) => acc + (Number(t.result) || 0), 0))
const avgPnl = computed(() => total.value ? (sumPnl.value / total.value) : 0)

function abs(n){ return Math.abs(Number(n) || 0) }
function formatNumber(v, d=2){
  if (v == null || v === '' || Number.isNaN(Number(v))) return '0.00'
  return Number(v).toFixed(d)
}
function formatMoney(v){
  const n = Number(v) || 0
  return n.toFixed(2)
}
function formatPercent(v){
  const n = Number(v) || 0
  return `${n.toFixed(1)}%`
}
</script>
