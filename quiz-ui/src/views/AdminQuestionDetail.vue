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
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'


const questions = [
    {
        id: 1,
        title: 'Quelle est la capitale de la France ?',
        intitule: 'Choisissez la bonne réponse parmi les options ci-dessous.',
        answers: ['Paris', 'Londres', 'Berlin', 'Madrid'],
        correctAnswerIndex: 0
    },
    {
        id: 2,
        title: 'Combien font 2 + 2 ?',
        intitule: 'Choisissez la bonne réponse.',
        answers: ['3', '4', '5', '6'],
        correctAnswerIndex: 1
    }
]

const route = useRoute()
const router = useRouter()


const questionId = parseInt(route.params.id, 10)
const question = ref(questions.find((q) => q.id === questionId))


function goToEditQuestion() {
    router.push(`/questions/${questionId}/edit`)
}


function deleteQuestion() {
    const index = questions.findIndex((q) => q.id === questionId)
    if (index !== -1) {
        questions.splice(index, 1)
    }
    router.push('/questions') 
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