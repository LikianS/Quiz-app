export function normalizeAnswers(arr) {
  if (!Array.isArray(arr)) return []
  const out = []
  for (const item of arr) {
    if (item == null) continue
    if (typeof item === 'string') {
      out.push({ text: item, isCorrect: false })
      continue
    }
    if (typeof item === 'object') {
      const text = item.text ?? item.label ?? item.value ?? item.answer ?? ''
      let isCorrect = item.isCorrect
      if (typeof isCorrect !== 'boolean') {
        if (typeof item.correct === 'boolean') isCorrect = item.correct
        else if (typeof item.is_correct === 'boolean') isCorrect = item.is_correct
        else if (typeof item.right === 'boolean') isCorrect = item.right
        else if (typeof item.correct === 'string') isCorrect = item.correct.toLowerCase() === 'true'
        else if (typeof item.isCorrect === 'string') isCorrect = item.isCorrect.toLowerCase() === 'true'
        else isCorrect = false
      }
      out.push({ text: String(text ?? ''), isCorrect: Boolean(isCorrect) })
    }
  }
  if (!out.some(a => a.isCorrect) && out.length > 0) {
    out[0].isCorrect = true
  }
  return out.filter(a => a.text && a.text.trim().length > 0)
}
