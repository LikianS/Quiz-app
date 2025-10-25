<template>
  <div class="logs-container">
    <h2>Logs d'administration</h2>
    <div v-if="loading">Chargement...</div>
    <div v-else>
      <table v-if="logs.length" class="logs-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Utilisateur</th>
            <th>Action</th>
            <th>Endpoint</th>
            <th>Status</th>
            <th>Détails</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.timestamp + log.action + log.endpoint">
            <td>{{ log.timestamp }}</td>
            <td>{{ log.user }}</td>
            <td>{{ log.action }}</td>
            <td>{{ log.endpoint }}</td>
            <td>{{ log.status }}</td>
            <td>{{ log.details }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else>Aucun log à afficher.</div>
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

<style scoped>

.logs-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  color: #111;
}
.logs-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
  color: #111;
  font-size: 15px;
}
.logs-table th, .logs-table td {
  border: 1px solid #eee;
  padding: 8px 12px;
  text-align: left;
  color: #111;
}
.logs-table td:last-child {
  max-width: 220px;
  word-break: break-word;
  white-space: pre-line;
  overflow-wrap: anywhere;
}
.logs-table th {
  background: #f7f7f7;
  color: #111;
}
.logs-table tr:nth-child(even) {
  background: #fafafa;
}
.logs-table tr:hover {
  background: #e6e6e6;
}
</style>
