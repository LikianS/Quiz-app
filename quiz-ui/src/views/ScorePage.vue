<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import ScoreDisplay from '@/components/ScoreDisplay.vue';

const playerName = ref(participationStorageService.getPlayerName());
const participationScore = ref(participationStorageService.getParticipationScore());
const previousParticipations = ref([]);
const bestScore = ref(null);
const challengeUrl = ref("");

function generateChallengeUrl() {
  const baseUrl = window.location.origin;
  const params = new URLSearchParams({
    player: playerName.value,
    score: participationScore.value
  });
  challengeUrl.value = `${baseUrl}/?challenge=1&${params.toString()}`;
}

onMounted(async () => {
  const quizInfo = await quizApiService.getQuizInfo();
  if (quizInfo && quizInfo.scores) {
    previousParticipations.value = quizInfo.scores;
    const scoresForPlayer = quizInfo.scores.filter(s => s.playerName === playerName.value);
    if (scoresForPlayer.length > 0) {
      bestScore.value = Math.max(...scoresForPlayer.map(s => s.score));
    }
  }
});
</script>

<template>
  <div class="max-w-4xl mx-auto p-6 space-y-6">
    <h1 class="text-4xl font-bold text-center text-main-violet">Votre score</h1>

    <div class="flex justify-center">
      <ScoreDisplay :playerName="playerName" :score="participationScore" />
    </div>


    <div v-if="bestScore !== null" class="bg-blue-100 text-blue-800 px-4 py-2 rounded-md text-center font-semibold">Meilleur score : {{ bestScore }}</div>

    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <div class="bg-gray-100 px-6 py-3 font-semibold text-gray-700">Participations précédentes</div>
      <div v-if="previousParticipations.length" class="overflow-x-auto">
        <table class="min-w-full text-left divide-y divide-gray-200">
          <thead>
            <tr class="bg-gray-50">
              <th class="px-6 py-3 text-gray-600 uppercase text-sm">Joueur</th>
              <th class="px-6 py-3 text-gray-600 uppercase text-sm text-right">Score</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="(scoreEntry, i) in previousParticipations" :key="i" :class="scoreEntry.playerName === playerName ? 'bg-green-50 font-semibold' : ''">
              <td class="px-6 py-3">{{ scoreEntry.playerName }}</td>
              <td class="px-6 py-3 text-right">{{ scoreEntry.score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="p-4 text-gray-500 text-center">Aucune participation enregistrée.</p>
    </div>

    <div class="flex flex-col md:flex-row items-center gap-3">
      <button class="bg-main-violet text-white px-6 py-2 rounded-lg hover:bg-main-dark transition" @click="generateChallengeUrl"> Partager mon score</button>
      <div v-if="challengeUrl" class="flex items-center w-full md:w-auto gap-2 mt-2 md:mt-0">
        <input :value="challengeUrl" readonly class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm" />
        <button class="bg-gray-200 px-3 py-2 rounded-lg hover:bg-gray-300 transition" @click="() => navigator.clipboard.writeText(challengeUrl)">Copier</button>
      </div>
    </div>
    <p v-if="challengeUrl" class="text-gray-500 text-sm text-center md:text-left mt-1">Envoie ce lien à un ami pour qu'il tente de battre ton score !</p>

    <router-link to="/" class="block text-center bg-main-dark text-white px-6 py-2 rounded-lg hover:bg-main-violet transition mt-4">Retour à l'accueil</router-link>
  </div>
</template>
