<template>
  <aside class="sidebar" :class="{ 'sidebar-collapsed': isCollapsed }">
    <!-- Toggle Button -->
    <button class="sidebar-toggle" @click="toggleCollapse" :title="isCollapsed ? 'Expandir' : 'Colapsar'">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="isCollapsed ? 'M9 5l7 7-7 7' : 'M15 19l-7-7 7-7'" />
      </svg>
    </button>

    <!-- Header with User Initials -->
    <div class="sidebar-header">
      <div class="relative">
        <div 
          class="user-initials cursor-pointer"
          @click="toggleDropdown"
          role="button"
          tabindex="0"
          @keydown.enter="toggleDropdown"
          @keydown.space.prevent="toggleDropdown"
        >
          {{ userInitials }}
        </div>
        
        <!-- Dropdown Menu -->
        <div 
          v-if="showDropdown"
          class="dropdown-menu"
          @click.stop
        >
          <button 
            @click="handleExport"
            :disabled="isExporting"
            class="dropdown-item"
            title="Exportar datos"
            aria-label="Exportar datos"
          >
            <svg v-if="!isExporting" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="dropdown-item-text">
              {{ isExporting ? 'Exportando...' : 'Exportar datos' }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Navigation Items -->
    <nav class="sidebar-nav">
      <router-link 
        v-for="item in navItems" 
        :key="item.name"
        :to="item.path" 
        class="nav-item"
        active-class="nav-item-active"
        :title="isCollapsed ? item.label : ''"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path :d="item.icon" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
        </svg>
        <span class="nav-item-text" v-show="!isCollapsed">{{ item.label }}</span>
      </router-link>
    </nav>

    <!-- Footer with Live/Dismiss Button and Time -->
    <div class="sidebar-footer">
      <button
        @click="handleLogout"
        class="live-button live-on"
      >
        <span class="pulse-dot"></span>
        <span class="live-text">
          <span class="live-default">LIVE</span>
          <span class="live-hover">DISMISS</span>
        </span>
      </button>
      
      <!-- Time Display with Sessions Table -->
      <div class="time-container" v-show="!isCollapsed">
        <div 
          class="current-time metric-mono text-sm text-white/70 cursor-pointer transition-colors hover:text-white"
          @mouseenter="showTimeDropdown = true"
          @mouseleave="showTimeDropdown = false"
        >
          {{ currentTime }}
        </div>
        
        <!-- Time Dropdown with Sessions -->
        <div 
          v-if="showTimeDropdown"
          class="time-dropdown"
          @mouseenter="showTimeDropdown = true"
          @mouseleave="showTimeDropdown = false"
        >
          <table class="sessions-table">
            <thead>
              <tr>
                <th>Sesión</th>
                <th>Horario</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="session in tradingSessions" 
                :key="session.id"
                :class="{ 'session-active': session.isActive, 'session-inactive': !session.isActive }"
              >
                <td class="session-name">{{ session.name }}</td>
                <td class="session-time">{{ session.timeRange }}</td>
                <td class="session-status">
                  <span v-if="session.isActive" class="status-badge active">EN CURSO</span>
                  <span v-else class="status-badge inactive">CERRADA</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'
import { exportAllData } from '../api'

const authStore = useAuthStore()
const router = useRouter()

const isExporting = ref(false)
const showDropdown = ref(false)
const isCollapsed = ref(false)
const currentTime = ref('')
const showTimeDropdown = ref(false)
let timeInterval = null

// Navigation items configuration
const navItems = [
  {
    name: 'Dashboard',
    path: '/dashboard',
    label: 'Dashboard',
    icon: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6'
  },
  {
    name: 'Statistics',
    path: '/statistics',
    label: 'Statistics',
    icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
  }
]

// Computed: Get user initials
const userInitials = computed(() => {
  const user = authStore.currentUser
  if (!user || !user.name) return 'AM'
  
  const nameParts = user.name.trim().split(' ')
  if (nameParts.length >= 2) {
    // First letter of first name + first letter of last name
    return (nameParts[0][0] + nameParts[nameParts.length - 1][0]).toUpperCase()
  } else if (nameParts.length === 1) {
    // Only one name, use first two letters
    return nameParts[0].substring(0, 2).toUpperCase()
  }
  return 'AM'
})

// Handle logout directly
async function handleLogout() {
  try {
    await authStore.logout()
    router.push('/login')
  } catch (err) {
    console.error('Error en logout:', err)
    // Even if there's an error, redirect to login
    router.push('/login')
  }
}

// Toggle dropdown
function toggleDropdown() {
  showDropdown.value = !showDropdown.value
}

// Close dropdown when clicking outside
function handleClickOutside(event) {
  const target = event.target
  const userInitialsEl = document.querySelector('.sidebar .user-initials')
  const dropdownEl = document.querySelector('.sidebar .dropdown-menu')
  
  if (userInitialsEl && !userInitialsEl.contains(target) && 
      dropdownEl && !dropdownEl.contains(target)) {
    showDropdown.value = false
  }
}

// Handle export
async function handleExport() {
  if (isExporting.value) return
  
  try {
    isExporting.value = true
    showDropdown.value = false // Close dropdown when exporting
    
    const data = await exportAllData()
    
    // Crear un blob con los datos JSON
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    
    // Crear un enlace temporal para descargar
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    
    // Nombre del archivo con la fecha actual
    const date = new Date().toISOString().split('T')[0]
    link.download = `trade-journal-export-${date}.json`
    
    // Trigger download
    document.body.appendChild(link)
    link.click()
    
    // Cleanup
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
  } catch (e) {
    console.error('Error exporting data:', e)
  } finally {
    isExporting.value = false
  }
}

// Toggle sidebar collapse
function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value
  // Emit event or store state for MainLayout
  const event = new CustomEvent('sidebar-toggle', { detail: { collapsed: isCollapsed.value } })
  window.dispatchEvent(event)
}

