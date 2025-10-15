<template>
    <div class="question-list-container">
        <h2>Liste des Questions</h2>
        <button @click="goToCreateQuestion">Créer une question</button>
        <ul>
            <li
                v-for="question in questions"
                :key="question.id"
                @click="goToQuestionDetail(question.id)"
                style="cursor: pointer; margin: 10px 0; padding: 5px; border: 1px solid black;"
            >
                {{ question.title }}
            </li>
        </ul>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const questions = ref([
    { id: 1, title: 'Quel est le type de pikachu' },
    { id: 2, title: 'Combien de dégats inflige déflagration ?' },
    { id: 3, title: 'Quelle est l\'évolution de abo ?' }
])

const router = useRouter()

function goToCreateQuestion() {
    router.push('/questions/create')
}

function goToQuestionDetail(id) {
    router.push(`/questions/${id}`)
}
</script>

<style scoped>
.question-list-container {
    max-width: 600px;
    margin: 40px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background: #f5f5f5;
    font-family: sans-serif;
    text-align: center;
}


h2 {
    font-size: 22px;
    margin-bottom: 15px;
    color: #000000;
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
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: left;
    transition: background-color 0.2s;
    color: #000;
}

li:hover {
    background-color: #f0f0f0;
}
</style>