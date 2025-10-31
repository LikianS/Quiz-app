<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import { useRoute } from 'vue-router';
import backgroundImg from '@/assets/background.jpg'
const backgroundImage = backgroundImg


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

<template class="w-full min-w-screen">

  <section class="h-screen relative overflow-hidden">
    <div class="absolute inset-0 bg-cover bg-center animate-zoom-slow" :style="{ backgroundImage: `url(${backgroundImage})` }"></div>
    <div class="absolute inset-0 bg-black bg-opacity-50"></div>

    <div class="relative z-10 flex items-center h-full">
      <div class="ml-auto max-w-xl p-7 text-white">
        <h1 class="text-5xl md:text-6xl font-bold leading-tight">Connaissez-vous l'Intelligence Artificielle ?</h1>
        <p class="text-xl md:text-2xl mt-4">Testez vos connaissances en IA dès maintenant</p>
        <div class="flex flex-wrap gap-4 mt-6">
          <router-link to="/new-quiz" class="px-6 py-3 bg-main-violet hover:bg-[#A48FD0] hover:text-white rounded-lg text-lg font-semibold transition">Accéder au quiz</router-link>
          <a href="#about" class="px-6 py-3 border border-white hover:bg-white hover:text-main-violet rounded-lg text-lg font-semibold transition">En savoir plus</a>
        </div>
      </div>
    </div>
  </section>

  <section id="about" class="flex flex-col items-center justify-center text-center py-32 bg-gray-100">
    <h2 class="text-4xl md:text-5xl font-bold mb-4">L’IA qui transforme notre monde</h2>
    <p class="text-lg md:text-xl max-w-3xl mb-12 text-gray-800">L'intelligence artificielle transforme notre quotidien, révolutionne les industries et redéfinit les limites de la technologie. Testez vos connaissances et découvrez à quel point l'IA a encore beaucoup à vous apprendre.</p>
    <blockquote class="text-gray-700 italic border-l-4 border-main-violet pl-6 max-w-2xl">"L’intelligence artificielle pourrait être soit la meilleure chose qui soit arrivée à l’humanité, soit la pire." <span class="font-semibold block mt-2">– Stephen Hawking</span>  </blockquote>
  </section>

  <section id="why-quiz" class="py-32 bg-white">
    <div class="max-w-6xl mx-auto px-6 text-center">
      <h2 class="text-4xl md:text-5xl font-bold mb-2">Pourquoi relever ce défi ?</h2>
      <p class="text-lg text-gray-600 mb-12">Apprenez, découvrez et mesurez-vous à vos amis.</p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
        <div class="flex flex-col items-center bg-gray-100 rounded-lg p-8 shadow hover:shadow-lg transition">
          <img src="@/assets/quiz.svg" class="w-16 h-16 mb-4" alt="Icon Quiz"/>
          <h3 class="text-2xl font-semibold mb-2">Testez vos connaissances</h3>
          <p class="text-gray-600 text-center">Évaluez ce que vous savez sur l’IA et découvrez des informations que vous ne connaissiez peut-être pas.</p>
        </div>

        <div class="flex flex-col items-center bg-gray-100 rounded-lg p-8 shadow hover:shadow-lg transition">
          <img src="@/assets/learning.svg" fill="main-violet" class="w-16 h-16 mb-4" alt="Icon Learning"/>
          <h3 class="text-2xl font-semibold mb-2">Apprenez des faits surprenants</h3>
          <p class="text-gray-600 text-center">Chaque question apporte une nouvelle découverte sur la technologie et l’intelligence artificielle.</p>
        </div>

        <div class="flex flex-col items-center bg-gray-100 rounded-lg p-8 shadow hover:shadow-lg transition">
          <img src="@/assets/friends.svg" class="w-16 h-16 mb-4 " alt="Icon Friends"/>
          <h3 class="text-2xl font-semibold mb-2">Mesurez-vous à vos amis</h3>
          <p class="text-gray-600 text-center">Comparez vos scores, relevez des défis et débloquez des badges pour vous motiver à progresser.</p>
        </div>
      </div>
    </div>
  </section>

  <div v-if="challenge" class="alert alert-warning mt-8 max-w-5xl mx-auto px-6">
    <strong>Défi :</strong> {{ challenge.player }} a obtenu le score <b>{{ challenge.score }}</b>.<br>
    Tente de battre son score en lançant le quiz !
  </div>

  <section id="scores" class="py-32 bg-gray-50">
    <div class="max-w-5xl mx-auto px-6 flex flex-col items-center">
      <h2 class="text-4xl md:text-5xl font-bold text-center mb-8">Classement des joueurs</h2>

      <div v-if="challenge" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 p-4 rounded-md mb-12 w-full">
        <p class="font-semibold">Défi :</p>
        <p>{{ challenge.player }} a obtenu le score <span class="font-bold">{{ challenge.score }}</span>.<br>Tente de battre son score en lançant le quiz !</p>
      </div>

      <div class="bg-white shadow-md rounded-lg w-full overflow-hidden mb-12">
        <div class="bg-gray-100 px-6 py-3 font-semibold text-gray-700">Participations précédentes</div>
        <div v-if="registeredScores.length" class="overflow-x-auto">
          <table class="min-w-full text-left">
            <thead>
              <tr class="bg-gray-50">
                <th class="px-6 py-3 text-gray-600 uppercase text-sm">Joueur</th>
                <th class="px-6 py-3 text-gray-600 uppercase text-sm text-right">Score</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(scoreEntry, i) in registeredScores" :key="i" class="border-b last:border-b-0 hover:bg-gray-50 transition">
                <td class="px-6 py-3">{{ scoreEntry.playerName }}</td>
                <td class="px-6 py-3 text-right font-medium">{{ scoreEntry.score }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="px-6 py-4 text-gray-500">Aucune participation enregistrée.</p>
      </div>

      <router-link to="/new-quiz" class="px-8 py-4 bg-main-violet hover:bg-[#A48FD0] hover:text-white text-white font-semibold rounded-lg text-lg transition">Démarrer le quiz !</router-link>
    </div>
  </section>

</template>
