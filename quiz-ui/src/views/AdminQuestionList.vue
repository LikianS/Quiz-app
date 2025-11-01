<template>
  <div class="max-w-3xl mx-auto mt-10 p-6 bg-gray-50 rounded-lg shadow-md">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Liste des Questions</h2>
      <div class="flex items-center gap-3">
        <button @click="openGenerator = true" class="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 transition">Générer (IA)</button>
        <button @click="goToCreateQuestion" class="bg-main-violet text-white px-4 py-2 rounded-md hover:bg-[#A48FD0] transition">Créer une question</button>
      </div>
    </div>

    <!-- Generator modal -->
    <div v-if="openGenerator" class="fixed inset-0 z-40 flex items-center justify-center bg-black/50">
      <div class="bg-white rounded-lg shadow-lg w-full max-w-3xl p-6">
        <h3 class="text-xl font-semibold mb-4">Générer des questions depuis un texte (IA)</h3>
        <div class="space-y-3 mb-4">
          <label class="block text-sm font-medium">Clé OpenAI (sécurise-la) :</label>
          <input v-model="openAiKey" type="password" class="w-full border px-3 py-2 rounded" placeholder="sk-... (clé API)" />

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
              <input type="checkbox" v-model="prettyJson" />
              <span class="text-sm">Afficher JSON modifiable pour prévisualisation</span>
            </label>
          </div>
        </div>

        <div class="flex justify-end gap-2">
          <button @click="openGenerator = false" class="px-4 py-2 rounded border">Annuler</button>
          <button @click="generateQuestions" :disabled="generating || !sourceText" class="px-4 py-2 rounded bg-main-violet text-white">{{ generating ? 'Génération...' : 'Générer' }}</button>
        </div>

        <!-- Generated preview -->
        <div v-if="generatedQuestions.length" class="mt-6">
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
              <label class="text-sm">Réponses (JSON)</label>
              <textarea v-model="q.possibleAnswersJson" rows="3" class="w-full border px-2 py-1 rounded mt-1"></textarea>
              <p class="text-xs text-gray-500 mt-1">Format : [{"text":"...","isCorrect":true}, ...]</p>
            </div>
          </div>

          <div class="flex justify-end gap-2">
            <button @click="applyGeneratedToBackend" class="px-4 py-2 rounded bg-green-600 text-white" :disabled="inserting">{{ inserting ? 'Insertion...' : (autoInsert ? 'Insérer dans la base' : 'Insérer sélectionnées') }}</button>
          </div>
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

const questions = ref([])
const router = useRouter()

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/questions/all')
    if (res.ok) {
      questions.value = await res.json()
    } else {
      console.error('Erreur lors de la récupération des questions')
    }
  } catch (error) {
    console.error('Erreur de connexion au serveur', error)
  }
})

function goToCreateQuestion() {
  router.push('/admin/questions/create')
}

function goToQuestionDetail(id) {
  router.push(`/admin/questions/${id}`)
}
</script>