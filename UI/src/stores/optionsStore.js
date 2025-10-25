import { reactive } from 'vue'
import { getEmotions, getConfirmations, createEmotion, deleteEmotion, createConfirmation, deleteConfirmation } from '../api'

const state = reactive({
  emotions: [],
  confirmations: [],
  loading: false,
  error: null,
})

async function loadAll() {
  try {
    state.loading = true
    const [emotions, confirmations] = await Promise.all([
      getEmotions(),
      getConfirmations()
    ])
    // API puede devolver objetos {id,name,description}
    state.emotions = (emotions || []).map(e => e.name || e)
    state.confirmations = (confirmations || []).map(c => c.name || c)
  } catch (e) {
    state.error = e?.message || String(e)
  } finally {
    state.loading = false
  }
}

async function addTag(type, value) {
  const v = String(value || '').trim()
  if (!v) return
  if (type === 'emotions') await createEmotion({ name: v })
  else if (type === 'confirmations') await createConfirmation({ name: v })
  await loadAll()
}

async function removeTag(type, value) {
  if (type === 'emotions') {
    const list = await getEmotions()
    const item = (list || []).find(e => (e.name || e) === value)
    if (item && item.id) await deleteEmotion(item.id)
  } else if (type === 'confirmations') {
    const list = await getConfirmations()
    const item = (list || []).find(c => (c.name || c) === value)
    if (item && item.id) await deleteConfirmation(item.id)
  }
  await loadAll()
}

export function useOptionsStore() {
  return { state, loadAll, addTag, removeTag }
}
