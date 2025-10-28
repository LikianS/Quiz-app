<script setup>
const props = defineProps({
  playerName: String,
  score: [String, Number],
});
</script>

<template>
  <div class="max-w-md mx-auto mt-8">
    <div v-if="playerName && score !== null" class="bg-white shadow-lg rounded-xl p-6 text-center">
      <p class="text-xl md:text-2xl mb-2">Bravo <strong class="text-main-violet">{{ playerName }}</strong> !</p>
      <p class="text-lg md:text-xl font-semibold text-gray-700">Votre score : <strong class="text-main-violet">{{ score }}</strong></p>
    </div>
    <div v-else class="bg-gray-100 rounded-xl p-6 text-center text-gray-500 shadow-md">
      <p>Aucun score à afficher.</p>
    </div>
  </div>
</template>
