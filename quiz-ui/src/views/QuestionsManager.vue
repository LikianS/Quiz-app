<script setup>
import { ref, onMounted, computed } from 'vue';
import QuestionDisplay from '../components/QuestionDisplay.vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import { useRouter } from 'vue-router';

const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestion = ref(0);
const score = ref(0);
const router = useRouter();
const isQuizFinished = ref(false);
const answers = ref([]);
const participationRows = ref([]);
const playerName = computed(() => participationStorageService.getPlayerName() || '');
const participationPayload = computed(() => {
  return JSON.stringify({ playerName: playerName.value, answers: answers.value }, null, 2);
});
const previousParticipations = ref([]);

async function loadQuestionByPosition(position) {
  try {
    const result = await quizApiService.getQuestion(position);
    if (result) {
      currentQuestion.value = result;
    } else {
      console.error('Question not found for position:', position);
    }
  } catch (error) {
    console.error('Error loading question:', error);
  }
}

async function answerClickedHandler(answerIdx) {
  if (currentQuestion.value) {
    answers.value[currentQuestionPosition.value - 1] = answerIdx;
    const selected = currentQuestion.value.possibleAnswers?.[answerIdx];
    if (selected && selected.isCorrect) {
      score.value++;
    }
    participationRows.value[currentQuestionPosition.value - 1] = {
      position: currentQuestionPosition.value,
      answerIndex: answerIdx,
      answerText: selected ? selected.text : ''
    };
  }
  if (currentQuestionPosition.value < totalNumberOfQuestion.value) {
    currentQuestionPosition.value++;
    await loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    endQuiz();
  }
}

function endQuiz() {
  isQuizFinished.value = true;
  const name = participationStorageService.getPlayerName();

  quizApiService.submitParticipation(name, answers.value)
    .then(response => {
      console.log('Participation submitted successfully:', response);
      score.value = response.score;
      participationStorageService.saveParticipationScore(score.value);
      quizApiService.getQuizInfo().then((info) => {
        if (info && info.scores) {
          previousParticipations.value = info.scores;
        }
        router.push('/score');
      }).catch(() => router.push('/score'));
    })
    .catch(error => {
      console.error('Error submitting participation:', error);
    });
}

onMounted(async () => {
  try {
    const quizInfo = await quizApiService.getQuizInfo();
    if (quizInfo && quizInfo.size) {
      totalNumberOfQuestion.value = quizInfo.size;
    }
    if (quizInfo && quizInfo.scores) {
      previousParticipations.value = quizInfo.scores;
    }
    await loadQuestionByPosition(currentQuestionPosition.value);
  } catch (error) {
    console.error('Error initializing quiz:', error);
  }
});
</script>

<template>
  <div class="container mt-5">
    <div class="row g-4">
      <div class="col-lg-8">
        <h1 v-if="!isQuizFinished">Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1>
        <p v-if="!isQuizFinished">Score actuel : {{ score }}</p>
        <QuestionDisplay
          v-if="!isQuizFinished && currentQuestion"
          :question="currentQuestion"
          @answer-clicked="answerClickedHandler"
        />
        <div v-else>
          <h2>Quiz terminé !</h2>
          <p>Votre score : {{ score }}</p>
        </div>
      </div>
    </div>
   </div>
</template>
