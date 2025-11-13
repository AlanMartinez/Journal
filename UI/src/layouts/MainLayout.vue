<template>
  <div class="layout-container">
    <Sidebar />
    <main class="main-content" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Sidebar from '../components/Sidebar.vue'

const sidebarCollapsed = ref(false)

function handleSidebarToggle(event) {
  sidebarCollapsed.value = event.detail.collapsed
}

onMounted(() => {
  window.addEventListener('sidebar-toggle', handleSidebarToggle)
})

onBeforeUnmount(() => {
  window.removeEventListener('sidebar-toggle', handleSidebarToggle)
})
</script>

<style scoped>
.layout-container {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 320px;
  min-height: 100vh;
  width: calc(100% - 320px);
  transition: margin-left 0.3s ease, width 0.3s ease;
}

.main-content.sidebar-collapsed {
  margin-left: 80px;
  width: calc(100% - 80px);
}

/* Responsive: Hide sidebar on smaller screens if needed */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .main-content.sidebar-collapsed {
    margin-left: 0;
    width: 100%;
  }
}
</style>

