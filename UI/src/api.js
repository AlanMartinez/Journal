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