// Update current time in UTC-4
function updateTime() {
  const now = new Date()
  // Convert to UTC-4 (subtract 4 hours from UTC)
  const utcMinus4 = new Date(now.getTime() - (4 * 60 * 60 * 1000))
  const hours = String(utcMinus4.getUTCHours()).padStart(2, '0')
  const minutes = String(utcMinus4.getUTCMinutes()).padStart(2, '0')
  const seconds = String(utcMinus4.getUTCSeconds()).padStart(2, '0')
  currentTime.value = `${hours}:${minutes}:${seconds}`
}

// Get current time in GMT/UTC
function getCurrentGMTTime() {
  const now = new Date()
  const gmtHours = now.getUTCHours()
  const gmtMinutes = now.getUTCMinutes()
  return { hours: gmtHours, minutes: gmtMinutes, dayOfWeek: now.getUTCDay() }
}

// Convert GMT time to minutes for easier comparison
function timeToMinutes(hours, minutes) {
  return hours * 60 + minutes
}

// Check if a session is active
function isSessionActive(startTime, endTime, days = [1, 2, 3, 4, 5]) {
  const current = getCurrentGMTTime()
  const currentDay = current.dayOfWeek // 0 = Sunday, 1 = Monday, etc.
  const currentMinutes = timeToMinutes(current.hours, current.minutes)
  
  // Check if current day is in allowed days
  if (!days.includes(currentDay)) {
    return false
  }
  
  const startMinutes = timeToMinutes(startTime.hours, startTime.minutes)
  let endMinutes = timeToMinutes(endTime.hours, endTime.minutes)
  
  // Handle sessions that span across midnight
  if (endMinutes < startMinutes) {
    // Session spans midnight
    return currentMinutes >= startMinutes || currentMinutes < endMinutes
  } else {
    return currentMinutes >= startMinutes && currentMinutes < endMinutes
  }
}

// Computed: Trading sessions with active status
const tradingSessions = computed(() => {
  const currentGMT = getCurrentGMTTime()
  
  // NY Session: 9:30-16:00 EST (Eastern Time is UTC-5 in winter, UTC-4 in summer)
  const nyStartGMT = { hours: 14, minutes: 30 } // 9:30 EST = 14:30 GMT (UTC-5)
  const nyEndGMT = { hours: 21, minutes: 0 } // 16:00 EST = 21:00 GMT
  const nyActive = isSessionActive(nyStartGMT, nyEndGMT, [1, 2, 3, 4, 5])
  
  // LN Session: 9:00-16:00 GMT (Monday-Friday)
  const lnStartGMT = { hours: 9, minutes: 0 }
  const lnEndGMT = { hours: 16, minutes: 0 }
  const lnActive = isSessionActive(lnStartGMT, lnEndGMT, [1, 2, 3, 4, 5])
  
  // AS Session: 22:00 GMT - 9:00 GMT next day (spans midnight)
  const asStartGMT = { hours: 22, minutes: 0 }
  const asEndGMT = { hours: 9, minutes: 0 }
  const currentMinutes = timeToMinutes(currentGMT.hours, currentGMT.minutes)
  const asStartMinutes = timeToMinutes(22, 0)
  const asEndMinutes = timeToMinutes(9, 0)
  const asActive = (currentGMT.dayOfWeek >= 1 && currentGMT.dayOfWeek <= 5) && 
                   (currentMinutes >= asStartMinutes || currentMinutes < asEndMinutes)
  
  return [
    {
      id: 'ny',
      name: 'Nueva York (NY)',
      timeRange: '9:30 - 16:00 EST',
      isActive: nyActive
    },
    {
      id: 'ln',
      name: 'Londres (LN)',
      timeRange: '9:00 - 16:00 GMT',
      isActive: lnActive
    },
    {
      id: 'as',
      name: 'Asiática (AS)',
      timeRange: '22:00 - 9:00 GMT',
      isActive: asActive
    }
  ]
})

