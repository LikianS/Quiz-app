<template>
  <header :class="['fixed top-0 w-full h-20 p-3 flex items-center text-white transition-colors duration-500 z-50', headerBgClass]">
    <RouterLink to="/" class="h-full">
      <img src="@/assets/logo.png" alt="Logo NeuroQuiz" class="h-full" />
    </RouterLink>

      <ul class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 flex space-x-10">
      <template v-if="!isAdmin">
        <li>
          <button @click="scrollToSection('about')" class="hover:text-main-violet">À propos</button>
        </li>
        <li>
          <button @click="scrollToSection('why-quiz')" class="hover:text-main-violet">Pourquoi ce quiz ?</button>
        </li>
        <li>
          <button @click="scrollToSection('scores')" class="hover:text-main-violet">Classement</button>
        </li>
      </template>
      <template v-else>
        <RouterLink to="/admin/questions/create" class="hover:text-main-violet">Créer</RouterLink>
        <RouterLink to="/admin" class="hover:text-main-violet">Éditer</RouterLink>
        <RouterLink to="/logs" class="hover:text-main-violet">Logs</RouterLink>
      </template>
    </ul>

    <div class="ml-auto flex items-center space-x-4">
      <template v-if="!isAdmin">
        <RouterLink to="/login" class="p-2 rounded-md border border-white hover:text-main-violet hover:bg-[#171717] transition">Connexion</RouterLink>
      </template>
      <template v-else>
        <button @click="logoutAdmin" class="hover:text-main-violet">Déconnexion</button>
      </template>

      <div class="flex rounded-full overflow-hidden">
        <button @click="toggleSound(true)" :class="['px-4 py-1 transition-colors', isPlaying ? 'bg-white text-black' : 'bg-black text-white']">ON</button>
        <button @click="toggleSound(false)" :class="['px-4 py-1 transition-colors', !isPlaying ? 'bg-white text-black' : 'bg-black text-white']">OFF</button>
      </div>
    </div>

    <audio ref="bgMusic" :src="themeSong" loop autoplay></audio>
  </header>
</template>

<script setup>
import { RouterLink, useRouter, useRoute } from 'vue-router';
import { ref, computed, onMounted, onUnmounted } from 'vue';
import themeSong from '@/assets/Themesong.mp3';

const router = useRouter();
const route = useRoute();

const token = ref(localStorage.getItem('token'));
const isAdmin = computed(() => !!token.value);

function handleStorageEvent() {
  token.value = localStorage.getItem('token');
}

onMounted(() => {
  window.addEventListener('storage', handleStorageEvent);
});

onUnmounted(() => {
  window.removeEventListener('storage', handleStorageEvent);
});

function logoutAdmin() {
  localStorage.removeItem('token');
  token.value = null;
  router.push('/');
}

const bgMusic = ref(null);
const isPlaying = ref(true);
function toggleSound(on) {
  if (on) {
    bgMusic.value.play().catch(() => {});
    isPlaying.value = true;
  } else {
    bgMusic.value.pause();
    isPlaying.value = false;
  }
}

const isTop = ref(true);
function handleScroll() {
  isTop.value = window.scrollY === 0;
}
window.addEventListener('scroll', handleScroll);

const isHomePage = computed(() => route.path === '/');
const headerBgClass = computed(() => (isHomePage.value && isTop.value ? 'bg-transparent' : 'bg-custom-dark'));

function scrollToSection(id) {
  const element = document.getElementById(id);
  if (!element) return;
  const yOffset = -80;
  const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
  window.scrollTo({ top: y, behavior: 'smooth' });
}
</script>
