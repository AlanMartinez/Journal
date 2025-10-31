<template>
  <div class="panel p-6 h-full flex flex-col min-h-[600px]">
    <!-- Month Navigation -->
    <div class="flex items-center justify-between mb-6">
      <button 
        @click="previousMonth"
        class="p-2 rounded-full hover:bg-white/10 transition-colors"
        aria-label="Mes anterior"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <h2 class="text-lg font-semibold">{{ currentMonthName }} {{ currentYear }}</h2>
      
      <button 
        @click="nextMonth"
        class="p-2 rounded-full hover:bg-white/10 transition-colors"
        :disabled="isCurrentMonth"
        :class="{ 'opacity-50 cursor-not-allowed': isCurrentMonth }"
        aria-label="Siguiente mes"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <!-- Calendar Grid -->
    <div class="grid grid-cols-7 gap-2 flex-grow">
      <!-- Day headers -->
      <div 
        v-for="day in ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']" 
        :key="day"
        class="text-center text-sm font-medium text-white/70 py-2"
      >
        {{ day }}
      </div>
      
      <!-- Empty cells for days before the 1st -->
      <div 
        v-for="n in firstDayOfMonth" 
        :key="'empty-' + n" 
        class="aspect-square border border-transparent"
      ></div>
      
      <!-- Days of the month -->
      <div 
        v-for="day in daysInMonth" 
        :key="day"
        @click="selectDay(day)"
        @dblclick="openDayJournal(day)"
        class="aspect-square border border-white/5 rounded p-1 cursor-pointer hover:bg-white/5 transition-colors flex flex-col relative"
        :class="{
          'bg-primary/20': isToday(day),
          'selected-day-glow': selectedDay === day,
          'border-primary': selectedDay === day,
          'opacity-50': !isCurrentMonth
        }"
      >
        <div class="flex items-center justify-between relative w-full">
          <div v-if="hasBreakTradingPlan(day)" class="text-red-400 flex-shrink-0">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 3l18 18M9 9v-.01M15 9v-.01M9 9v6m0-6l6 6m0-6v6m0-6l-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="text-right text-sm flex-1">{{ day }}</div>
        </div>
        <div 
          v-if="getDayResult(day) !== 0" 
          class="text-xs mt-auto text-center font-medium py-1 px-1 rounded"
          :class="{
            'bg-green-500/20 text-green-400': getDayResult(day) > 0,
            'bg-red-500/20 text-red-400': getDayResult(day) < 0
          }"
        >
          {{ formatCurrency(getDayResult(day)) }}
        </div>
      </div>
    </div>

    <!-- Day Journal Modal -->
    <DayJournalModal 
      :isOpen="showDayJournalModal"
      :date="selectedDate"
      :trades="trades"
      @close="showDayJournalModal = false"
      @saved="handleDayJournalSaved"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import DayJournalModal from './DayJournalModal.vue'
import * as api from '../api.js'

const props = defineProps({
  trades: {
    type: Array,
    required: true
  }
})

const today = new Date()
const currentDate = ref(new Date())
const currentMonth = computed(() => currentDate.value.getMonth())
const currentYear = computed(() => currentDate.value.getFullYear())
const selectedDay = ref(today.getDate())
const showDayJournalModal = ref(false)
const selectedDate = ref('')
const dayJournals = ref([])

const monthNames = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
]

const currentMonthName = computed(() => monthNames[currentMonth.value])

const isCurrentMonth = computed(() => {
  const now = new Date()
  return currentMonth.value === now.getMonth() && currentYear.value === now.getFullYear()
})

function changeMonth(offset) {
  const newDate = new Date(currentDate.value)
  newDate.setMonth(newDate.getMonth() + offset)
  currentDate.value = newDate
  selectedDay.value = null
  // El watch se encargará de cargar los day journals del nuevo mes
}

function previousMonth() {
  changeMonth(-1)
}

function nextMonth() {
  if (!isCurrentMonth.value) {
    changeMonth(1)
  }
}

const daysInMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
})

const firstDayOfMonth = computed(() => {
  return new Date(currentYear.value, currentMonth.value, 1).getDay() // 0 = Sunday
})

function isToday(day) {
  const today = new Date()
  return day === today.getDate() && 
         currentMonth.value === today.getMonth() && 
         currentYear.value === today.getFullYear()
}

function selectDay(day) {
  selectedDay.value = day
  // Emit event or update state as needed
}

function getDayResult(day) {
  const y = currentYear.value
  const m = String(currentMonth.value + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  const date = `${y}-${m}-${d}`
  return props.trades
    .filter(trade => {
      // Handle both 'YYYY-MM-DD' and 'MM/DD/YYYY' formats
      let tradeDate = trade.date
      if (tradeDate.includes('/')) {
        const [month, day, year] = tradeDate.split('/')
        tradeDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
      }
      return tradeDate === date
    })
    .reduce((sum, trade) => sum + (parseFloat(trade.result) || 0), 0)
}

function formatCurrency(amount) {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount)
}

function openDayJournal(day) {
  const y = currentYear.value
  const m = String(currentMonth.value + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  const date = `${y}-${m}-${d}`
  selectedDate.value = date
  showDayJournalModal.value = true
}

function handleDayJournalSaved() {
  // Recargar day journals del mes actual cuando se guarda
  loadDayJournalsForMonth()
}

function hasBreakTradingPlan(day) {
  const y = currentYear.value
  const m = String(currentMonth.value + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  const date = `${y}-${m}-${d}`
  const dayJournal = dayJournals.value.find(dj => dj.date === date)
  return dayJournal && dayJournal.break_trading_plan === true
}

function getMonthDateRange() {
  // Obtener el primer día del mes
  const firstDay = new Date(currentYear.value, currentMonth.value, 1)
  const startDate = `${firstDay.getFullYear()}-${String(firstDay.getMonth() + 1).padStart(2, '0')}-${String(firstDay.getDate()).padStart(2, '0')}`
  
  // Obtener el último día del mes
  const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
  const endDate = `${lastDay.getFullYear()}-${String(lastDay.getMonth() + 1).padStart(2, '0')}-${String(lastDay.getDate()).padStart(2, '0')}`
  
  return { startDate, endDate }
}

async function loadDayJournalsForMonth() {
  try {
    const { startDate, endDate } = getMonthDateRange()
    dayJournals.value = await api.getDayJournalsByDateRange(startDate, endDate)
  } catch (error) {
    console.error('Error loading day journals for month:', error)
    dayJournals.value = []
  }
}

async function loadDayJournals() {
  try {
    dayJournals.value = await api.getDayJournals()
  } catch (error) {
    console.error('Error loading day journals:', error)
    dayJournals.value = []
  }
}

// Watch para recargar cuando cambie el mes o año
watch([currentMonth, currentYear], () => {
  loadDayJournalsForMonth()
})

onMounted(() => {
  loadDayJournalsForMonth()
})
</script>
