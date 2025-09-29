<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import ScoreDisplay from '@/components/ScoreDisplay.vue';

const registeredScores = ref([]);
const playerName = participationStorageService.getPlayerName();
const participationScore = participationStorageService.getParticipationScore();
const totalQuestions = ref(0);
const estimatedDuration = ref(5);
const totalParticipants = ref(0);

onMounted(async () => {
  registeredScores.value = [
    { playerName: 'Alice Martin', score: 8, date: '2024-01-01' },
    { playerName: 'Bob Dupont', score: 10, date: '2024-01-02' },
    { playerName: 'Charlie Brown', score: 6, date: '2024-01-03' },
    { playerName: 'Diana Prince', score: 9, date: '2024-01-04' },
    { playerName: 'Eva Green', score: 7, date: '2024-01-05' },
    { playerName: 'Frank Castle', score: 10, date: '2024-01-06' },
    { playerName: 'Grace Kelly', score: 3, date: '2024-01-07' },
  ].sort((a, b) => b.score - a.score);

  totalParticipants.value = registeredScores.value.length;
  totalQuestions.value = 10;

  // const result = await quizApiService.getQuizInfo();
  // if (result && result.data && result.data.scores) {
  //   registeredScores.value = result.data.scores.sort((a, b) => b.score - a.score);
  // }
});
</script>

<template>
  <div class="container mt-5">
    <div class="text-center mb-5">
      <h1 class="display-4 text-primary">Le Méga Quiz</h1>
      <p class="lead">Testez vos connaissances !</p>
    </div>

    <ScoreDisplay :playerName="playerName" :score="participationScore" />

    <h3 class="text-center mb-4">Hall of Fame</h3>
    <div
      v-for="(scoreEntry, index) in registeredScores"
      :key="scoreEntry.date"
      class="d-flex justify-content-between align-items-center py-2"
    >
      <div>
        <span class="badge bg-warning me-2">{{ index + 1 }}</span>
        <strong>{{ index + 1 }}. {{ scoreEntry.playerName }} - {{ scoreEntry.score }}</strong>
      </div>
    </div>
    <div class="text-center mb-5">
      <router-link to="/new-quiz" class="btn btn-primary btn-lg px-5 py-3">
        Commencer le défi !
      </router-link>
    </div>
    <div class="row mb-5">
      <div class="col-md-4 text-center">
        <div class="card bg-light">
          <div class="card-body">
            <h2 class="text-primary mb-1">{{ totalQuestions }}</h2>
            <small class="text-muted">Questions</small>
          </div>
        </div>
      </div>
      <div class="col-md-4 text-center">
        <div class="card bg-light">
          <div class="card-body">
            <h2 class="text-primary mb-1">{{ estimatedDuration }} min</h2>
            <small class="text-muted">Durée estimée</small>
          </div>
        </div>
      </div>
      <div class="col-md-4 text-center">
        <div class="card bg-light">
          <div class="card-body">
            <h2 class="text-primary mb-1">{{ totalParticipants }}</h2>
            <small class="text-muted">Participants</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 1rem;
}
</style>
