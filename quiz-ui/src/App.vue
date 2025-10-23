<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { ref, onMounted, onUnmounted } from 'vue';

import clickSound from '@/assets/clickvalide.mp3';
import emptyClickSound from '@/assets/clickdenied.mp3';
import themeSong from '@/assets/Themesong.mp3';

const clickAudio = ref(null);
const emptyClickAudio = ref(null);
const bgMusic = ref(null);
const volume = ref(1);

function setVolume() {
  if (clickAudio.value) clickAudio.value.volume = volume.value;
  if (emptyClickAudio.value) emptyClickAudio.value.volume = volume.value;
  if (bgMusic.value) bgMusic.value.volume = volume.value;
}

function playClickSound(e) {
  setVolume();
  if (
    e.target.tagName === 'BUTTON' ||
    e.target.closest('button') ||
    e.target.tagName === 'A' ||
    e.target.closest('a')
  ) {
    clickAudio.value.currentTime = 0;
    clickAudio.value.play().catch(() => {});
  } else {
    emptyClickAudio.value.currentTime = 0;
    emptyClickAudio.value.play().catch(() => {});
  }
}

onMounted(() => {
  window.addEventListener('click', playClickSound);
  setVolume();

  if (bgMusic.value && bgMusic.value.paused) {
    bgMusic.value.play().catch(() => {});
  }
});

onUnmounted(() => {
  window.removeEventListener('click', playClickSound);
});
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
    <div class="wrapper">
      <nav>
        <audio ref="bgMusic" :src="themeSong" autoplay loop></audio>

        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to="/login">Admin (Protected)</RouterLink>
      </nav>
    </div>
  </header>

  <audio ref="clickAudio" :src="clickSound"></audio>
  <audio ref="emptyClickAudio" :src="emptyClickSound"></audio>

  <div style="margin: 1rem">
    <label>Volume :</label>
    <input type="range" min="0" max="1" step="0.01" v-model="volume" @input="setVolume" />
  </div>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: var(--color-text);
  transition:
    background-color 0.3s,
    color 0.3s;
}

nav a:hover {
  background-color: #f0f0f0;
  color: #007bff;
}

nav a.router-link-exact-active {
  font-weight: bold;
  color: #0056b3;
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;
    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
