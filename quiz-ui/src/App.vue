<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { ref, onMounted } from 'vue';
const theme = ref(localStorage.getItem('theme') || 'dark');
function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark';
  applyTheme();
}
function applyTheme() {
  localStorage.setItem('theme', theme.value);
  document.documentElement.classList.toggle('theme-dark', theme.value === 'dark');
  document.documentElement.classList.toggle('theme-light', theme.value === 'light');
}
onMounted(applyTheme);
</script>
<template>
  <header class="main-header">
    <div class="container d-flex justify-content-between align-items-center py-3">
      <RouterLink to="/" class="brand mb-0">Quiz</RouterLink>
      <nav class="d-flex gap-3 align-items-center">
        <RouterLink to="/" class="nav-link">Accueil</RouterLink>
        <RouterLink to="/admin" class="nav-link">Admin</RouterLink>
        <button class="theme-btn" @click="toggleTheme">{{ theme === 'dark' ? '☀️' : '🌙' }}</button>
      </nav>
    </div>
  </header>
  <RouterView />
</template>
<style scoped>
.main-header {
  background: linear-gradient(90deg, #1d4ed8, #7e22ce);
  color: #fff;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}
.brand {
  font-weight: 700;
  font-size: 1.25rem;
  text-decoration: none;
  color: #fff;
  letter-spacing: 0.5px;
}
.nav-link {
  color: #f1f5f9;
  text-decoration: none;
  position: relative;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
}
.nav-link.router-link-exact-active {
  color: #fff;
}
.nav-link.router-link-exact-active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -6px;
  height: 3px;
  background: #fff;
  border-radius: 2px;
}
.nav-link:hover {
  color: #fff;
  opacity: 0.85;
}
.theme-btn {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.25);
  color: #fff;
  padding: 0.35rem 0.65rem;
  border-radius: 8px;
  font-size: 0.85rem;
  cursor: pointer;
}
.theme-btn:hover {
  background: rgba(255, 255, 255, 0.25);
}
</style>
<style>
:root {
  --c-bg: #111;
  --c-bg-soft: #1c1c1f;
  --c-surface: #ffffff;
  --c-border: #e5e7eb;
  --c-text: #1f2937;
  --c-text-soft: #64748b;
}
.theme-dark {
  --c-bg: #111;
  --c-bg-soft: #1d1f22;
  --c-surface: #1f2429;
  --c-border: #2e343b;
  --c-text: #f1f5f9;
  --c-text-soft: #94a3b8;
}
.theme-light {
  --c-bg: #f8fafc;
  --c-bg-soft: #f1f5f9;
  --c-surface: #ffffff;
  --c-border: #e5e7eb;
  --c-text: #1f2937;
  --c-text-soft: #64748b;
}
html,
body,
#app {
  background: var(--c-bg);
  color: var(--c-text);
  min-height: 100%;
}
body {
  margin: 0;
  font-family:
    system-ui,
    -apple-system,
    'Segoe UI',
    Roboto,
    'Helvetica Neue',
    Arial,
    sans-serif;
}
</style>
