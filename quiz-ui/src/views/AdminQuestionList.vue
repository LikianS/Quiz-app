<template>
    <div class="question-list-container">
        <h2>Liste des Questions</h2>
        <button @click="goToCreateQuestion">Créer une question</button>
        <ul>
            <li
                v-for="question in questions"
                :key="question.id"
                class="question-item"
                @click="goToQuestionDetail(question.id)"
            >
                <h3>{{ question.title }}</h3>
                <p>{{ question.text }}</p>
            </li>
        </ul>
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

<style scoped>
.question-list-container {
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background: #f9f9f9;
    font-family: Arial, sans-serif;
}

h2 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
}

button {
    margin-bottom: 20px;
    padding: 8px 15px;
    font-size: 14px;
    color: white;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

li:hover {
    background-color: #f0f0f0;
}
</style>