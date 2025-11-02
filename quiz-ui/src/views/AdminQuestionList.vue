<template>
  <div class="max-w-3xl mx-auto mt-10 p-6 bg-gray-50 rounded-lg shadow-md">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Liste des Questions</h2>
      <div class="flex items-center gap-3">
        <button @click="openGenerator = true" class="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 transition">Générer (IA)</button>
        <button @click="goToCreateQuestion" class="bg-main-violet text-white px-4 py-2 rounded-md hover:bg-[#A48FD0] transition">Créer une question</button>
      </div>
    </div>

    <div v-if="openGenerator" class="fixed inset-0 z-40 flex items-center justify-center bg-black/50">
      <div class="bg-white rounded-lg shadow-lg w-full max-w-3xl p-6 max-h-[85vh] flex flex-col">
        <h3 class="text-xl font-semibold mb-4">Générer des questions depuis un texte</h3>
        <div class="space-y-3 mb-4">
          <label class="block text-sm font-medium">Texte source :</label>
          <textarea v-model="sourceText" rows="6" class="w-full border px-3 py-2 rounded" placeholder="Colle ici le texte depuis lequel générer des questions..."></textarea>

          <div class="flex items-center gap-4">
            <div>
              <label class="block text-sm">Nombre de questions</label>
              <input v-model.number="count" type="number" min="1" max="10" class="w-24 border px-2 py-1 rounded" />
            </div>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="autoInsert" />
              <span class="text-sm">Insérer automatiquement dans la base</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="autoImage" />
              <span class="text-sm">Chercher une image et convertir en base64</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="prettyJson" />
              <span class="text-sm">Afficher JSON modifiable pour prévisualisation</span>
            </label>
          </div>
        </div>

        <div class="flex justify-end gap-2">
          <button @click="openGenerator = false" class="px-4 py-2 rounded border">Annuler</button>
          <button @click="generateQuestions" :disabled="generating || !sourceText" class="px-4 py-2 rounded bg-main-violet text-white">{{ generating ? 'Génération...' : 'Générer' }}</button>
        </div>

        <div v-if="generatedQuestions.length" class="mt-4 flex-1 overflow-y-auto pr-2">
          <h4 class="font-semibold mb-2">Questions générées</h4>
          <div v-for="(q, idx) in generatedQuestions" :key="idx" class="mb-4 border rounded p-3 bg-gray-50">
            <div class="flex justify-between items-start">
              <strong>Question {{ idx + 1 }}</strong>
              <button @click="removeGenerated(idx)" class="text-red-600">Supprimer</button>
            </div>
            <div class="mt-2">
              <label class="text-sm">Titre</label>
              <input v-model="q.title" class="w-full border px-2 py-1 rounded mt-1" />
            </div>
            <div class="mt-2">
              <label class="text-sm">Texte</label>
              <textarea v-model="q.text" rows="2" class="w-full border px-2 py-1 rounded mt-1"></textarea>
            </div>
            <div class="mt-2">
              <label class="text-sm">Image</label>
              <div class="flex items-center gap-3 mt-1">
                <div class="w-32 h-20 bg-white border rounded flex items-center justify-center overflow-hidden">
                  <img v-if="q.image" :src="q.image" alt="aperçu" class="object-contain max-w-full max-h-full" />
                  <span v-else class="text-xs text-gray-400">Aucune</span>
                </div>
                <button type="button" @click="regenerateImage(idx)" class="px-3 py-1 border rounded">Chercher image</button>
                <button type="button" @click="q.image = null" class="px-3 py-1 border rounded">Retirer</button>
              </div>
            </div>
            <div class="mt-2">
              <label class="text-sm">Réponses (JSON)</label>
              <textarea v-model="q.possibleAnswersJson" rows="3" class="w-full border px-2 py-1 rounded mt-1"></textarea>
              <p class="text-xs text-gray-500 mt-1">Format : [{"text":"...","isCorrect":true}, ...]</p>
            </div>
          </div>
        </div>
        <div v-if="generatedQuestions.length" class="mt-3 flex justify-end gap-2">
          <button @click="applyGeneratedToBackend" class="px-4 py-2 rounded bg-green-600 text-white" :disabled="inserting">{{ inserting ? 'Insertion...' : (autoInsert ? 'Insérer dans la base' : 'Insérer sélectionnées') }}</button>
        </div>
      </div>
    </div>

    <ul class="space-y-4">
      <li v-for="question in questions" :key="question.id" @click="goToQuestionDetail(question.id)" class="p-4 bg-white border border-gray-200 rounded-md shadow hover:shadow-lg cursor-pointer transition">
        <h3 class="text-lg font-semibold text-gray-800 mb-1">{{ question.title }}</h3>
        <p class="text-gray-600">{{ question.text }}</p>
      </li>
    </ul>

    <div v-if="questions.length === 0" class="text-gray-500 mt-4">
      Aucune question disponible.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import QuizApiService from '@/services/QuizApiService'
