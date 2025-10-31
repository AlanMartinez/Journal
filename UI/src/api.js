const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function toSnakeCasePayload(payload) {
  const out = { ...payload }
  if ('tradingLink' in out) {
    out.trading_link = out.tradingLink || null
    delete out.tradingLink
  }
  return out
}

async function http(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`)
  }
  const ct = res.headers.get('content-type') || ''
  return ct.includes('application/json') ? res.json() : res.text()
}

// Trades
export async function getTrades() {
  return http('/trades')
}
export async function createTrade(trade) {
  const body = JSON.stringify(toSnakeCasePayload(trade))
  return http('/trades', { method: 'POST', body })
}

export async function updateTrade(id, trade) {
  const body = JSON.stringify(toSnakeCasePayload(trade))
  return http(`/trades/${encodeURIComponent(id)}`, { method: 'PUT', body })
}

// Emotions
export async function getEmotions() {
  return http('/emotions')
}
export async function createEmotion(data) {
  return http('/emotions', { method: 'POST', body: JSON.stringify(data) })
}
export async function deleteEmotion(id) {
  return http(`/emotions/${encodeURIComponent(id)}`, { method: 'DELETE' })
}

// Confirmations
export async function getConfirmations() {
  return http('/confirmations')
}
export async function createConfirmation(data) {
  return http('/confirmations', { method: 'POST', body: JSON.stringify(data) })
}
export async function deleteConfirmation(id) {
  return http(`/confirmations/${encodeURIComponent(id)}`, { method: 'DELETE' })
}

// Stats
export async function getTradeStatsSummary() {
  return http('/trades/stats/summary')
}

// Day Journal
export async function getDayJournals() {
  return http('/day-journal')
}

export async function getDayJournalById(id) {
  return http(`/day-journal/${encodeURIComponent(id)}`)
}

export async function createDayJournal(data) {
  return http('/day-journal', { method: 'POST', body: JSON.stringify(data) })
}

export async function updateDayJournal(id, data) {
  return http(`/day-journal/${encodeURIComponent(id)}`, { method: 'PUT', body: JSON.stringify(data) })
}

export async function deleteDayJournal(id) {
  return http(`/day-journal/${encodeURIComponent(id)}`, { method: 'DELETE' })
}

export async function getDayJournalsByDateRange(startDate, endDate) {
  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate
  })
  return http(`/day-journal/range?${params}`)
}

// Export
export async function exportAllData() {
  return http('/export/all')
}