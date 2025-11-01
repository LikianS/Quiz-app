<script setup>
const props = defineProps({
  question: Object,
  isAnswered: Boolean,
});
const emit = defineEmits(['answer-clicked']);
</script>

<template>
  <div v-if="question" class="w-full flex items-center justify-center">
    <div class="bg-white shadow-lg rounded-xl p-6 md:p-8 max-w-4xl w-full mx-4">
      <div class="md:flex md:items-center md:space-x-6">
        <div class="md:w-1/2 flex flex-col justify-center">
          <h2 class="text-1xl md:text-1xl font-bold mb-4 text-gray-800 leading-tight">{{ question.text }}</h2>
          <img
            v-if="question.image"
            :src="question.image"
            class="w-full md:max-w-sm h-auto rounded-lg mb-6 border border-gray-200 shadow-sm object-contain"
            alt="Illustration question"
          />
        </div>

        <div class="md:w-1/2 mt-4 md:mt-0">
          <div class="flex flex-col gap-4">
            <button
              v-for="(answer, index) in question.possibleAnswers"
              :key="index"
              class="w-full py-3 px-4 text-left rounded-lg border border-main-violet hover:bg-main-violet hover:text-white transition-colors font-medium text-gray-800 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="isAnswered"
              @click="$emit('answer-clicked', index)"
            >
              {{ answer.text }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
