<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto">
    <div class="absolute inset-0 bg-black/70 backdrop-blur-sm" @click="close"></div>
    <div
      class="relative mx-auto w-full max-w-2xl px-6 py-10"
      :class="containerClass"
      role="dialog"
      aria-modal="true"
    >
      <div class="panel p-0 overflow-hidden glow-cyan max-h-[85vh] overflow-y-auto">
        <header class="flex items-center justify-between px-6 py-4 border-b border-white/10">
          <h2 class="title-glow text-lg font-semibold">{{ title }}</h2>
          <button class="btn-secondary px-3 py-1" @click="close">Cerrar</button>
        </header>
        <section class="p-6">
          <slot />
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: '' },
  containerClass: { type: String, default: 'pt-28' }
})
const emit = defineEmits(['update:modelValue'])

function close() {
  emit('update:modelValue', false)
}

function onKey(e) {
  if (e.key === 'Escape') close()
}

onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>
