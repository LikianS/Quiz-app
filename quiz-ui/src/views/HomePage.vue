<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import { useRoute } from 'vue-router';


const registeredScores = ref([]);
const playerName = participationStorageService.getPlayerName();
const participationScore = participationStorageService.getParticipationScore();

const route = useRoute();
const challenge = ref(null);
onMounted(() => {
  const params = route.query;
  if (params.challenge && params.player && params.score) {
    challenge.value = {
      player: params.player,
      score: Number(params.score)
    };
  }
});

onMounted(async () => {
  const result = await quizApiService.getQuizInfo();
  if (result && result.scores) {
    registeredScores.value = result.scores;
  }
});
</script>

<template>

  <h1>Home page</h1>
  <div v-if="challenge" class="alert alert-warning mt-3">
    <strong>Défi :</strong> {{ challenge.player }} a obtenu le score <b>{{ challenge.score }}</b>.<br>
    Tente de battre son score en lançant le quiz !
  </div>

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
