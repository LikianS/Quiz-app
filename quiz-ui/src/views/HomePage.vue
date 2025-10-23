<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';

const registeredScores = ref([]);
const playerName = participationStorageService.getPlayerName();
const participationScore = participationStorageService.getParticipationScore();

onMounted(async () => {
  const result = await quizApiService.getQuizInfo();
  if (result && result.scores) {
    registeredScores.value = result.scores;
  }
});
</script>

<template>
  <h1>Home page</h1>

  <div class="card mt-3">
    <div class="card-header">Participations précédentes</div>
    <div class="card-body">
      <div class="table-responsive" v-if="registeredScores.length">
        <table class="table table-sm table-striped">
          <thead>
            <tr>
              <th>Joueur</th>
              <th class="text-end">Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(scoreEntry, i) in registeredScores" :key="i">
              <td>{{ scoreEntry.playerName }}</td>
              <td class="text-end">{{ scoreEntry.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="text-muted">Aucune participation enregistrée.</p>
    </div>
  </div>
  <router-link to="/new-quiz">Démarrer le quiz !</router-link>
</template>

<style scoped>
h1 {
  margin-bottom: 1rem;
}
</style>
