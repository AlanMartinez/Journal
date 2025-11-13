<template>
  <nav class="navbar fixed top-0 left-0 right-0 z-50">
    <div class="mx-auto max-w-7xl px-6 py-4 flex items-center justify-between">
      <!-- Left: User Initials -->
      <div class="flex items-center gap-3">
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
        <span class="text-lg font-semibold text-white/90">{{ userName }}</span>
      </div>

      <!-- Right: Time and Live Button -->
      <div class="flex items-center gap-4">
        <div class="relative">
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
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'
import { exportAllData } from '../api'

const authStore = useAuthStore()
const router = useRouter()

const currentTime = ref('')
const isExporting = ref(false)
const showDropdown = ref(false)
const showTimeDropdown = ref(false)
let timeInterval = null

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

// Computed: Get user name
const userName = computed(() => {
  const user = authStore.currentUser
  if (!user || !user.name) return 'Usuario'
  return user.name.split(' ')[0]
})

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
  // For simplicity, we'll use EST = UTC-5, so 9:30 EST = 14:30 GMT
  // But since the user wants UTC-4 display, let's use EST conversion
  // EST = UTC-5, EDT = UTC-4. We'll use EST base: 9:30 EST = 14:30 GMT, 16:00 EST = 21:00 GMT
  const nyStartGMT = { hours: 14, minutes: 30 } // 9:30 EST = 14:30 GMT (UTC-5)
  const nyEndGMT = { hours: 21, minutes: 0 } // 16:00 EST = 21:00 GMT
  const nyActive = isSessionActive(nyStartGMT, nyEndGMT, [1, 2, 3, 4, 5])
  
  // LN Session: 9:00-16:00 GMT (Monday-Friday)
  const lnStartGMT = { hours: 9, minutes: 0 }
  const lnEndGMT = { hours: 16, minutes: 0 }
  const lnActive = isSessionActive(lnStartGMT, lnEndGMT, [1, 2, 3, 4, 5])
  
  // AS Session: 22:00 GMT - 9:00 GMT next day (spans midnight)
  // This session can extend into weekends for markets that trade on Saturday
  const asStartGMT = { hours: 22, minutes: 0 }
  const asEndGMT = { hours: 9, minutes: 0 }
  // Check if current time is within session (spans midnight)
  const currentMinutes = timeToMinutes(currentGMT.hours, currentGMT.minutes)
  const asStartMinutes = timeToMinutes(22, 0)
  const asEndMinutes = timeToMinutes(9, 0)
  // Session is active if after 22:00 or before 9:00 on weekdays
  // Also check if it's Monday early morning (before 9:00) from Sunday's session
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
  const userInitialsEl = document.querySelector('.user-initials')
  const dropdownEl = document.querySelector('.dropdown-menu')
  
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

// Initialize time and set interval
onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  document.addEventListener('click', handleClickOutside)
})

// Cleanup interval
onBeforeUnmount(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.user-initials {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(var(--accent-cyan) / 1), rgba(170, 135, 245, 0.92));
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 18px;
  color: #0f0f17;
  box-shadow: 0 6px 20px rgba(var(--accent-cyan) / 0.3);
  border: 2px solid rgba(var(--accent-cyan) / 0.4);
  flex-shrink: 0;
  transition: all 0.2s ease;
  user-select: none;
}

.user-initials:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 25px rgba(var(--accent-cyan) / 0.4);
}

.user-initials:active {
  transform: scale(0.98);
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
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
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
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

.current-time {
  font-size: 14px;
  letter-spacing: 0.05em;
  min-width: 80px;
  text-align: right;
}

.time-dropdown {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
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
  padding: 10px 20px;
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
  min-width: 90px;
  justify-content: center;
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

.glow-cyan {
  box-shadow: 
    0 8px 28px rgba(0,0,0,0.35), 
    0 0 24px rgba(var(--accent-cyan) / 0.15),
    inset 0 0 40px rgba(var(--accent-cyan) / 0.05);
}

.btn-danger {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  padding: 12px 24px;
  border-radius: 10px;
  border: 1px solid rgba(239, 68, 68, 0.4);
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
  font-weight: 600;
  transition: all 0.2s ease;
  cursor: pointer;
}

.btn-danger:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.4);
}
</style>

