<template>
  <div class="statistics-container px-6 pt-12 pb-12">
    <section class="panel p-6 md:p-8">
      <h2 class="heading-lg title-glow">Estadisticas</h2>
      <p class="subtitle mt-2">Análisis detallado de tu rendimiento</p>
      
      <!-- Loading State -->
      <LoadingState v-if="loading" message="Cargando estadísticas..." />

      <!-- Error State -->
      <ErrorState 
        v-else-if="error" 
        :message="error"
        @retry="fetchStats"
      />

      <!-- Statistics Content -->
      <div v-else-if="stats" class="stats-content">
        <!-- Metric Cards Grid -->
        <div class="metrics-grid">
          <MetricCard
            title="Total Trades"
            :value="stats.total_trades"
            icon="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            color="cyan"
          />
          <MetricCard
            title="Total P&L"
            :value="formatCurrency(stats.total_pnl)"
            :is-positive="stats.total_pnl >= 0"
            icon="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            color="cyan"
          />
          <MetricCard
            title="Average P&L"
            :value="formatCurrency(stats.avg_pnl)"
            :is-positive="stats.avg_pnl >= 0"
            icon="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"
            color="amber"
          />
          <MetricCard
            title="Average Risk"
            :value="`${formatNumber(stats.avg_risk, 2)}`"
            icon="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
            color="pink"
          />
        </div>

        <!-- Charts Grid -->
        <div class="charts-grid">
          <!-- Win Rate Donut Chart -->
          <ChartCard title="Win Rate">
            <Doughnut
              :data="winRateData"
              :options="winRateOptions"
            />
            <template #footer>
              <span class="chart-value">{{ stats.win_rate }}%</span>
              <span class="chart-description">Tasa de operaciones ganadoras</span>
            </template>
          </ChartCard>

          <!-- Winning vs Losing Trades Bar Chart -->
          <ChartCard title="Winning vs Losing Trades">
            <Bar
              :data="tradesComparisonData"
              :options="barChartOptions"
            />
            <template #footer>
              <div class="chart-legend">
                <div class="legend-item">
                  <span class="legend-color" style="background: rgba(212, 173, 252, 0.8)"></span>
                  <span>Ganadoras: {{ stats.winning_trades }}</span>
                </div>
                <div class="legend-item">
                  <span class="legend-color" style="background: rgba(239, 68, 68, 0.8)"></span>
                  <span>Perdedoras: {{ stats.losing_trades }}</span>
                </div>
              </div>
            </template>
          </ChartCard>
        </div>
      </div>

      <!-- Empty State -->
      <EmptyState
        v-else
        message="No hay estadísticas disponibles"
        subtitle="Registra algunas operaciones para ver tus estadísticas"
      />
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Doughnut, Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { getTradeStatsSummary } from '../api'
import MetricCard from './ui/MetricCard.vue'
import LoadingState from './ui/LoadingState.vue'
import ErrorState from './ui/ErrorState.vue'
import EmptyState from './ui/EmptyState.vue'
import ChartCard from './ui/ChartCard.vue'

// Register Chart.js components
ChartJS.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

const stats = ref(null)
const loading = ref(true)
const error = ref(null)

// Fetch statistics
async function fetchStats() {
  loading.value = true
  error.value = null
  try {
    stats.value = await getTradeStatsSummary()
  } catch (err) {
    console.error('Error fetching stats:', err)
    error.value = 'No se pudieron cargar las estadísticas. Por favor, intenta de nuevo.'
  } finally {
    loading.value = false
  }
}

// Format currency
function formatCurrency(amount) {
  const num = Number(amount) || 0
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(num)
}

// Format number
function formatNumber(v, d = 2) {
  if (v == null || v === '' || Number.isNaN(Number(v))) return '0.00'
  return new Intl.NumberFormat('es-AR', {
    minimumFractionDigits: d,
    maximumFractionDigits: d
  }).format(Number(v))
}

// Win Rate Donut Chart Data
const winRateData = computed(() => {
  if (!stats.value) return null
  
  const winRate = stats.value.win_rate || 0
  const lossRate = 100 - winRate
  
  return {
    labels: ['Wins', 'Losses'],
    datasets: [{
      data: [winRate, lossRate],
      backgroundColor: [
        'rgba(212, 173, 252, 0.8)',  // accent-cyan
        'rgba(239, 68, 68, 0.8)'     // red for losses
      ],
      borderColor: [
        'rgba(212, 173, 252, 1)',
        'rgba(239, 68, 68, 1)'
      ],
      borderWidth: 2,
      hoverOffset: 4
    }]
  }
})

// Win Rate Chart Options
const winRateOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(22, 30, 46, 0.95)',
      titleColor: 'rgba(255, 255, 255, 0.9)',
      bodyColor: 'rgba(255, 255, 255, 0.7)',
      borderColor: 'rgba(212, 173, 252, 0.3)',
      borderWidth: 1,
      padding: 12,
      callbacks: {
        label: function(context) {
          return `${context.label}: ${context.parsed}%`
        }
      }
    }
  },
  cutout: '70%'
}))

// Winning vs Losing Trades Bar Chart Data
const tradesComparisonData = computed(() => {
  if (!stats.value) return null
  
  return {
    labels: ['Trades'],
    datasets: [
      {
        label: 'Winning Trades',
        data: [stats.value.winning_trades || 0],
        backgroundColor: 'rgba(212, 173, 252, 0.8)',
        borderColor: 'rgba(212, 173, 252, 1)',
        borderWidth: 2
      },
      {
        label: 'Losing Trades',
        data: [stats.value.losing_trades || 0],
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 2
      }
    ]
  }
})

// Bar Chart Options
const barChartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(22, 30, 46, 0.95)',
      titleColor: 'rgba(255, 255, 255, 0.9)',
      bodyColor: 'rgba(255, 255, 255, 0.7)',
      borderColor: 'rgba(212, 173, 252, 0.3)',
      borderWidth: 1,
      padding: 12
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        color: 'rgba(255, 255, 255, 0.6)',
        font: {
          size: 12
        }
      },
      grid: {
        color: 'rgba(255, 255, 255, 0.05)'
      }
    },
    x: {
      ticks: {
        color: 'rgba(255, 255, 255, 0.6)',
        font: {
          size: 12
        }
      },
      grid: {
        display: false
      }
    }
  }
}))

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.statistics-container {
  width: 100%;
}


.stats-content {
  margin-top: 32px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
}

.chart-value {
  font-size: 32px;
  font-weight: 700;
  color: rgba(var(--accent-cyan) / 1);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

.chart-description {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
}

.chart-legend {
  display: flex;
  gap: 24px;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>

