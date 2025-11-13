<template>
  <div class="error-state">
    <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <p class="error-text">{{ message }}</p>
    <button v-if="showRetry" class="btn-primary mt-4" @click="handleRetry">
      {{ retryText }}
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  message: {
    type: String,
    default: 'Ocurrió un error'
  },
  showRetry: {
    type: Boolean,
    default: true
  },
  retryText: {
    type: String,
    default: 'Reintentar'
  }
})

const emit = defineEmits(['retry'])

function handleRetry() {
  emit('retry')
}
</script>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: rgba(255, 255, 255, 0.5);
}

.error-icon {
  width: 64px;
  height: 64px;
  color: rgba(var(--accent-cyan) / 0.3);
  margin-bottom: 16px;
}

.error-text {
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 16px;
  text-align: center;
}
</style>


