export async function toDataUrl(url) {
  const resp = await fetch(url)
  const blob = await resp.blob()
  return await new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(blob)
  })
}

export async function findImageUrl(keyword) {
  async function tryWikipedia(lang) {
    try {
      const api = `https://${lang}.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&piprop=thumbnail&pithumbsize=800&generator=search&gsrlimit=1&gsrsearch=${encodeURIComponent(keyword)}&origin=*`
      const r = await fetch(api)
      const j = await r.json()
      if (j?.query?.pages) {
        const first = Object.values(j.query.pages)[0]
        const thumb = first?.thumbnail?.source
        if (thumb) return thumb
      }
    } catch (e) {
    }
    return null
  }

  let url = await tryWikipedia('fr')
  if (url) return url
  url = await tryWikipedia('en')
  if (url) return url

  try {
    const api = `https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&generator=search&gsrnamespace=6&gsrlimit=1&gsrsearch=${encodeURIComponent(keyword)}&origin=*`
    const r = await fetch(api)
    const j = await r.json()
    if (j?.query?.pages) {
      const first = Object.values(j.query.pages)[0]
      const u = first?.imageinfo?.[0]?.url
      if (u) return u
    }
  } catch (e) {
  }

  return `https://picsum.photos/seed/${encodeURIComponent(keyword)}/800/600`
}
