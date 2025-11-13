<template>
  <div class="loading-state">
    <div class="loading-spinner"></div>
    <p class="loading-text">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: 'Cargando...'
  }
})
</script>

<style scoped>
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: rgba(255, 255, 255, 0.5);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(var(--accent-cyan) / 0.2);
  border-top-color: rgba(var(--accent-cyan) / 1);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
}
</style>


