<template>
  <div class="chart-card">
    <h3 v-if="title" class="chart-title">{{ title }}</h3>
    <div class="chart-container" :style="{ height: height }">
      <slot />
    </div>
    <div v-if="$slots.footer" class="chart-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: ''
  },
  height: {
    type: String,
    default: '300px'
  }
})
</script>

<style scoped>
.chart-card {
  background: rgba(var(--panel-2) / 0.5);
  border: 1px solid rgba(var(--accent-cyan) / 0.1);
  border-radius: var(--radius);
  padding: 24px;
  transition: all 0.3s ease;
}

.chart-card:hover {
  border-color: rgba(var(--accent-cyan) / 0.3);
  box-shadow: 0 4px 20px rgba(var(--accent-cyan) / 0.15);
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 20px;
  text-align: center;
}

.chart-container {
  position: relative;
  margin-bottom: 20px;
}

.chart-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}
</style>


