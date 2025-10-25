<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h3 class="heading-lg title-glow text-base">{{ prettyTitle }}</h3>
    </div>

    <div class="flex flex-wrap gap-2 mb-4">
      <span v-for="tag in list" :key="tag" class="badge badge-cyan inline-flex items-center gap-2">
        {{ tag }}
        <button type="button" class="btn-secondary px-2 py-0.5" @click="remove(tag)">x</button>
      </span>
      <span v-if="!list || list.length === 0" class="text-white/60">No hay elementos.</span>
    </div>

    <form @submit.prevent="add" class="flex items-center gap-2">
      <input v-model.trim="draft" class="input flex-1" :placeholder="`Nueva ${typeSingular}`" />
      <button type="submit" class="btn-primary">Agregar</button>
    </form>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useOptionsStore } from '../stores/optionsStore'

const props = defineProps({
  type: { type: String, required: true } // 'emotions' | 'confirmations'
})

const store = useOptionsStore()
const draft = ref('')

const list = computed(() => store.state[props.type])
const prettyTitle = computed(() => props.type === 'emotions' ? 'Emociones' : 'Confirmaciones')
const typeSingular = computed(() => props.type === 'emotions' ? 'emoción' : 'confirmación')

function add() {
  if (!draft.value) return
  store.addTag(props.type, draft.value)
  draft.value = ''
}
function remove(tag) {
  store.removeTag(props.type, tag)
}
</script>
