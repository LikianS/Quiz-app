<template>
<div class="bg-[#171717] text-white w-screen h-[85vh] flex items-center justify-center">
  <div class="max-w-md w-full text-center">
    <h2 class="text-4xl mb-4">Connexion</h2>
    <p class="mb-6">Vous êtes administrateur ? Connectez-vous ici !</p>
    <form @submit.prevent="handleLogin" class="space-y-4">
      <div>
        <label for="password" class="block text-left">Mot de passe :</label>
        <input id="password" type="password" v-model="password" class="w-full p-2 rounded bg-[#222] border border-gray-600 focus:outline-none focus:ring focus:ring-gray-400" placeholder="Entrez votre mot de passe"/>
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
