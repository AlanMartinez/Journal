<template>
  <div class="empty-state">
    <svg xmlns="http://www.w3.org/2000/svg" class="empty-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="iconPath" />
    </svg>
    <p class="empty-text">{{ message }}</p>
    <p v-if="subtitle" class="empty-subtext">{{ subtitle }}</p>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  message: {
    type: String,
    default: 'No hay datos disponibles'
  },
  subtitle: {
    type: String,
    default: ''
  },
  iconPath: {
    type: String,
    default: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
  }
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  color: rgba(255, 255, 255, 0.5);
}

.empty-icon {
  width: 64px;
  height: 64px;
  color: rgba(var(--accent-cyan) / 0.3);
  margin-bottom: 16px;
}

.empty-text {
  font-size: 18px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 16px;
}

.empty-subtext {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 8px;
  text-align: center;
}
</style>