// Initialize and cleanup
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style scoped>
.sidebar {
  width: 320px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background: rgba(var(--panel) / 0.75);
  backdrop-filter: blur(20px) saturate(180%);
  border-right: 1px solid rgba(var(--accent-cyan) / 0.12);
  box-shadow: 4px 0 30px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  z-index: 40;
  transition: width 0.3s ease, background 0.3s ease;
}

.sidebar-collapsed {
  width: 80px;
}

.sidebar-toggle {
  position: absolute;
  top: 16px;
  right: -12px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(var(--panel) / 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(var(--accent-cyan) / 0.2);
  color: rgba(var(--accent-cyan) / 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 50;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.sidebar-toggle:hover {
  background: rgba(var(--panel) / 1);
  border-color: rgba(var(--accent-cyan) / 0.4);
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(var(--accent-cyan) / 0.3);
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid rgba(var(--accent-cyan) / 0.1);
  display: flex;
  justify-content: center;
  transition: padding 0.3s ease;
}

.sidebar-collapsed .sidebar-header {
  padding: 24px 12px;
}

.user-initials {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(var(--accent-cyan) / 1), rgba(170, 135, 245, 0.92));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 24px;
  color: #0f0f17;
  box-shadow: 0 8px 24px rgba(var(--accent-cyan) / 0.3);
  border: 2px solid rgba(var(--accent-cyan) / 0.4);
  flex-shrink: 0;
  transition: all 0.2s ease;
  user-select: none;
}

.user-initials:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 30px rgba(var(--accent-cyan) / 0.4);
}

.user-initials:active {
  transform: scale(0.98);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 15, 23, 0.98);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(var(--accent-cyan) / 0.3);
  border-radius: 12px;
  padding: 8px;
  min-width: 180px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.5),
    0 0 24px rgba(var(--accent-cyan) / 0.15);
  z-index: 1000;
  animation: dropdownFadeIn 0.2s ease;
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.9);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.dropdown-item:hover:not(:disabled) {
  background: rgba(var(--accent-cyan) / 0.1);
  color: rgba(255, 255, 255, 1);
}

.dropdown-item:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.dropdown-item-text {
  flex: 1;
}

.sidebar-nav {
  flex: 1;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
  transition: padding 0.3s ease;
}

.sidebar-collapsed .sidebar-nav {
  padding: 24px 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 12px;
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  position: relative;
  justify-content: center;
}

.sidebar:not(.sidebar-collapsed) .nav-item {
  justify-content: flex-start;
}

.nav-item:hover {
  background: rgba(var(--accent-cyan) / 0.08);
  color: rgba(255, 255, 255, 0.9);
}

.nav-item-active {
  background: rgba(var(--accent-cyan) / 0.15);
  color: rgba(var(--accent-cyan) / 1);
  border-left: 3px solid rgba(var(--accent-cyan) / 1);
  padding-left: 17px;
}

.nav-item-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, rgba(var(--accent-cyan) / 1), rgba(170, 135, 245, 0.8));
  border-radius: 0 4px 4px 0;
}

.nav-item svg {
  flex-shrink: 0;
}

.nav-item-text {
  flex: 1;
}

