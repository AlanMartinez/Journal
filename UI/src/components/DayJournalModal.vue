<template>
  <Modal :modelValue="isOpen" @update:modelValue="$emit('close')" :title="modalTitle">
    <div class="space-y-6">
    <!-- Form -->
      <div class="border-t border-white/10 pt-6">
        <h3 class="subtitle mb-4">Notas del día</h3>
        <form @submit.prevent="saveDayJournal" class="space-y-4">
          <!-- Break Trading Plan Button -->
          <div class="flex items-center gap-3">
            <label class="flex items-center gap-2 cursor-pointer">
              <input 
                type="checkbox" 
                v-model="breakTradingPlan"
                class="sr-only"
              />
              <div 
                class="w-12 h-12 rounded-lg border-2 transition-all duration-200 flex items-center justify-center"
                :class="breakTradingPlan 
                  ? 'bg-red-500/20 border-red-500 text-red-400' 
                  : 'bg-white/5 border-white/10 text-white/50 hover:border-white/20'"
              >
                <svg v-if="breakTradingPlan" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 3l18 18M9 9v-.01M15 9v-.01M9 9v6m0-6l6 6m0-6v6m0-6l-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 12l2 2 4-4M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9 9 4.03 9 9z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <span class="text-sm font-medium" :class="breakTradingPlan ? 'text-red-400' : 'text-white/70'">
                {{ breakTradingPlan ? 'Rompí mi trading plan' : 'No rompí mi trading plan' }}
              </span>
            </label>
          </div>

          <!-- Notes Textarea -->
          <div>
            <label class="block text-sm font-medium text-white/70 mb-2">
              Notas generales del día
            </label>
            <textarea
              v-model="notes"
              rows="5"
              class="input w-full"
              placeholder="Reflexiones sobre la sesión, análisis del mercado, lecciones aprendidas..."
            ></textarea>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-3 justify-end pt-4 border-t border-white/10">
            <button 
              type="button" 
              @click="$emit('close')"
              class="btn-secondary"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              class="btn-primary"
              :disabled="saving"
            >
              <span v-if="!saving">Guardar</span>
              <span v-else class="flex items-center gap-2">
                <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Guardando...
              </span>
            </button>
          </div>
        </form>
      </div>
      
      <!-- Trades List -->
      <div>
        <h3 class="subtitle mb-4">Operaciones del día</h3>
        <div v-if="dayTrades.length === 0" class="text-white/50 text-center py-8">
          No hay operaciones registradas para este día
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-left align-middle">
            <thead>
              <tr class="text-sm text-white/70">
                <th class="py-2 pr-4">Símbolo</th>
                <th class="py-2 pr-4">Estado</th>
                <th class="py-2 pr-4">Tipo</th>
                <th class="py-2 pr-4">Rate</th>
                <th class="py-2 pr-4">Riesgo</th>
                <th class="py-2 pr-4">Resultado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trade in dayTrades" :key="trade.id" 
                  class="border-t border-white/10 hover:bg-white/5 transition-colors">
                <td class="py-3 pr-4">{{ trade.symbol }}</td>
                <td class="py-3 pr-4">
                  <span class="badge" :class="statusClass(trade.status)">{{ trade.status || 'BE' }}</span>
                </td>
                <td class="py-3 pr-4">{{ trade.side === 'buy' ? 'Compra' : 'Venta' }}</td>
                <td class="py-3 pr-4 metric-mono">{{ formatRate(trade.rate) }}</td>
                <td class="py-3 pr-4 metric-mono">{{ formatRisk(trade.risk) }}</td>
                <td class="py-3 pr-4 metric-mono">
                  <span :style="moneyColor(trade.status)">{{ formatMoney(trade.result) }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      
    </div>
  </Modal>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Modal from './Modal.vue'
import * as api from '../api.js'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  date: {
    type: String,
    required: true
  },
  trades: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'saved'])

const notes = ref('')
const breakTradingPlan = ref(false)
const saving = ref(false)
const existingDayJournal = ref(null)

// Computed
function formatLocalISOToLongEs(dateStr) {
  if (!dateStr) return ''
  const [y, m, d] = dateStr.split('-').map(Number)
  const localDate = new Date(y, (m || 1) - 1, d || 1)
  return localDate.toLocaleDateString('es-AR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

const modalTitle = computed(() => {
  const formattedDate = formatLocalISOToLongEs(props.date)
  return `Registro Diario - ${formattedDate}`
})

const dayTrades = computed(() => {
  return props.trades.filter(trade => {
    let tradeDate = trade.date
    if (tradeDate.includes('/')) {
      const [month, day, year] = tradeDate.split('/')
      tradeDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
    }
    return tradeDate === props.date
  })
})

// Watch for date changes to load existing data
watch(() => props.date, async (newDate) => {
  if (newDate && props.isOpen) {
    await loadExistingDayJournal()
  }
}, { immediate: true })

watch(() => props.isOpen, async (isOpen) => {
  if (isOpen) {
    await loadExistingDayJournal()
  }
})

async function loadExistingDayJournal() {
  if (!props.date) return

  try {
    const dayJournals = await api.getDayJournals()
    const existing = dayJournals.find(dj => dj.date === props.date)
    
    if (existing) {
      existingDayJournal.value = existing
      notes.value = existing.notes || ''
      breakTradingPlan.value = existing.break_trading_plan || false
    } else {
      existingDayJournal.value = null
      notes.value = ''
      breakTradingPlan.value = false
    }
  } catch (error) {
    console.error('Error loading day journal:', error)
  }
}

async function saveDayJournal() {
  saving.value = true
  
  try {
    if (existingDayJournal.value) {
      // Update existing - no incluimos date ya que no debe cambiar
      const data = {
        break_trading_plan: breakTradingPlan.value,
        notes: notes.value
      }
      await api.updateDayJournal(existingDayJournal.value.id, data)
    } else {
      // Create new - incluir date al crear
      const data = {
        date: props.date,
        break_trading_plan: breakTradingPlan.value,
        notes: notes.value
      }
      await api.createDayJournal(data)
    }

    emit('saved')
    emit('close')
  } catch (error) {
    console.error('Error saving day journal:', error)
    alert('No se pudo guardar el registro. Por favor intenta nuevamente.')
  } finally {
    saving.value = false
  }
}

// Format functions
function formatRate(v) {
  if (v == null || v === '') return '-'
  const n = Number(v)
  return `${n.toFixed(1)}%`
}

function formatRisk(v) {
  if (v == null || v === '') return '-'
  return Number(v).toFixed(2)
}

function formatMoney(v) {
  if (v == null || v === '') return '-'
  const sign = Number(v) >= 0 ? '+' : ''
  const abs = Math.abs(Number(v)).toFixed(2)
  return `${sign}$${abs}`
}

function moneyColor(status) {
  if (status === 'TP') return 'color: rgb(34,197,94)'
  if (status === 'SL') return 'color: rgb(239,68,68)'
  return 'color: rgb(59,130,246)'
}

function statusClass(status) {
  if (status === 'TP') return 'status-tp'
  if (status === 'SL') return 'status-sl'
  return 'status-be'
}
</script>

