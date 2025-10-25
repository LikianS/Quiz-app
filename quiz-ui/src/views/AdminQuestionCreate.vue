<template>
  <div>
    <h2>Créer une nouvelle question</h2>
    <form @submit.prevent="createQuestion">
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

      <button type="submit" style="margin-right:10px;">Créer</button>
      <button type="button" @click="cancelCreate">Annuler</button>
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