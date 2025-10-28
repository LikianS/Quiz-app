<template>
  <div class="max-w-5xl mx-auto mt-10 p-6 bg-white rounded-xl shadow-md">
    <h2 class="text-2xl font-bold mb-4 text-gray-800">Logs d'administration</h2>
    <div v-if="loading" class="text-gray-500">Chargement...</div>

    <div v-else>
      <div v-if="logs.length" class="overflow-x-auto">
        <table class="min-w-full border border-gray-200 rounded-lg">
          <thead class="bg-gray-100">
            <tr>
              <th class="px-4 py-2 text-left text-gray-700 uppercase text-sm">Date</th>
              <th class="px-4 py-2 text-left text-gray-700 uppercase text-sm">Utilisateur</th>
              <th class="px-4 py-2 text-left text-gray-700 uppercase text-sm">Action</th>
              <th class="px-4 py-2 text-left text-gray-700 uppercase text-sm">Endpoint</th>
              <th class="px-4 py-2 text-left text-gray-700 uppercase text-sm">Status</th>
              <th class="px-4 py-2 text-left text-gray-700 uppercase text-sm">Détails</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.timestamp + log.action + log.endpoint" class="hover:bg-gray-50 transition-colors">
              <td class="px-4 py-2 text-gray-800">{{ log.timestamp }}</td>
              <td class="px-4 py-2 text-gray-800">{{ log.user }}</td>
              <td class="px-4 py-2 text-gray-800">{{ log.action }}</td>
              <td class="px-4 py-2 text-gray-800">{{ log.endpoint }}</td>
              <td class="px-4 py-2 text-gray-800">{{ log.status }}</td>
              <td class="px-4 py-2 text-gray-800 break-words max-w-xs">{{ log.details }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="text-gray-500 mt-4">Aucun log à afficher.</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import QuizApiService from '@/services/QuizApiService';

const logs = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const token = localStorage.getItem('token');
    const res = await QuizApiService.getLogs(token);
    logs.value = Array.isArray(res) ? res : [];
  } catch (e) {
    logs.value = [];
  } finally {
    loading.value = false;
  }
});
</script>
