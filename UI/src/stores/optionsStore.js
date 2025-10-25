import { reactive } from 'vue'

const state = reactive({
  emotions: ['Confianza', 'Ansiedad', 'Miedo', 'Avaricia', 'Calma', 'Impulsividad', 'Recuperar'],
  confirmations: ['CISD', 'FVG', 'IFVG', 'Avaricia', 'Calma', 'Impulsividad']
})

function addTag(type, value) {
  const list = state[type]
  if (!list) return
  const v = String(value || '').trim()
  if (!v) return
  if (!list.includes(v)) list.push(v)
}

function removeTag(type, value) {
  const list = state[type]
  if (!list) return
  const i = list.indexOf(value)
  if (i >= 0) list.splice(i, 1)
}

export function useOptionsStore() {
  return { state, addTag, removeTag }
}
