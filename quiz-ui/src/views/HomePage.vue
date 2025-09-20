<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import ScoreDisplay from '@/components/ScoreDisplay.vue';

const registeredScores = ref([]);
const playerName = participationStorageService.getPlayerName();
const participationScore = participationStorageService.getParticipationScore();

onMounted(async () => {
  const result = await quizApiService.getQuizInfo();
  if (result && result.data && result.data.scores) {
    registeredScores.value = result.data.scores;
  }
});
</script>

<template>
  <h1>Home page</h1>

  <ScoreDisplay :playerName="playerName" :score="participationScore" />

  <div v-for="scoreEntry in registeredScores" :key="scoreEntry.date">
    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
  </div>
  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
</template>

<style scoped>
h1 {
  margin-bottom: 1rem;
}
</style>
