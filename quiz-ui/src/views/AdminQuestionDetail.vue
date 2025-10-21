<template>
    <div class="question-detail-container">
        <h2>Détail de la Question</h2>
        <div class="question-actions">
            <button @click="goToEditQuestion" class="edit-button">Éditer</button>
            <button @click="deleteQuestion" class="delete-button">Supprimer</button>
        </div>
        <div class="question-content">
            <h3>{{ question.title }}</h3>
            <p>{{ question.intitule }}</p>
            <ul>
                <li
                    v-for="(answer, index) in question.answers"
                    :key="index"
                    :class="{ correct: index === question.correctAnswerIndex }"
                >
                    <input
                        type="radio"
                        :name="'answer-' + question.id"
                        :checked="index === question.correctAnswerIndex"
                        disabled
                    />
                    {{ answer }}
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const route = useRoute()
const router = useRouter()
const question = ref(null)
const answers = ref([])
const questionId = route.params.id

onMounted(async () => {
  const res = await fetch(`http://127.0.0.1:5000/questions/${questionId}`)
  if (res.ok) {
    const data = await res.json()
    question.value = data
    answers.value = typeof data.answers === 'string' ? JSON.parse(data.answers) : data.answers
  }
})

function goToEditQuestion() {
  router.push(`/admin/questions/${questionId}/edit`)
}

async function deleteQuestion() {
  await fetch(`http://127.0.0.1:5000/questions/${questionId}`, { method: 'DELETE' })
  router.push('/admin')
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