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
        <textarea v-model="question.text" rows="3"></textarea>
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
          <input
            type="text"
            v-model="answers[idx].text"
            placeholder="Intitulé de la réponse"
          />
          <input
            type="checkbox"
            :checked="correctAnswerIndex === idx"
            @change="setCorrect(idx)"
          />
          <span>Bonne réponse</span>
        </div>
      </div>

  <button type="submit" style="margin-right:10px;">Sauvegarder</button>
  <button type="button" @click="cancelEdit" style="margin-right:10px;">Annuler</button>
  <button type="button" @click="deleteQuestion" style="background:#dc3545;">Supprimer</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import QuizApiService from '@/services/QuizApiService'

const router = useRouter()
const route = useRoute()
const questionId = route.params.id

const question = ref({ position: 1, title: '', text: '' })
const answers = ref([{ text: '', isCorrect: false }, { text: '', isCorrect: false }, { text: '', isCorrect: false }, { text: '', isCorrect: false }]) 
const correctAnswerIndex = ref(0) 
const imagePreview = ref(null) 
const imageFile = ref(null) 

onMounted(async () => {
  try {
    const data = await QuizApiService.getQuestionById(questionId)
    question.value = { 
      position: data.position || 1, 
      title: data.title || '', 
      text: data.text || '' 
    }
    answers.value = data.possibleAnswers || []
    correctAnswerIndex.value = answers.value.findIndex(answer => answer.isCorrect)
    imagePreview.value = data.image || null
  } catch (error) {
    console.error('Erreur lors de la récupération de la question', error)
  }
})

function setCorrect(idx) {
  correctAnswerIndex.value = idx
  answers.value.forEach((answer, index) => {
    answer.isCorrect = index === idx
  })
}

function onImageChange(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    imagePreview.value = URL.createObjectURL(file)
    toBase64(file).then(base64 => {
      imageFile.value.base64 = base64;
    });
  }
}

async function saveQuestion() {
  try {
    let imageBase64 = null;
    if (imageFile.value && imageFile.value.base64) {
      imageBase64 = imageFile.value.base64;
    } else {
      imageBase64 = imagePreview.value;
    }
    const payload = {
      ...question.value,
      image: imageBase64,
      possibleAnswers: answers.value,
    };
    await QuizApiService.updateQuestion(questionId, payload)
    alert('Question sauvegardée avec succès')
    router.push('/admin') 
  } catch (error) {
    console.error('Erreur lors de la sauvegarde de la question', error)
    alert('Une erreur est survenue lors de la sauvegarde')
  }
}

async function toBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

function cancelEdit() {
  router.push('/admin') 
}

async function deleteQuestion() {
  if (confirm('Voulez-vous vraiment supprimer cette question ?')) {
    try {
      await QuizApiService.deleteQuestion(questionId)
      alert('Question supprimée avec succès')
      router.push('/admin')
    } catch (error) {
      console.error('Erreur lors de la suppression de la question', error)
      alert('Une erreur est survenue lors de la suppression')
    }
  }
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
  padding: 20px;
  border-radius: 8px;
  background: #f9f9f9;
  max-width: 500px;
  margin: 20px auto;
}
label {
  font-size: 14px;
}
textarea {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}
input[type="text"], input[type="number"], input[type="file"] {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}
button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 15px;
  cursor: pointer;
}
button:hover {
  background: #0056b3;
}
img {
  margin-top: 5px;
  border: 1px solid #ccc;
}
</style>