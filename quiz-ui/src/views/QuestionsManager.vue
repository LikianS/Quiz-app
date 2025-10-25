<script setup>
const feedback = ref(null);
const feedbackText = ref("");
const progressPercent = computed(() => {
  return totalNumberOfQuestion.value > 0
    ? Math.round((currentQuestionPosition.value - 1) / totalNumberOfQuestion.value * 100)
    : 0;
});
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
      feedback.value = 'success';
      feedbackText.value = 'Bonne réponse !';
    } else {
      feedback.value = 'error';
      feedbackText.value = 'Mauvaise réponse.';
    }
    participationRows.value[currentQuestionPosition.value - 1] = {
      position: currentQuestionPosition.value,
      answerIndex: answerIdx,
      answerText: selected ? selected.text : '',
    };
    setTimeout(async () => {
      feedback.value = null;
      feedbackText.value = "";
      if (currentQuestionPosition.value < totalNumberOfQuestion.value) {
        currentQuestionPosition.value++;
        await loadQuestionByPosition(currentQuestionPosition.value);
      } else {
        endQuiz();
      }
    }, 900);
  }
}

function endQuiz() {
  isQuizFinished.value = true;
  const name = participationStorageService.getPlayerName();

  quizApiService
    .submitParticipation(name, answers.value, score.value)
    .then((response) => {
      console.log('Participation submitted successfully:', response);
      participationStorageService.saveParticipationScore(score.value);
      quizApiService
        .getQuizInfo()
        .then((info) => {
          if (info && info.scores) {
            previousParticipations.value = info.scores;
          }
          router.push('/score');
        })
        .catch(() => router.push('/score'));
    })
    .catch((error) => {
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
        <div v-if="!isQuizFinished">
          <div class="d-flex align-items-center mb-2">
            <span>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</span>
            <div class="progress flex-grow-1 ms-3" style="height: 18px;">
              <div class="progress-bar" :style="{ width: ((currentQuestionPosition-1)/totalNumberOfQuestion*100)+'%' }"></div>
            </div>
          </div>
          <p>Score actuel : {{ score }}</p>
          <div v-if="feedback" :class="['alert', feedback === 'success' ? 'alert-success animate__animated animate__bounceIn' : 'alert-danger animate__animated animate__shakeX']">
            {{ feedbackText }}
          </div>
          <Transition
            name="question-fade"
            mode="out-in"
            enter-active-class="animate__animated animate__fadeIn"
            leave-active-class="animate__animated animate__fadeOut"
          >
            <div v-if="currentQuestion" :key="currentQuestion.id">
              <h3 class="mb-3">{{ currentQuestion.title }}</h3>
              <QuestionDisplay :question="currentQuestion" @answer-clicked="answerClickedHandler" />
            </div>
          </Transition>
        </div>
        <div v-else>
          <h2>Quiz terminé !</h2>
          <p>Votre score : {{ score }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