import { toDataUrl, findImageUrl } from '@/utils/image'
import { normalizeAnswers } from '@/utils/normalize'

const questions = ref([])
const router = useRouter()

const openGenerator = ref(false)
const sourceText = ref('')
const count = ref(3)
const autoInsert = ref(true)
const autoImage = ref(true)
const prettyJson = ref(true)
const generating = ref(false)
const inserting = ref(false)
const generatedQuestions = ref([])

onMounted(async () => {
  await loadQuestions()
})

async function loadQuestions() {
  try {
    questions.value = await QuizApiService.getAllQuestions()
  } catch (error) {
    console.error('Erreur de connexion au serveur', error)
  }
}

function goToCreateQuestion() {
  router.push('/admin/questions/create')
}

function goToQuestionDetail(id) {
  router.push(`/admin/questions/${id}`)
}

function removeGenerated(idx) {
  generatedQuestions.value.splice(idx, 1)
}

async function generateQuestions() {
  if (!sourceText.value) return
  generating.value = true
  generatedQuestions.value = []
  try {
    const payload = { text: sourceText.value, count: count.value, autoInsert: autoInsert.value }
    const data = await QuizApiService.generateQuestions(payload)

    if (data.inserted) {
      alert(`Questions insérées (${data.inserted.length})`)
      await loadQuestions()
      openGenerator.value = false
      return
    }

    const parsed = data
    generatedQuestions.value = parsed.map((q) => {
      const possibleAnswers = q.possibleAnswers || []
      return {
        title: q.title || (q.text ? q.text.slice(0, 60) : 'Question'),
        text: q.text || '',
        image: q.image || null,
        possibleAnswersJson: JSON.stringify(possibleAnswers, null, 2),
      }
    })

    if (autoImage.value) {
      for (let i = 0; i < generatedQuestions.value.length; i++) {
        try {
          const q = generatedQuestions.value[i]
          if (!q.image) {
            const keyword = (q.title || q.text || 'quiz').slice(0, 80)
            const url = await findImageUrl(keyword)
            if (url) {
              q.image = await toDataUrl(url)
            }
          } else if (!/^data:/.test(q.image) && !/^https?:\/\//i.test(q.image)) {
            const url = await findImageUrl(String(q.image).slice(0, 80))
            if (url) {
              q.image = await toDataUrl(url)
            }
          } else if (/^https?:\/\//i.test(q.image)) {
            q.image = await toDataUrl(q.image)
          }
        } catch (e) {
          console.warn('Image fetch failed for question', i, e)
        }
      }
    }
  } catch (err) {
    alert('Erreur génération IA: ' + (err.message || err))
    console.error(err)
  } finally {
    generating.value = false
  }
}

async function regenerateImage(idx) {
  const q = generatedQuestions.value[idx]
  const keyword = (q.title || q.text || 'quiz').slice(0, 80)
  try {
    const url = await findImageUrl(keyword)
    if (url) q.image = await toDataUrl(url)
    else alert('Aucune image trouvée pour: ' + keyword)
  } catch (e) {
    alert('Recherche image échouée: ' + (e.message || e))
  }
}

async function applyGeneratedToBackend() {
  if (!generatedQuestions.value.length) return
  inserting.value = true
  try {
    let startPos = 1
    try {
      const info = await QuizApiService.getQuizInfo()
      startPos = (info?.size || 0) + 1
    } catch {}

    let currentPos = startPos
    for (const q of generatedQuestions.value) {
      let answers = []
      try {
        answers = JSON.parse(q.possibleAnswersJson)
      } catch (e) {
        console.warn('Réponses invalides pour une question, skip')
        continue
      }
      answers = normalizeAnswers(answers)
      if (answers.length === 0) {
        answers = [
          { text: 'Oui', isCorrect: true },
          { text: 'Non', isCorrect: false }
        ]
      }

      const safeTitle = (q.title && String(q.title).trim()) || 'Question'
      const safeText = (q.text && String(q.text).trim()) || safeTitle

      const payload = {
        position: currentPos++,
        title: safeTitle,
        text: safeText,
        image: q.image || null,
        possibleAnswers: answers
      }

      try {
        await QuizApiService.insertQuestion(payload)
      } catch (e) {
        console.error('Erreur insertion question:', e, '\nPayload:', payload)
      }
    }

    await loadQuestions()
    generatedQuestions.value = []
    openGenerator.value = false
    alert('Questions insérées (ou envoyées) avec succès.')
  } catch (e) {
    alert('Erreur insertion: ' + (e.message || e))
    console.error(e)
  } finally {
    inserting.value = false
  }
}
</script>