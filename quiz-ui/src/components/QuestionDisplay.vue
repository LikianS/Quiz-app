<script setup>
const props = defineProps({
  question: Object,
  isAnswered: Boolean,
});
const emit = defineEmits(['answer-clicked']);
</script>

<template>
  <div v-if="question">
    <h2>{{ question.text }}</h2>
    <img v-if="question.image" :src="question.image" class="img-fluid mb-3" />
    <div v-for="(answer, index) in question.possibleAnswers" :key="index" class="mb-2">
      <button class="btn btn-outline-primary w-100" :disabled="isAnswered" @click="$emit('answer-clicked', index)">{{ answer.text }}</button>
    </div>
  </div>
</template>
