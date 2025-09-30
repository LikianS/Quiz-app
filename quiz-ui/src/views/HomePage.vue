<script setup>
import { ref, computed, onMounted } from 'vue';
import quizApiService from '@/services/QuizApiService';
import participationStorageService from '@/services/ParticipationStorageService';
import ScoreDisplay from '@/components/ScoreDisplay.vue';

const rawScores = ref([]);
const registeredScores = ref([]);
const playerName = participationStorageService.getPlayerName();
const participationScore = participationStorageService.getParticipationScore();
const bestScore = participationStorageService.getBestScore();
const totalQuestions = ref(0);
const estimatedDuration = ref(5);
const totalParticipants = ref(0);
const participationCount = ref(participationStorageService.getParticipationCount());
const lastAvgTime = ref(0);
const activeRange = ref('all');
const categories = ref(['Général', 'Science', 'Histoire', 'Tech', 'Culture', 'Sport']);
const activeCategories = ref(new Set());

function toggleCategory(cat) {
  if (activeCategories.value.has(cat)) activeCategories.value.delete(cat);
  else activeCategories.value.add(cat);
}

const filteredScores = computed(() => {
  let list = [...rawScores.value];
  const now = Date.now();
  if (activeRange.value === '24h') {
    list = list.filter((s) => now - new Date(s.date).getTime() <= 24 * 3600 * 1000);
  } else if (activeRange.value === '7d') {
    list = list.filter((s) => now - new Date(s.date).getTime() <= 7 * 24 * 3600 * 1000);
  }
  list.sort((a, b) => b.score - a.score);
  return list;
});

const globalBest = computed(() =>
  filteredScores.value.length ? filteredScores.value[0].score : null
);
const personalProgressPercent = computed(() =>
  totalQuestions.value ? (participationScore / totalQuestions.value) * 100 : 0
);
const avgTimePerQuestion = computed(() => {
  if (lastAvgTime.value) return lastAvgTime.value;
  if (totalQuestions.value && estimatedDuration.value)
    return Math.round((estimatedDuration.value * 60) / totalQuestions.value);
  return 0;
});

function setRange(r) {
  activeRange.value = r;
}

