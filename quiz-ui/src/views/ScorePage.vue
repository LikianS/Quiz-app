<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import ScoreDisplay from '@/components/ScoreDisplay.vue';


const playerName = ref(participationStorageService.getPlayerName());
const participationScore = ref(participationStorageService.getParticipationScore());
const previousParticipations = ref([]);
const bestScore = ref(null);

onMounted(async () => {
  const quizInfo = await quizApiService.getQuizInfo();
  if (quizInfo && quizInfo.scores) {
    previousParticipations.value = quizInfo.scores;
    const scoresForPlayer = quizInfo.scores.filter(s => s.playerName === playerName.value);
    if (scoresForPlayer.length > 1) {
      bestScore.value = Math.max(...scoresForPlayer.map(s => s.score));
    }
  }
});
</script>

<template>
  <div class="container mt-5">
    <h1>Votre score</h1>

    <ScoreDisplay :playerName="playerName" :score="participationScore" />
    <div v-if="bestScore !== null" class="alert alert-info mt-3">
      <strong>Meilleur score :</strong> {{ bestScore }}
    </div>

    <div class="card mt-4">
      <div class="card-header">Participations précédentes</div>
      <div class="card-body">
        <div class="table-responsive" v-if="previousParticipations.length">
          <table class="table table-sm table-striped">
            <thead>
              <tr>
                <th>Joueur</th>
                <th class="text-end">Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(scoreEntry, i) in previousParticipations" :key="i"
                  :class="{ 'table-success': scoreEntry.playerName === playerName }">
                <td>{{ scoreEntry.playerName }}</td>
                <td class="text-end">{{ scoreEntry.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-muted">Aucune participation enregistrée.</p>
      </div>
    </div>

    <router-link to="/" class="btn btn-primary mt-3">Retour à l'accueil</router-link>
  </div>
</template>
