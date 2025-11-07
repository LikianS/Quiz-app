<template>
  <div class="max-w-3xl mx-auto mt-12 p-6 bg-white rounded-xl shadow-md" v-if="question">
    <h2 class="text-2xl font-semibold text-center text-gray-800 mb-6">Détail de la Question</h2>

    <div class="flex justify-end gap-4 mb-6">
      <button @click="goBack" class="bg-main-violet text-white px-4 py-2 rounded-md hover:bg-[#A48FD0] transition">Retour</button>
      <button @click="goToEditQuestion" class="bg-main-violet text-white px-4 py-2 rounded-md hover:bg-[#A48FD0] transition">Éditer</button>
      <button @click="deleteQuestion" class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition">Supprimer</button>
    </div>

    <div class="space-y-4">
      <h3 class="text-xl font-semibold text-gray-700">{{ question.title }}</h3>
      <p class="text-gray-600">{{ question.text }}</p>

      <ul class="space-y-2">
        <li v-for="(answer, index) in question.possibleAnswers" :key="index" :class="['flex items-center p-3 border rounded-md', answer.isCorrect ? 'border-green-500 bg-green-50 font-semibold text-green-700' : 'border-gray-200 bg-white']">
          <input type="radio" :name="'answer-' + question.id" :checked="answer.isCorrect" disabled class="mr-3"/>
          {{ answer.text }}
        </li>
      </ul>
    </div>
  </div>

  <div v-else class="text-center text-gray-500 mt-12">
    <p>Chargement des données...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const route = useRoute()
const router = useRouter()
const question = ref(null)
const questionId = String(route.params.id)

onMounted(async () => {
  try {
    const res = await fetch(`http://127.0.0.1:5000/questions/${questionId}`)
    if (res.ok) {
      question.value = await res.json()
    } else {
      console.error('Erreur lors de la récupération de la question')
    }
  } catch (error) {
    console.error('Erreur de connexion au serveur', error)
  }
})

function goToEditQuestion() {
  router.push(`/admin/questions/${questionId}/edit`)
}

function goBack() {
  router.push(`/admin`)
}

async function deleteQuestion() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('Vous devez être connecté en tant qu\'admin pour supprimer une question.');
    return;
  }
  try {
    const res = await fetch(`http://127.0.0.1:5000/questions/${questionId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (res.ok) {
      alert('Question supprimée avec succès');
      router.push('/admin');
    } else {
      alert('Erreur lors de la suppression de la question');
    }
  } catch (error) {
    console.error('Erreur lors de la suppression de la question', error);
  }
}
</script>