onMounted(async () => {
  rawScores.value = [
    { playerName: 'Alice Martin', score: 8, date: '2025-09-29T10:00:00Z' },
    { playerName: 'Bob Dupont', score: 10, date: '2025-09-30T08:00:00Z' },
    { playerName: 'Charlie Brown', score: 6, date: '2025-09-25T12:00:00Z' },
    { playerName: 'Diana Prince', score: 9, date: '2025-09-30T07:00:00Z' },
    { playerName: 'Eva Green', score: 7, date: '2025-09-29T16:00:00Z' },
    { playerName: 'Frank Castle', score: 10, date: '2025-09-28T09:00:00Z' },
    { playerName: 'Grace Kelly', score: 3, date: '2025-09-24T14:00:00Z' },
  ];
  registeredScores.value = filteredScores.value;
  totalParticipants.value = rawScores.value.length;
  totalQuestions.value = 10;
  participationCount.value = participationStorageService.getParticipationCount();
  const lastDur = participationStorageService.getLastDuration();
  if (lastDur && totalQuestions.value)
    lastAvgTime.value = Math.round(lastDur / totalQuestions.value);
});
</script>
<template>
  <div class="container home-page">
    <section class="intro">
      <div class="intro-left">
        <h1 class="title gradient-text">Le Méga Quiz</h1>
        <p class="tagline">Testez vos connaissances et grimpez dans le classement</p>
        <div class="cta-row">
          <router-link to="/new-quiz" class="btn-primary-lg">Commencer</router-link>
          <div class="mini-stats">
            <div class="mini-stat">
              <span class="v">{{ participationCount }}</span>
              <span class="l">Participations</span>
            </div>
            <div class="mini-stat">
              <span class="v">{{ bestScore ?? '—' }}</span>
              <span class="l">Meilleur</span>
            </div>
            <div class="mini-stat">
              <span class="v">{{ globalBest ?? '—' }}</span>
              <span class="l">Global</span>
            </div>
          </div>
        </div>
        <div v-if="playerName && participationScore" class="you-block">
          <div class="you-header">
            <span class="you-name">{{ playerName }}</span>
            <ScoreDisplay :playerName="playerName" :score="participationScore" />
          </div>
          <div class="progress-line">
            <div class="bar" :style="{ width: personalProgressPercent + '%' }"></div>
          </div>
          <div class="progress-info">
            <span>{{ participationScore }} / {{ totalQuestions }}</span>
            <span>{{ Math.round(personalProgressPercent) }}%</span>
          </div>
        </div>
      </div>
      <div class="intro-right">
        <div class="stat-grid">
          <div class="stat-card">
            <h2>{{ totalQuestions }}</h2>
            <p>Questions</p>
          </div>
          <div class="stat-card">
            <h2>{{ estimatedDuration }}m</h2>
            <p>Durée</p>
          </div>
          <div class="stat-card">
            <h2>{{ totalParticipants }}</h2>
            <p>Joueurs</p>
          </div>
          <div class="stat-card">
            <h2 v-if="avgTimePerQuestion">{{ avgTimePerQuestion }}s</h2>
            <p>Temps/Q</p>
          </div>
        </div>
      </div>
    </section>

    <section class="categories">
      <h3 class="sec-title">Catégories</h3>
      <div class="cat-list">
        <button
          v-for="c in categories"
          :key="c"
          :class="['cat-pill', { active: activeCategories.has(c) }]"
          @click="toggleCategory(c)"
        >
          {{ c }}
        </button>
      </div>
    </section>

    <section class="leaderboard-section">
      <div class="leaderboard-header">
        <h3 class="sec-title small">Hall of Fame</h3>
        <div class="filters">
          <button :class="['f-btn', { active: activeRange === 'all' }]" @click="setRange('all')">
            All
          </button>
          <button :class="['f-btn', { active: activeRange === '24h' }]" @click="setRange('24h')">
            24h
          </button>
          <button :class="['f-btn', { active: activeRange === '7d' }]" @click="setRange('7d')">
            7j
          </button>
        </div>
      </div>
      <div class="leaderboard">
        <div
          v-for="(scoreEntry, index) in filteredScores"
          :key="scoreEntry.date + scoreEntry.playerName"
          class="lb-row"
          :class="{ top: index < 3 }"
        >
          <div class="lb-left">
            <span class="rk" :class="{ r1: index === 0, r2: index === 1, r3: index === 2 }">{{
              index + 1
            }}</span>
            <span class="nm">{{ scoreEntry.playerName }}</span>
          </div>
          <span class="sc">{{ scoreEntry.score }}</span>
        </div>
        <div v-if="!filteredScores.length" class="empty">Aucun score</div>
      </div>
    </section>

    <section class="rules">
      <h3 class="sec-title">Règles</h3>
      <ol class="rules-list">
        <li>Entrez votre nom et démarrez.</li>
        <li>Choisissez la bonne réponse parmi 4 options.</li>
        <li>Votre score est enregistré et comparé au classement.</li>
      </ol>
    </section>
  </div>
