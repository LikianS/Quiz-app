<script setup>
import { ref, onMounted } from 'vue';
import QuestionDisplay from '../components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import { useRouter } from 'vue-router';

const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestion = ref(0);
const score = ref(0);
const router = useRouter();

async function loadQuestionByPosition(position) {
  const result = await quizApiService.getQuestion(position);
  if (result && result.data) {
    currentQuestion.value = result.data;
  }
}

async function answerClickedHandler(answerIdx) {
  if (currentQuestion.value && answerIdx === currentQuestion.value.correctAnswer) {
    score.value++;
  }
  if (currentQuestionPosition.value < totalNumberOfQuestion.value) {
    currentQuestionPosition.value++;
    await loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
}

function endQuiz() {
  participationStorageService.saveParticipationScore(score.value);
  router.push('/score');
}

onMounted(async () => {
  const quizInfo = await quizApiService.getQuizInfo();
  if (quizInfo && quizInfo.data && quizInfo.data.totalQuestions) {
    totalNumberOfQuestion.value = quizInfo.data.totalQuestions;
  }
  await loadQuestionByPosition(currentQuestionPosition.value);
});
</script>

<template>
  <div class="container mt-5">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
    <QuestionDisplay :question="currentQuestion" @answer-clicked="answerClickedHandler" />
  </div>
</template>
