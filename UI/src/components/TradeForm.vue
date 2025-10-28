<template>
  <form @submit.prevent="onSubmit" class="space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label class="subtitle block mb-1">Símbolo</label>
        <div class="flex flex-wrap gap-2">
          <button v-for="s in symbolOptions" :key="s" type="button"
                  class="badge px-3 py-1"
                  :class="{ 'badge-live': form.symbol === s }"
                  @click="form.symbol = s">
            {{ s }}
          </button>
        </div>
      </div>
      <div>
        <label class="subtitle block mb-1">Tipo de operación</label>
        <select v-model="form.side" class="input w-full" required>
          <option value="buy">Compra</option>
          <option value="sell">Venta</option>
        </select>
      </div>
      <div>
        <label class="subtitle block mb-1">Fecha</label>
        <input v-model="form.date" type="date" class="input w-full" required />
      </div>
      <div>
        <label class="subtitle block mb-1">rate</label>
        <div class="relative">
          <input v-model.number="form.rate" type="number" step="0.01" min="0" class="input w-full pr-12" placeholder="0.5" required />
          <span class="absolute right-3 top-1/2 -translate-y-1/2 text-white/70">%</span>
        </div>
      </div>
      <div>
        <label class="subtitle block mb-1">Riesgo (R)</label>
        <input v-model.number="form.risk" type="number" step="0.01" class="input w-full" placeholder="1.0" />
      </div>
      <div>
        <label class="subtitle block mb-1">dinero+-</label>
        <input v-model.number="form.result" type="number" step="0.01" class="input w-full" placeholder="$" />
      </div>
      <div class="sm:col-span-2">
        <label class="subtitle block mb-1">Emociones asociadas</label>
        <div class="flex flex-wrap gap-2">
          <button v-for="tag in emotionOptions" :key="tag" type="button"
                  class="chip"
                  :class="{ 'chip-selected': form.emotions.includes(tag) }"
                  @click="toggleEmotion(tag)">
            {{ tag }}
          </button>
        </div>
      </div>
      <div class="sm:col-span-2">
        <label class="subtitle block mb-1">Confirmaciones</label>
        <div class="flex flex-wrap gap-2">
          <button v-for="confirmation in confirmationsOptions" :key="confirmation" type="button"
                  class="chip"
                  :class="{ 'chip-selected': form.confirmations.includes(confirmation) }"
                  @click="toggleConfirmation(confirmation)">
            {{ confirmation }}
          </button>
        </div>
      </div>
      <div class="sm:col-span-2">
        <label class="subtitle block mb-1">Notas</label>
        <textarea v-model.trim="form.notes" rows="4" class="input w-full" placeholder="Contexto, setup, gestión, mejoras..."></textarea>
      </div>
    </div>

    <div class="mt-2">
      <label class="subtitle block mb-1">Trade Link</label>
      <input v-model.trim="form.tradingLink" type="url" class="input w-full" placeholder="https://..." />
    </div>

    <div class="flex items-center justify-center pt-2">
      <div class="inline-flex gap-2 p-1 rounded-full border border-white/10 backdrop-blur-sm">
        <button type="button"
                class="btn-secondary px-12 py-2"
                :class="form.status === 'TP' ? 'glow-cyan' : ''"
                :style="form.status === 'TP' ? 'color: rgb(34,197,94); border-color: rgba(34,197,94,0.5); background: rgba(34,197,94,0.15);' : ''"
                @click="form.status = 'TP'">
          TP
        </button>
        <button type="button"
                class="btn-secondary px-12 py-2"
                :class="form.status === 'BE' ? 'glow-cyan' : ''"
                :style="form.status === 'BE' ? 'color: rgb(59,130,246); border-color: rgba(59,130,246,0.5); background: rgba(59,130,246,0.15);' : ''"
                @click="form.status = 'BE'">
          BE
        </button>
        <button type="button"
                class="btn-secondary px-12 py-2"
                :class="form.status === 'SL' ? 'glow-cyan' : ''"
                :style="form.status === 'SL' ? 'color: rgb(239,68,68); border-color: rgba(239,68,68,0.5); background: rgba(239,68,68,0.15);' : ''"
                @click="form.status = 'SL'">
          SL
        </button>
      </div>
    </div>

    <div class="flex items-center justify-end gap-3 pt-2">
      <button type="button" class="btn-secondary" @click="$emit('cancel')">Cancelar</button>
      <button type="submit" class="btn-primary">Guardar Trade</button>
    </div>
  </form>
</template>

<script setup>
import { reactive, computed } from 'vue'
import { useOptionsStore } from '../stores/optionsStore'

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['submit', 'cancel'])

const store = useOptionsStore()
const emotionOptions = computed(() => store.state.emotions)
const confirmationsOptions = computed(() => store.state.confirmations)

const symbolOptions = ['NQ', 'ES', 'YM', 'CL', 'GC']
const form = reactive({
  symbol: props.initialData?.symbol || 'NQ',
  side: props.initialData?.side || 'buy',
  date: props.initialData?.date || new Date().toISOString().slice(0, 10),
  rate: props.initialData?.rate || 0.5,
  risk: props.initialData?.risk || null,
  result: props.initialData?.result || null,
  notes: props.initialData?.notes || '',
  emotions: props.initialData?.emotions || [],
  confirmations: props.initialData?.confirmations || [],
  tradingLink: props.initialData?.tradingLink || null,
  status: props.initialData?.status || 'BE'
})

function toggleEmotion(tag) {
  const i = form.emotions.indexOf(tag)
  if (i >= 0) form.emotions.splice(i, 1)
  else form.emotions.push(tag)
}

function toggleConfirmation(tag) {
  const i = form.confirmations.indexOf(tag)
  if (i >= 0) form.confirmations.splice(i, 1)
  else form.confirmations.push(tag)
}

function onSubmit() {
  if (!form.symbol || !form.side || !form.date) return
  if (form.rate == null) return

  const payload = {
    symbol: form.symbol,
    side: form.side,
    date: form.date,
    rate: form.rate,
    risk: form.risk,
    result: form.result,
    notes: form.notes,
    emotions: form.emotions,
    confirmations: form.confirmations,
    tradingLink: form.tradingLink,
    status: form.status,
    ...(props.initialData?.id && { id: props.initialData.id }) // Include ID if editing
  }
  
  emit('submit', payload)
}
</script>
