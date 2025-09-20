<script setup>
import participationStorageService from '@/services/ParticipationStorageService';
import ScoreDisplay from '@/components/ScoreDisplay.vue';

const playerName = participationStorageService.getPlayerName();
const participationScore = participationStorageService.getParticipationScore();
</script>

<template>
  <div class="container mt-5">
    <h1>Votre score</h1>
    <ScoreDisplay :playerName="playerName" :score="participationScore" />
    <router-link to="/" class="btn btn-primary mt-3">Retour à l'accueil</router-link>
  </div>
</template>
