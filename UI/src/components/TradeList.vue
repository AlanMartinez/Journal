<template>
  <div class="mt-6">
    <!-- Pagination Controls -->
    
    <!-- Trades Table -->
    <div class="overflow-x-auto">
      <table class="w-full text-left align-middle">
      <thead>
        <tr class="text-sm text-white/70">
          <th class="py-2 pr-4">Símbolo</th>
          <th class="py-2 pr-4">Estado</th>
          <th class="py-2 pr-4">Tipo</th>
          <th class="py-2 pr-20">Fecha</th>
          <th class="py-2 pr-4">Rate</th>
          <th class="py-2 pr-4">Riesgo</th>
          <th class="py-2 pr-4">Dinero+-</th>
          <th class="py-2 pr-4">
            <div class="flex items-center gap-2">
              <span>Emociones</span>
              <button type="button" class="btn-secondary px-2 py-0.5" title="Configurar emociones" @click.stop="openManager('emotions')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 8 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 3.4 15a1.65 1.65 0 0 0-1.51-1H2a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 3.4 8a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 8 3.4a1.65 1.65 0 0 0 1-1.51V2a2 2 0 1 1 4 0v.09A1.65 1.65 0 0 0 15 3.4a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 20.6 8c.36.36.57.85.6 1.36V9a2 2 0 1 1 0 4h-.09c-.51.03-1 .24-1.36.6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </th>
          <th class="py-2 pr-4">
            <div class="flex items-center gap-2">
              <span>Confirmaciones</span>
              <button type="button" class="btn-secondary px-2 py-0.5" title="Configurar confirmaciones" @click.stop="openManager('confirmations')">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 8 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 3.4 15a1.65 1.65 0 0 0-1.51-1H2a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 3.4 8a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 8 3.4a1.65 1.65 0 0 0 1-1.51V2a2 2 0 1 1 4 0v.09A1.65 1.65 0 0 0 15 3.4a1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 20.6 8c.36.36.57.85.6 1.36V9a2 2 0 1 1 0 4h-.09c-.51.03-1 .24-1.36.6z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </div>
          </th>
          <th class="py-2 pr-4">Enlace</th>
          <th class="py-2 pr-4">Notas</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in paginatedTrades" :key="t.id" 
    class="border-t border-white/10 hover:bg-white/5 transition-colors duration-150 cursor-pointer"
    @dblclick="editTrade(t)">
          <td class="py-3 pr-4">{{ t.symbol }}</td>
          <td class="py-3 pr-4">
            <span class="badge" :class="statusClass(t.status)">{{ t.status || 'BE' }}</span>
          </td>
          <td class="py-3 pr-4">{{ t.side === 'buy' ? 'Compra' : 'Venta' }}</td>
          <td class="py-3 pr-4">{{ t.date }}</td>
          <td class="py-3 pr-4 metric-mono">{{ formatRate(t.rate) }}</td>
          <td class="py-3 pr-4 metric-mono">{{ formatRisk(t.risk) }}</td>
          <td class="py-3 pr-4 metric-mono">
            <span :style="moneyColor(t.status)">{{ formatMoney(t.result) }}</span>
          </td>
          <td class="py-3 pr-4">
            <div class="flex flex-wrap gap-2">
              <span v-for="e in t.emotions || []" :key="e" class="badge badge-cyan text-xs">{{ e }}</span>
            </div>
          </td>
          <td class="py-3 pr-4">
            <div class="flex flex-wrap gap-2">
              <span v-for="c in t.confirmations || []" :key="c" class="badge badge-amber text-xs">{{ c }}</span>
            </div>
          </td>
          <td class="py-3 pr-4">
            <a v-if="tradeLink(t)" :href="tradeLink(t)" target="_blank" rel="noopener" class="inline-flex items-center justify-center link" title="Abrir link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 3h7v7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M10 14L21 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M21 14v7h-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M3 10h7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </a>
            <span v-else class="text-white/50">-</span>
          </td>
          <td class="py-3 pr-4">
            <div class="relative inline-block">
              <button v-if="t.notes" type="button" class="inline-flex items-center justify-center btn-secondary px-2 py-1"
                      @click.stop="(e) => toggleNote(e, t.id)" :aria-expanded="openNoteId === t.id">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M19 21H5a2 2 0 0 1-2-2V7l4-4h10a2 2 0 0 1 2 2v16z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 7h6M9 11h6M9 15h4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
              <span v-else class="text-white/50">-</span>

              <div v-if="openNoteId === t.id" 
                   class="panel absolute right-0 top-full mt-2 w-72 p-4 z-50 shadow-xl border border-white/10"
                   v-click-outside="() => closeNote()">
                <div class="flex justify-between items-center mb-2">
                  <div class="subtitle">Notas</div>
                  <button @click="closeNote" class="text-white/50 hover:text-white transition-colors">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </button>
                </div>
                <p class="text-sm leading-relaxed whitespace-pre-wrap">{{ t.notes }}</p>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    </div>

     <div class="flex flex-col items-center mt-2">
      <div class="flex items-center gap-1 bg-panel-2/50 rounded-xl p-1 border border-white/5 shadow-lg">
        <button 
          @click="previousPage" 
          :disabled="currentPage === 1"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-1.5"
          :class="{
            'text-white/40 cursor-not-allowed': currentPage === 1,
            'text-white hover:bg-accent-cyan/10 hover:text-accent-cyan': currentPage > 1
          }"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="shrink-0">
            <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Anterior</span>
        </button>
        
        <div class="px-4 py-2 text-sm font-medium text-white/80">
          <span class="text-accent-cyan font-semibold">{{ currentPage }}</span> / {{ totalPages }}
        </div>
        
        <button 
          @click="nextPage" 
          :disabled="currentPage >= totalPages"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 flex items-center gap-1.5"
          :class="{
            'text-white/40 cursor-not-allowed': currentPage >= totalPages,
            'text-white hover:bg-accent-cyan/10 hover:text-accent-cyan': currentPage < totalPages
          }"
        >
          <span>Siguiente</span>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="shrink-0">
            <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
   
    
    
    <!-- Tag Manager Modal -->
    <Modal :modelValue="!!showManagerFor" @update:modelValue="val => !val && (showManagerFor = null)" :title="showManagerFor === 'emotions' ? 'Administrar Emociones' : 'Administrar Confirmaciones'">
      <TagManager :type="showManagerFor" />
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import Modal from './Modal.vue'
import TagManager from './TagManager.vue'
import { useOptionsStore } from '../stores/optionsStore'

