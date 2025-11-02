<template>
<div class="bg-[#171717] text-white w-screen h-[85vh] flex items-center justify-center">
  <div class="max-w-md w-full text-center">
    <h2 class="text-4xl mb-4">Connexion</h2>
    <p class="mb-6">Vous êtes administrateur ? Connectez-vous ici !</p>
    <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="password" class="block text-left">Mot de passe :</label>
          <div class="relative">
            <input
              id="password"
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              class="w-full p-2 rounded bg-[#222] border border-gray-600 focus:outline-none focus:ring focus:ring-gray-400"
              placeholder="Entrez votre mot de passe"
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              @mousedown.prevent
              class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-300 hover:text-white"
              :aria-pressed="showPassword.toString()"
              aria-label="Afficher/Masquer le mot de passe"
            >
              
              <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              
              <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.269-2.943-9.543-7a9.965 9.965 0 012.022-3.3M6.1 6.1L17.9 17.9" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.88 9.88a3 3 0 104.24 4.24" />
              </svg>
            </button>
          </div>
        </div>
      <button type="submit" class="w-full py-2 bg-gray-700 hover:bg-gray-600 rounded transition">Connexion</button>
      <p v-if="error" class="text-red-500 mt-2">Mauvais mot de passe</p>
    </form>
  </div>
</div>

</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import QuizApiService from '@/services/QuizApiService';

const password = ref('');
const showPassword = ref(false);
const error = ref(false);
const router = useRouter();

async function handleLogin() {
  try {
    const res = await QuizApiService.loginAdmin(password.value);
    if (res && res.token) {
      localStorage.setItem('token', res.token);
      window.dispatchEvent(new Event('storage'));
      error.value = false;
      router.push('/admin');
    } else {
      error.value = true;
    }
  } catch (e) {
    error.value = true;
  }
}
</script>
