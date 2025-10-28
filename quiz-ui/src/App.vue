<script setup>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import { useRoute } from 'vue-router';
const route = useRoute();
</script>

<template>
  <Header />
  <div :class="route.path !== '/' ? 'mt-32' : ''">
    <RouterView />
  </div>
  <Footer />
</template>
