<template>
  <div class="max-w-xl mx-auto mt-10 p-6 bg-gray-50 rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Éditer la question</h2>

    <form @submit.prevent="saveQuestion" class="space-y-6">

      <div class="flex gap-4">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-1">Position :</label>
          <input type="number" v-model="question.position" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-main-violet focus:border-main-violet"/>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-1">Titre :</label>
          <input type="text" v-model="question.title" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-main-violet focus:border-main-violet"/>
        </div>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Intitulé :</label>
        <textarea v-model="question.text" rows="3" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-main-violet focus:border-main-violet"></textarea>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Image :</label>
        <input type="file" @change="onImageChange" class="block w-full text-gray-700" />
        <div v-if="imagePreview" class="mt-2">
          <img :src="imagePreview" alt="aperçu" class="w-full border border-gray-300 rounded-md" />
        </div>
      </div>
      <div>
        <p class="text-gray-700 font-medium mb-2">Réponses :</p>
        <div v-for="(answer, idx) in answers" :key="idx" class="flex items-center gap-2 mb-2">
          <input type="text" v-model="answers[idx].text" placeholder="Intitulé de la réponse" class="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:ring-main-violet focus:border-main-violet"/>
          <label class="flex items-center gap-1">
            <input type="checkbox" :checked="correctAnswerIndex === idx" @change="setCorrect(idx)" class="w-4 h-4 text-main-violet border-gray-300 rounded"/>
            <span class="text-gray-600 text-sm">Bonne réponse</span>
          </label>
        </div>
      </div>

      <div class="flex gap-4">
        <button type="submit" class="bg-main-violet text-white px-4 py-2 rounded-md hover:bg-[#A48FD0] transition">Sauvegarder</button>
        <button type="button" @click="cancelEdit" class="bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition">Annuler</button>
        <button type="button" @click="deleteQuestion" class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition">Supprimer</button>
      </div>

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
