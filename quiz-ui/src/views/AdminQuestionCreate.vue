<template>
  <div class="max-w-2xl mx-auto p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-6">Créer une nouvelle question</h2>
    <form @submit.prevent="createQuestion" class="space-y-6 bg-white p-6 rounded-xl shadow-md">

      <div class="flex flex-col">
        <label class="mb-1 text-gray-700 font-medium">Position :</label>
        <input type="number" v-model="question.position" class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-main-violet"/>
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-gray-700 font-medium">Titre :</label>
        <input type="text" v-model="question.title" class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-main-violet"/>
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-gray-700 font-medium">Intitulé :</label>
        <textarea v-model="question.text" rows="3" class="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-main-violet"></textarea>
      </div>

      <div class="flex flex-col">
        <label class="mb-1 text-gray-700 font-medium">Image :</label>
        <input type="file" @change="onImageChange" class="mb-2"/>
        <img v-if="imagePreview" :src="imagePreview" alt="aperçu" class="w-24 border border-gray-300 rounded mt-2"/>
      </div>

      <div class="flex flex-col">
        <p class="mb-2 text-gray-700 font-medium">Réponses :</p>
        <div v-for="(answer, idx) in answers" :key="idx" class="flex items-center gap-3 mb-2">
          <input type="text" v-model="answers[idx].text" placeholder="Intitulé de la réponse" class="flex-1 border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-main-violet"/>
          <label class="flex items-center gap-1">
            <input type="checkbox" :checked="correctAnswerIndex === idx" @change="setCorrect(idx)" class="w-4 h-4"/>
            <span class="text-gray-600">Bonne réponse</span>
          </label>
        </div>
      </div>


    
      <div class="flex gap-4">
        <button type="submit" class="appearance-none focus:outline-none bg-main-violet text-white px-4 py-2 rounded-md hover:bg-[#A48FD0] transition">Créer</button>
        <button type="button" @click="cancelCreate" class="appearance-none focus:outline-none bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400 transition">Annuler</button>
        </div>


    </form>
  </div>
</template>


<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();


const question = ref({ position: 1, title: '', text: '' });
const answers = ref([
  { text: '', isCorrect: false },
  { text: '', isCorrect: false },
  { text: '', isCorrect: false },
  { text: '', isCorrect: false },
]); 
const correctAnswerIndex = ref(0); 
const imagePreview = ref(null); 
const imageFile = ref(null); 


function setCorrect(idx) {
  correctAnswerIndex.value = idx;
  answers.value.forEach((answer, index) => {
    answer.isCorrect = index === idx;
  });
}


function onImageChange(e) {
  const file = e.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
  }
}


async function createQuestion() {
  try {
    let imageBase64 = null;
    if (imageFile.value) {
      imageBase64 = await toBase64(imageFile.value);
    }
    const payload = {
      position: question.value.position,
      title: question.value.title,
      text: question.value.text,
      image: imageBase64,
      possibleAnswers: answers.value,
    };
    const res = await fetch('http://127.0.0.1:5000/questions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      throw new Error('Erreur lors de la création de la question');
    }
    alert('Question créée avec succès');
    router.push('/admin');
  } catch (error) {
    console.error('Erreur lors de la création de la question', error);
    alert('Une erreur est survenue lors de la création');
  }
async function toBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}
}


function cancelCreate() {
  router.push('/admin'); 
}
</script>
