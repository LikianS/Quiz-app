<template>
  <div>
    <h2>Éditer la question</h2>
    <form @submit.prevent="saveQuestion">
      <div>
        <label>Position :</label>
        <input type="number" v-model="question.position" />
      </div>
      <div>
        <label>Titre :</label>
        <input type="text" v-model="question.title" />
      </div>
      <div>
        <label>Intitulé :</label>
        <input type="text" v-model="question.intitule" />
      </div>
      <div>
        <label>Image :</label>
        <input type="file" @change="onImageChange" />
        <div v-if="imagePreview">
          <img :src="imagePreview" alt="aperçu" style="width:100px;" />
        </div>
      </div>
      <div>
        <p>Réponses :</p>
        <div v-for="(answer, idx) in answers" :key="idx" style="margin-bottom:8px;">
          <input type="text" v-model="answers[idx]" placeholder="Réponse" />
          <input type="checkbox" :checked="correctAnswerIndex === idx" @change="setCorrect(idx)" />
          <span>Bonne réponse</span>
        </div>
      </div>
      <button type="submit" style="margin-right:10px;">Sauvegarder</button>
      <button type="button" @click="cancelEdit">Annuler</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const questionId = route.params.id

const question = ref({ position: 1, title: '', intitule: '' })
const answers = ref(['', '', '', ''])
const correctAnswerIndex = ref(0)
const imagePreview = ref(null)
const imageFile = ref(null)

onMounted(async () => {
  const res = await fetch(`http://127.0.0.1:5000/questions/${questionId}`)
  if (res.ok) {
    const data = await res.json()
    question.value = { ...data, position: data.position || 1 }
    answers.value = typeof data.answers === 'string' ? JSON.parse(data.answers) : data.answers
    correctAnswerIndex.value = data.correctAnswerIndex ?? 0
  }
})

function setCorrect(idx) {
  correctAnswerIndex.value = idx
}

function onImageChange(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
  }
}

async function saveQuestion() {
  const payload = {
    ...question.value,
    answers: answers.value,
    correctAnswerIndex: correctAnswerIndex.value
  }
  await fetch(`http://127.0.0.1:5000/questions/${questionId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  router.push('/questions')
}

function cancelEdit() {
  router.push('/questions')
}
</script>

<style scoped>
h2 {
  color: #333;
  font-size: 20px;
  margin-bottom: 15px;
}
form {
  border: 1px solid #aaa;
  padding: 15px;
  border-radius: 6px;
  background: #fafafa;
  max-width: 400px;
  margin: 0 auto;
}
label {
  font-size: 14px;
}
input[type="text"], input[type="number"] {
  margin-bottom: 8px;
  padding: 4px;
  border: 1px solid #bbb;
  border-radius: 3px;
  width: 90%;
}
button {
  background: #eee;
  border: 1px solid #bbb;
  border-radius: 3px;
  padding: 6px 12px;
  cursor: pointer;
}
button:hover {
  background: #ddd;
}
img {
  margin-top: 5px;
  border: 1px solid #ccc;
}
</style>