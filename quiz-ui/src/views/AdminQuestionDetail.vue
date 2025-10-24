<template>
    <div class="question-detail-container" v-if="question">
        <h2>Détail de la Question</h2>
        <div class="question-actions">
            <button @click="goToEditQuestion" class="edit-button">Éditer</button>
            <button @click="deleteQuestion" class="delete-button">Supprimer</button>
        </div>
        <div class="question-content">
            <h3>{{ question.title }}</h3>
            <p>{{ question.text }}</p>
            <ul>
                <li
                    v-for="(answer, index) in question.possibleAnswers"
                    :key="index"
                    :class="{ correct: answer.isCorrect }"
                >
                    <input
                        type="radio"
                        :name="'answer-' + question.id"
                        :checked="answer.isCorrect"
                        disabled
                    />
                    {{ answer.text }}
                </li>
            </ul>
        </div>
    </div>
    <div v-else>
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

async function deleteQuestion() {
  try {
    const res = await fetch(`http://127.0.0.1:5000/questions/${questionId}`, { method: 'DELETE' })
    
    if (res.ok) {
      alert('Question supprimée avec succès')
      router.push('/admin')
    } else {
      alert('Erreur lors de la suppression de la question')
    }
  } catch (error) {
    console.error('Erreur lors de la suppression de la question', error)
  }
}
</script>

<style scoped>
.question-detail-container {
    max-width: 600px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #f9f9f9;
    font-family: sans-serif;
}

h2 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
    text-align: center;
}

.question-actions {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.edit-button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.edit-button:hover {
    background-color: #0056b3;
}

.delete-button {
    padding: 8px 16px;
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.delete-button:hover {
    background-color: #c82333;
}

.question-content h3 {
    font-size: 20px;
    margin-bottom: 10px;
    color: #444;
}

.question-content p {
    font-size: 16px;
    margin-bottom: 20px;
    color: #555;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    margin-bottom: 10px;
    display: flex;
    align-items: center;
}

input[type='radio'] {
    margin-right: 10px;
}

.correct {
    font-weight: bold;
    color: green;
}
</style>