// Click outside directive
const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function(event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value()
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}

const props = defineProps({
  trades: {
    type: Array,
    default: () => []
  }
})

// Pagination state
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Computed properties
const totalItems = computed(() => props.trades.length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
const startItem = computed(() => (currentPage.value - 1) * itemsPerPage.value + 1)
const endItem = computed(() => {
  const end = currentPage.value * itemsPerPage.value
  return end > totalItems.value ? totalItems.value : end
})

// Paginated trades
const paginatedTrades = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return props.trades.slice(start, end)
})

// Navigation methods
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

function previousPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// Reset to first page when items per page changes
watch(itemsPerPage, () => {
  currentPage.value = 1
})

const openNoteId = ref(null)
const showManagerFor = ref(null) // 'emotions' | 'confirmations' | null
const emit = defineEmits(['edit'])
const optionsStore = useOptionsStore()

function editTrade(trade) {
  emit('edit', trade)
}

function toggleNote(event, id) {
  event.stopPropagation()
  openNoteId.value = openNoteId.value === id ? null : id
}

function closeNote() {
  openNoteId.value = null
}

function onDocClick() {
  if (openNoteId.value !== null) {
    openNoteId.value = null
  }
}

function onKey(e) {
  if (e.key === 'Escape') {
    if (openNoteId.value != null) openNoteId.value = null
    if (showManagerFor.value) showManagerFor.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', onDocClick)
  document.addEventListener('keydown', onKey)
})
onBeforeUnmount(() => {
  document.removeEventListener('click', onDocClick)
  document.removeEventListener('keydown', onKey)
})

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
  const sign = Number(v) >= 0 ? '' : '-'
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

function tradeLink(t) {
  const raw = (t && (t.tradingLink || t.trading_link)) || ''
  if (!raw) return ''
  return /^https?:\/\//i.test(raw) ? raw : `https://${raw}`
}

async function openManager(type) {
  try {
    await optionsStore.loadAll()
  } catch (error) {
    console.error('Error loading options:', error)
  } finally {
    showManagerFor.value = type
  }
}
</script>

<style scoped>
.items-per-page-selector {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%23D4ADFC' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.25rem center;
  background-size: 1.25rem;
}
</style>