</template>
<style scoped>
.home-page {
  max-width: 1100px;
  padding: 2rem 0;
  display: flex;
  flex-direction: column;
  gap: 2.2rem;
}
.title {
  margin: 0;
  font-size: 2.6rem;
  line-height: 1.05;
}
.gradient-text {
  background: linear-gradient(90deg, #2563eb, #9333ea);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  color: transparent;
}
.intro {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2.5rem;
  align-items: start;
}
.intro-left {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}
.tagline {
  margin: 0;
  color: var(--c-text-soft);
  font-size: 0.95rem;
}
.cta-row {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}
.btn-primary-lg {
  background: #1d4ed8;
  color: #fff;
  text-decoration: none;
  padding: 0.85rem 1.75rem;
  border-radius: 14px;
  font-weight: 600;
  font-size: 0.95rem;
  box-shadow: 0 4px 14px -4px rgba(29, 78, 216, 0.5);
  transition: 0.2s;
}
.btn-primary-lg:hover {
  background: #1e40af;
}
.mini-stats {
  display: flex;
  gap: 1.1rem;
}
.mini-stat {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.mini-stat .v {
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--c-text);
}
.mini-stat .l {
  font-size: 0.6rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--c-text-soft);
  font-weight: 600;
  margin-top: 0.15rem;
}
.you-block {
  background: var(--c-bg-soft);
  padding: 1rem 1rem 0.9rem;
  border-radius: 16px;
  border: 1px solid var(--c-border);
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}
.you-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}
.you-name {
  font-weight: 600;
  font-size: 0.9rem;
}
.progress-line {
  height: 8px;
  background: #2c3136;
  border-radius: 4px;
  overflow: hidden;
}
.progress-line .bar {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #9333ea);
}
.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.65rem;
  color: var(--c-text-soft);
  font-weight: 600;
  letter-spacing: 0.05em;
}
.intro-right .stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 1rem;
}
.stat-card {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 18px;
  padding: 1rem 0.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  min-height: 110px;
}
.stat-card h2 {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 700;
  color: #1d4ed8;
}
.stat-card p {
  margin: 0;
  font-size: 0.6rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--c-text-soft);
}
.sec-title {
  margin: 0 0 0.8rem;
  font-size: 0.9rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
  color: var(--c-text-soft);
}
.sec-title.small {
  font-size: 0.8rem;
  margin: 0;
}
.cat-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
}
.cat-pill {
  background: var(--c-bg-soft);
  color: var(--c-text-soft);
  border: 1px solid var(--c-border);
  padding: 0.45rem 0.85rem;
  font-size: 0.65rem;
  font-weight: 600;
  border-radius: 999px;
  cursor: pointer;
  letter-spacing: 0.05em;
}
.cat-pill.active {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}
.leaderboard-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.leaderboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.filters {
  display: flex;
  gap: 0.4rem;
}
.f-btn {
  background: var(--c-bg-soft);
  border: 1px solid var(--c-border);
  color: var(--c-text-soft);
  padding: 0.35rem 0.7rem;
  font-size: 0.6rem;
  font-weight: 600;
  border-radius: 9px;
  cursor: pointer;
  letter-spacing: 0.05em;
}
.f-btn.active {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
}
.leaderboard {
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 16px;
  max-height: 260px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  scrollbar-width: thin;
}
.leaderboard::-webkit-scrollbar {
  width: 6px;
}
.leaderboard::-webkit-scrollbar-track {
  background: var(--c-bg-soft);
  border-radius: 4px;
}
.leaderboard::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 4px;
}
.lb-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.75rem;
  border-bottom: 1px solid var(--c-border);
  font-size: 0.75rem;
}
.lb-row:last-child {
  border-bottom: none;
}
.lb-row.top {
  background: linear-gradient(90deg, rgba(37, 99, 235, 0.06), rgba(147, 51, 234, 0.06));
}
.lb-left {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  min-width: 0;
}
.rk {
  width: 30px;
  height: 30px;
  border-radius: 9px;
  background: var(--c-bg-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.7rem;
  color: var(--c-text-soft);
}
.rk.r1 {
  background: linear-gradient(135deg, #facc15, #f59e0b);
  color: #1f2937;
}
.rk.r2 {
  background: linear-gradient(135deg, #e5e7eb, #9ca3af);
  color: #1f2937;
}
.rk.r3 {
  background: linear-gradient(135deg, #fbbf24, #ea580c);
  color: #1f2937;
}
.nm {
  font-weight: 500;
  color: var(--c-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}
.sc {
  background: #2563eb;
  color: #fff;
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.7rem;
  min-width: 38px;
  text-align: center;
}
.empty {
  padding: 1rem;
  text-align: center;
  font-size: 0.7rem;
  color: var(--c-text-soft);
}
.rules-list {
  margin: 0;
  padding-left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-size: 0.7rem;
  color: var(--c-text-soft);
  line-height: 1.3;
  font-weight: 500;
  max-width: 520px;
}
@media (max-width: 640px) {
  .title {
    font-size: 2.2rem;
  }
  .intro {
    grid-template-columns: 1fr;
  }
  .nm {
    max-width: 120px;
  }
}
</style>
