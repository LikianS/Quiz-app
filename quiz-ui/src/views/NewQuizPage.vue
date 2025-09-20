<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  console.log("Launch new quiz with", username.value);
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<template>
  <div class="container mt-5" style="max-width: 400px">
    <h1 class="mb-4">Nouveau Quiz</h1>
    <form @submit.prevent="launchNewQuiz">
      <div class="mb-3">
        <label for="username" class="form-label">Nom du joueur</label>
        <input id="username" type="text" class="form-control" v-model="username" required />
      </div>
      <button type="submit" class="btn btn-primary w-100">Commencer</button>
    </form>
  </div>
</template>
