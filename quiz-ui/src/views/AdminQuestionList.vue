<template>
  <div class="max-w-3xl mx-auto mt-10 p-6 bg-gray-50 rounded-lg shadow-md">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-800">Liste des Questions</h2>
      <button @click="goToCreateQuestion" class="bg-main-violet text-white px-4 py-2 rounded-md hover:bg-[#A48FD0] transition">Créer une question</button>
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