.sidebar-footer {
  padding: 24px;
  border-top: 1px solid rgba(var(--accent-cyan) / 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.time-container {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
}

.current-time {
  font-size: 13px;
  letter-spacing: 0.05em;
  text-align: center;
  padding: 8px 12px;
  border-radius: 8px;
  background: rgba(var(--accent-cyan) / 0.05);
  border: 1px solid rgba(var(--accent-cyan) / 0.1);
  width: 100%;
  transition: all 0.2s ease;
}

.current-time:hover {
  background: rgba(var(--accent-cyan) / 0.1);
  border-color: rgba(var(--accent-cyan) / 0.2);
}

.time-dropdown {
  position: absolute;
  bottom: calc(100% + 12px);
  left: 50%;
  transform: translateX(-50%);
  background: rgba(15, 15, 23, 0.98);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(var(--accent-cyan) / 0.3);
  border-radius: 12px;
  padding: 16px;
  min-width: 320px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.5),
    0 0 24px rgba(var(--accent-cyan) / 0.15);
  z-index: 1000;
  animation: dropdownFadeIn 0.2s ease;
}

.sessions-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.sessions-table thead th {
  text-align: left;
  padding: 8px 12px;
  color: rgba(255, 255, 255, 0.6);
  font-weight: 600;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sessions-table tbody td {
  padding: 10px 12px;
  color: rgba(255, 255, 255, 0.9);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.sessions-table tbody tr:last-child td {
  border-bottom: none;
}

.session-name {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
}

.session-time {
  font-family: 'Courier New', monospace;
  color: rgba(255, 255, 255, 0.7);
  font-size: 11px;
}

.session-status {
  text-align: center;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.status-badge.inactive {
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.session-active {
  background: rgba(var(--accent-cyan) / 0.15);
  border-radius: 6px;
  position: relative;
  animation: sessionGlow 2s ease-in-out infinite;
  filter: none;
  opacity: 1;
}

.session-active::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 6px;
  padding: 1px;
  background: linear-gradient(135deg, rgba(var(--accent-cyan) / 0.6), rgba(16, 185, 129, 0.4));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  pointer-events: none;
}

@keyframes sessionGlow {
  0%, 100% {
    box-shadow: 0 0 10px rgba(var(--accent-cyan) / 0.2);
  }
  50% {
    box-shadow: 0 0 20px rgba(var(--accent-cyan) / 0.4), 0 0 30px rgba(16, 185, 129, 0.2);
  }
}

.session-inactive {
  opacity: 0.6;
  filter: blur(1.5px);
  transition: all 0.3s ease;
}

.live-button {
  position: relative;
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.1em;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
  border: 2px solid;
  cursor: pointer;
  overflow: hidden;
  min-width: 120px;
  justify-content: center;
  width: 100%;
}

.sidebar-collapsed .live-button {
  min-width: 50px;
  padding: 12px;
}

.sidebar-collapsed .live-button .live-text {
  display: none;
}

.live-button:hover {
  transform: translateY(-2px);
}

.live-on {
  background: linear-gradient(135deg, #10b981, #059669);
  border-color: rgba(16, 185, 129, 0.5);
  color: white;
  box-shadow: 
    0 0 20px rgba(16, 185, 129, 0.5),
    0 6px 20px rgba(16, 185, 129, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
  animation: live-pulse 2s ease-in-out infinite;
}

.live-on:hover {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border-color: rgba(239, 68, 68, 0.5);
  box-shadow: 
    0 0 30px rgba(239, 68, 68, 0.7),
    0 8px 25px rgba(239, 68, 68, 0.4),
    inset 0 0 20px rgba(255, 255, 255, 0.15);
  animation: none;
}

.live-on:hover .live-default {
  display: none;
}

.live-on:hover .live-hover {
  display: inline;
}

.live-on:hover .pulse-dot {
  animation: none;
  opacity: 0.7;
}

.pulse-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: white;
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
  animation: pulse 2s infinite;
  flex-shrink: 0;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(0.9);
  }
}

@keyframes live-pulse {
  0%, 100% {
    box-shadow: 
      0 0 20px rgba(16, 185, 129, 0.5),
      0 6px 20px rgba(16, 185, 129, 0.3),
      inset 0 0 20px rgba(255, 255, 255, 0.1);
  }
  50% {
    box-shadow: 
      0 0 30px rgba(16, 185, 129, 0.7),
      0 8px 25px rgba(16, 185, 129, 0.4),
      inset 0 0 25px rgba(255, 255, 255, 0.15);
  }
}

.live-text {
  position: relative;
  z-index: 1;
}

.live-default {
  display: inline;
}

.live-hover {
  display: none;
}

/* Scrollbar styling */
.sidebar-nav::-webkit-scrollbar {
  width: 6px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(var(--accent-cyan) / 0.3);
  border-radius: 3px;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--accent-cyan) / 0.5);
}
</style>

