<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from '@/services/ParticipationStorageService';

const username = ref('');
const router = useRouter();

function launchNewQuiz() {
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<template>
  <section class="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-6">
    <div class="bg-white shadow-lg rounded-xl p-10 max-w-md w-full">
      <h1 class="text-3xl md:text-4xl font-bold text-center mb-6">Nouveau Quiz</h1>
      <p class="text-center text-gray-600 mb-6">Entrez votre nom pour commencer et testez vos connaissances en Intelligence Artificielle.</p>
      <form @submit.prevent="launchNewQuiz" class="flex flex-col gap-4">
        <input id="username" type="text" v-model="username" placeholder="Votre nom" required class="px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-violet focus:border-main-violet transition"/>
        <button type="submit" class="w-full py-3 bg-main-violet text-white font-semibold rounded-lg hover:bg-main-dark transition">Commencer le quiz</button>
      </form>
    </div>
  </section>
</template>
