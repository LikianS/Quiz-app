<script setup>
const props = defineProps({
  playerName: String,
  score: [String, Number],
});
</script>

<template>
  <div v-if="playerName && score !== null">
    <p>
      Bravo <strong>{{ playerName }}</strong> !
    </p>
    <p>
      Votre score : <strong>{{ score }}</strong>
    </p>
  </div>
  <div v-else>
    <p>Aucun score à afficher.</p>
  </div>
</template>
