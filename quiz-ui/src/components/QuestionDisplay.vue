<script setup>
const props = defineProps({
  question: Object,
  isAnswered: Boolean,
});
const emit = defineEmits(['answer-clicked']);
</script>

<template>
  <div v-if="question" class="bg-white shadow-lg rounded-xl p-6 md:p-8 max-w-3xl mx-auto mb-8">
    <h2 class="text-2xl md:text-3xl font-bold mb-4 text-gray-800">{{ question.text }}</h2>
    <img v-if="question.image" :src="question.image" class="w-full h-auto rounded-lg mb-6 border border-gray-200 shadow-sm" alt="Illustration question"/>


    <div class="grid gap-4">
      <button v-for="(answer, index) in question.possibleAnswers" :key="index" class="w-full py-3 px-4 text-left rounded-lg border border-main-violet hover:bg-main-violet hover:text-white transition-colors font-medium text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed" :disabled="isAnswered" @click="$emit('answer-clicked', index)">{{ answer.text }}</button>
    </div>
  </div>
</template>
