<template>
  <div class="metric-card">
    <div class="metric-header">
      <svg 
        v-if="icon" 
        xmlns="http://www.w3.org/2000/svg" 
        class="metric-icon" 
        :class="`icon-${color}`"
        fill="none" 
        viewBox="0 0 24 24" 
        stroke="currentColor"
      >
        <path :d="icon" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
      </svg>
      <span class="metric-title">{{ title }}</span>
    </div>
    <div 
      class="metric-value" 
      :class="{ 
        'value-positive': isPositive === true, 
        'value-negative': isPositive === false 
      }"
    >
      {{ value }}
    </div>
    <div v-if="subtitle" class="metric-subtitle">{{ subtitle }}</div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: ''
  },
  color: {
    type: String,
    default: 'cyan',
    validator: (value) => ['cyan', 'amber', 'pink', 'green', 'blue', 'red'].includes(value)
  },
  isPositive: {
    type: Boolean,
    default: null
  }
})
</script>

<style scoped>
.metric-card {
  background: rgba(var(--panel-2) / 0.5);
  border: 1px solid rgba(var(--accent-cyan) / 0.1);
  border-radius: var(--radius);
  padding: 20px;
  transition: all 0.3s ease;
}

.metric-card:hover {
  border-color: rgba(var(--accent-cyan) / 0.3);
  box-shadow: 0 4px 20px rgba(var(--accent-cyan) / 0.15);
  transform: translateY(-2px);
}

.metric-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.metric-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.icon-cyan {
  color: rgba(var(--accent-cyan) / 0.9);
}

.icon-amber {
  color: rgba(var(--accent-amber) / 0.9);
}

.icon-pink {
  color: rgba(var(--accent-pink) / 0.9);
}

.icon-green {
  color: rgba(34, 197, 94, 0.9);
}

.icon-blue {
  color: rgba(59, 130, 246, 0.9);
}

.icon-red {
  color: rgba(239, 68, 68, 0.9);
}

.metric-title {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-value {
  font-size: 28px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

.value-positive {
  color: rgba(34, 197, 94, 0.9);
}

.value-negative {
  color: rgba(239, 68, 68, 0.9);
}

.metric-subtitle {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 8px;
}
</style>


