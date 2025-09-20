<script setup>
const props = defineProps({
  question: Object,
});
const emit = defineEmits(['answer-clicked']);
</script>

<template>
  <div v-if="question">
    <h2>{{ question.label }}</h2>
    <img v-if="question.image" :src="question.image" class="img-fluid mb-3" />
    <div v-for="(answer, idx) in question.answers" :key="idx" class="mb-2">
      <button class="btn btn-outline-primary w-100" @click="emit('answer-clicked', idx)">
        {{ answer }}
      </button>
    </div>
  </div>
</template>
